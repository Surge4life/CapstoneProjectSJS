# Chapter 11 — Security Doctrine

## Security as a Constitutional Requirement

Security in the G.O.D.S ecosystem is not a feature layer. It is a constitutional requirement derived from the sovereignty and audit pillars. A system that can be compromised cannot provide governance guarantees. Therefore, security is inseparable from governance.

---

## The Security Perimeter Model

The G.O.D.S ecosystem operates with a layered security perimeter model. Each layer is independently secured. Compromise of one layer does not automatically compromise the others.

```
Layer 5: Application (RBAC, input validation, output encoding)
Layer 4: Service (mTLS, service-to-service auth, JWT validation)
Layer 3: Network (TLS, firewall rules, VPC isolation)
Layer 2: Compute (OS hardening, minimal attack surface, no SSH in production)
Layer 1: Cryptographic (HSM/TPM key management, HMAC sealing, Dilithium refs)
```

---

## Authentication Architecture

### User Authentication (JWT)
- Tokens issued by `/auth/login` endpoint
- RS256 signing (RSA private key, 2048-bit minimum)
- Token expiry: 8 hours (configurable, minimum 1 hour, maximum 24 hours)
- Refresh tokens: 30 days, single-use, stored as bcrypt hash
- `kid` (key ID) header supports key rotation
- Token revocation via Redis blacklist (immediate effect, no waiting for expiry)

### Service-to-Service Authentication (mTLS)
- All internal service-to-service communication uses mutual TLS
- Each service has a client certificate issued by the platform's CA
- Certificate rotation is automated
- mTLS enforcement: the `core/mtls.py` module in `platform-core`

### Hardware Authentication (PKCS#11)
- HSM/TPM integration via PKCS#11 interface
- Master key sealed in hardware
- Key derivation for audit sealing happens in the HSM — private keys never leave hardware
- Emulated in development via software HSM (`hw-bringup/drivers/hsm_pkcs11/`)

---

## Authorisation Architecture (RBAC)

Roles are defined in the `rbac` router and `rbac` service. Every role has:
- A unique name
- A set of permissions (resource:action pairs)
- An optional division scope (a role can be scoped to a specific division)
- An optional jurisdiction scope

### Core Roles

| Role | Scope | Key Permissions |
|------|-------|----------------|
| `gods_admin` | All | Full platform control |
| `division_admin` | Division | Full division control |
| `compliance` | All | Read all; write compliance records |
| `sovereignty` | All | Read all; manage sovereignty declarations |
| `supervisor` | Division | Review OversightCases within division |
| `operator` | All | Register AI models; view own governance records |
| `analyst` | Division | Read divisional analytics |
| `learner` | SETHS | Own SETHS records only |
| `employer` | SETHS | Own employer records; posted opportunities |
| `investor` | MADIBA | Own investor records |
| `external_auditor` | All | Read-only audit chain access |

### Permission Inheritance
Higher roles inherit all permissions of lower roles within their scope. `gods_admin` inherits everything. Custom roles are built by composing permissions directly, not by inheriting from default roles.

---

## Data Security

### Data at Rest
- PostgreSQL: AES-256 encryption at the storage layer (disk encryption)
- Cassandra: Same storage encryption
- Object storage (documents): AES-256 per-object encryption with key stored in key service
- Redis: Encrypted at rest; TLS in transit

### Data in Transit
- All external traffic: TLS 1.3 minimum
- All internal traffic: mTLS
- No plaintext transmission of any data at any point in the stack

### Data Classification

| Classification | Examples | Controls |
|---------------|---------|---------|
| Constitutional | Audit records, governance decisions | Immutable, HMAC-sealed, HSM-key-protected |
| Sensitive | PII, financial data, credentials | Encrypted at rest and transit, RBAC-restricted |
| Internal | Operational logs, metrics, configurations | Encrypted at rest, authenticated access |
| Public | API documentation, health endpoints | No authentication required |

---

## Cryptographic Standards

| Purpose | Algorithm | Key Size | Notes |
|---------|----------|---------|-------|
| JWT signing | RS256 | 2048-bit | PKCS#1 v1.5 |
| Audit HMAC | HMAC-SHA256 | 256-bit | Key stored in HSM |
| Password hashing | bcrypt | cost=12 | |
| Document hashing | SHA-256 | 256-bit | Integrity verification |
| Post-quantum reference | Dilithium (reference) | Standard | For audit seal attestation |
| TLS | TLS 1.3 | System default | Forward secrecy required |

---

## Vulnerability Management

### Dependency Scanning
- Python dependencies: `pip-audit` in CI pipeline
- Node dependencies: `npm audit` in CI pipeline
- Docker base images: `trivy` scan in CI pipeline

### Penetration Testing
- Annual third-party penetration test before each major release
- Internal security review for every new router and service

### Incident Response
The G.O.D.S incident response procedure:
1. Detection (automated via SIEM hooks in `services/audit_writer.py`)
2. Containment (service isolation via the `access_control` service)
3. Assessment (forensic review of audit chain — the audit chain cannot be tampered with)
4. Remediation (fix + deploy + audit record of the fix)
5. Post-incident review (documented in the immutable audit chain)
