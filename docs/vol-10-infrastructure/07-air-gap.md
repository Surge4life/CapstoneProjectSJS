# Chapter 07 — Air-Gap Deployment

## What Air-Gap Means in the G.O.D.S Context

An air-gapped G.O.D.S deployment runs entirely within a physically isolated network — no internet connectivity, no cloud services, no external API calls. All services run on hardware controlled by the deploying institution.

This is the highest tier of institutional sovereignty. It is not the default deployment mode, but the entire architecture is designed so that any G.O.D.S installation *can* be air-gapped without compromising functionality or governance guarantees.

---

## Why Air-Gap is a Requirement (Not a Nice-to-Have)

The G.O.D.S ecosystem is designed for institutions whose governance requirements include:

1. **National security considerations** — government agencies that cannot have citizen data transit commercial networks
2. **Regulatory data residency** — financial institutions required to keep data entirely within a specific jurisdiction
3. **Institutional sovereignty** — organisations that require complete control over their governance infrastructure
4. **Critical infrastructure protection** — utilities, healthcare, justice systems that cannot accept internet-dependent governance

For these institutions, cloud deployment is not an option. G.O.D.S meets them where they are.

---

## Air-Gap Architecture Differences

### What Changes in Air-Gap Mode

| Component | Cloud Mode | Air-Gap Mode |
|-----------|-----------|-------------|
| Container registry | Docker Hub / cloud registry | Private registry (on-premise) |
| Object storage | S3-compatible cloud | MinIO (self-hosted S3-compatible) |
| Secrets management | Cloud secrets manager | HashiCorp Vault (self-hosted) |
| External intelligence | Optional (user-initiated) | Disabled |
| Monitoring | Cloud APM | Prometheus + Grafana (self-hosted) |
| Certificate authority | Let's Encrypt / cloud CA | Self-hosted CA (Step CA) |
| Time synchronisation | Cloud NTP | Internal NTP server |
| Package updates | Internet registry | Mirrored package registry |

### What Does NOT Change in Air-Gap Mode

- The governance path (identical)
- The audit chain (identical)
- The constitutional checks (identical)
- The GBS Runtime (identical)
- The API surface (identical)
- The frontend applications (identical)
- The security model (identical)

---

## Air-Gap Deployment Checklist

### Pre-Deployment (Requires Internet Access)

These steps are performed before the hardware is physically isolated:

```bash
# 1. Pull all required container images
docker pull gods-platform-core:v2.1.0
docker pull gods-governance-engines:v2.1.0
docker pull postgres:15-alpine
docker pull redis:7-alpine
docker pull confluentinc/cp-kafka:7.5.0
docker pull cassandra:4.1
docker pull opensearch/opensearch:2.11.0
docker pull minio/minio:latest
docker pull hashicorp/vault:latest

# 2. Save images to tar files
docker save gods-platform-core:v2.1.0 | gzip > gods-platform-core-v2.1.0.tar.gz
# ... repeat for all images

# 3. Build private container registry
# (Set up a registry.tar.gz with all images for transfer to air-gapped environment)

# 4. Download all Python packages
pip download -r requirements.txt -d ./packages/python/

# 5. Download all Node.js packages
npm pack --pack-destination ./packages/npm/ [each package]

# 6. Generate all required TLS certificates
# (Root CA + intermediate CA + service certificates)

# 7. Generate initial database migration scripts
alembic upgrade head --sql > initial-migration.sql

# 8. Export platform configuration
gods-cli export-config --output gods-config-v2.1.0.tar.gz
```

### On-Site Deployment

```bash
# 1. Load container images into local registry
docker load < gods-platform-core-v2.1.0.tar.gz
docker tag gods-platform-core:v2.1.0 registry.internal:5000/gods-platform-core:v2.1.0

# 2. Install offline packages
pip install --no-index --find-links=./packages/python/ -r requirements.txt

# 3. Configure internal DNS (registry.internal, kafka.internal, postgres.internal, etc.)

# 4. Deploy infrastructure services
kubectl apply -f infra/k8s/air-gap/

# 5. Run initial migrations
kubectl exec -it platform-core-pod -- alembic upgrade head

# 6. Verify all services healthy
gods-cli health-check --all
```

---

## The udoc-edge in Air-Gap Mode

The `udoc-edge` component is specifically designed for air-gapped operation. In air-gap mode:

1. The edge downloads the complete model registry and PolicyPack during the last connectivity window
2. All governance requests are processed locally using the cached registry and rules
3. Decisions are written to local persistent storage (SQLite or PostgreSQL, depending on configuration)
4. When connectivity is restored (even briefly), the edge syncs: pushes accumulated decisions to `platform-core`, pulls updated registry and PolicyPacks

The edge maintains a **governance continuity window** — the maximum time it can operate without syncing before requiring a manual review of accumulated decisions. Default: 30 days. After this window, the edge enters REVIEW mode for all decisions (no automatic APPROVEs) until a sync occurs.

---

## Signed Update Delivery

In air-gap environments, software updates cannot be delivered over the internet. The update delivery mechanism:

1. G.O.D.S engineering team produces a signed update bundle:
   - Container images (tar.gz)
   - Database migrations
   - PolicyPack updates
   - Release notes
   - Signature file (signed with the G.O.D.S release signing key)

2. The bundle is delivered to the institution via physical media or a one-way data diode

3. The institution verifies the signature before applying:
   ```bash
   gods-cli verify-bundle gods-update-v2.2.0.tar.gz --public-key gods-release.pub
   ```

4. The update is applied by the institution's administrators:
   ```bash
   gods-cli apply-update gods-update-v2.2.0.tar.gz --dry-run  # Preview
   gods-cli apply-update gods-update-v2.2.0.tar.gz            # Apply
   ```

The update process is atomic — it either fully succeeds or fully rolls back. Partial updates are not permitted.
