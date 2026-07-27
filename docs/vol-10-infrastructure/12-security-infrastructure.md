# Chapter 12 — Security Infrastructure

## Security at Every Layer

Security in the G.O.D.S infrastructure is not a perimeter — it is layered from the network level to the application level to the database level. A compromise at one layer should not automatically compromise all layers.

---

## Layer 1: Network Security

### Kubernetes NetworkPolicy

Every namespace has a default-deny policy:

```yaml
# infra/k8s/network-policies/default-deny.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: gods-ns
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

Explicit allow rules are added for each legitimate communication path:

```yaml
# Allow platform-core to call governance engines
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-platform-to-governance
  namespace: gods-ns
spec:
  podSelector:
    matchLabels: { app: eva-engine }
  ingress:
    - from:
        - podSelector:
            matchLabels: { app: platform-core }
      ports:
        - protocol: TCP
          port: 3002
```

### NGINX Ingress Security

```nginx
# WAF rules
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/main.conf;

# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
limit_req_zone $binary_remote_addr zone=auth:10m rate=10r/m;

# Security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options nosniff always;
add_header X-Frame-Options DENY always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self';" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

---

## Layer 2: mTLS (Service-to-Service)

All service-to-service communication within the cluster uses mTLS via Istio service mesh (or manual mTLS certificates for deployments without Istio):

- platform-core ↔ EVA engine: mTLS (server presents cert; client verifies + presents own cert)
- udoc-agent ↔ platform-core: mTLS (edge node must present a valid certificate)
- Internal Kafka consumers: SASL/SSL

---

## Layer 3: Secrets Management

No secrets in environment variables (except for small Render deployments where Vault is not practical). All secrets in Vault:

| Secret Type | Vault Path | Rotation |
|-------------|-----------|----------|
| Database credentials | `database/creds/platform-core` | 1 hour (dynamic) |
| JWT signing key (RS256) | `secret/jwt_private_key` | 90 days (manual + auto) |
| HMAC seal key | `secret/hmac_key` | 90 days |
| Kafka SASL password | `secret/kafka_sasl` | 90 days |
| Encryption keys (AES-256) | `transit/keys/gods-data` | Annual |

Dynamic database credentials (1-hour TTL) mean that even if a credential is leaked, it expires quickly. The Vault audit log shows every credential issuance.

---

## Layer 4: Application Security

### JWT Security

```python
ALGORITHM = "RS256"                    # Asymmetric — signing key never leaves the server
ACCESS_TOKEN_EXPIRE_MINUTES = 15       # Short-lived; refresh token used for persistence
REFRESH_TOKEN_EXPIRE_DAYS = 7
TOKEN_FAMILY_TRACKING = True           # Detect stolen refresh tokens via family invalidation
```

The RS256 algorithm means the public key (used for verification) can be distributed; the private key (used for signing) never leaves the HSM/Vault.

### RBAC Enforcement

```python
# Every protected endpoint uses require_permission()
@router.post("/oversight/{case_id}/resolve")
async def resolve_case(
    case_id: UUID,
    request: ResolveRequest,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("oversight:review:division"))
):
    ...
```

The `require_permission()` dependency is injected by the framework — it is not possible to forget to add it. There is no "public" route decorator — every route is either explicitly public or explicitly requires a permission.

### Input Validation

All inputs validated by Pydantic:
- String lengths bounded
- UUIDs validated as proper UUID format
- Enums validated against permitted values
- No raw SQL construction — all queries use SQLAlchemy ORM or parameterised queries
- No `eval()`, `exec()`, or dynamic code execution anywhere

### SAST and Dependency Scanning

Weekly automated scans:
- `bandit` SAST scan — Python security issues
- `pip-audit` — Python dependency CVEs
- `npm audit` — Node.js dependency CVEs
- Results reviewed by designated security owner within 48 hours

---

## Incident Response

Security incidents follow a defined response process:

1. **Detect** — automated alert or manual report
2. **Contain** — isolate affected component (suspend model, revoke token, block IP)
3. **Assess** — determine scope (which data, which users, which governance records)
4. **Notify** — Information Regulator notification within 72 hours if POPIA breach (Section 22)
5. **Remediate** — fix root cause
6. **Document** — `SYSTEM.SECURITY_INCIDENT` audit record created
7. **Review** — post-incident review, preventive measures

Every security incident is a governance event. It is recorded in the audit chain regardless of severity.
