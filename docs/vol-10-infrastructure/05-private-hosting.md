# Chapter 05 — Private Cloud and On-Premises Hosting

## When to Use Private Hosting

Private hosting (self-managed Kubernetes on bare metal or private cloud) is appropriate when:
- Data sovereignty requirements prohibit use of public cloud providers
- Air-gap requirements mandate no internet connectivity
- Regulatory mandates require on-premises data processing
- Scale economics favour owned infrastructure over per-unit cloud pricing
- Security posture requires full stack control

---

## Private Hosting Architecture

```
┌─────────────────────────────────────────────────┐
│                Organisation Network              │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │          Kubernetes Cluster               │   │
│  │                                          │   │
│  │  ┌─────────────┐  ┌───────────────────┐  │   │
│  │  │  gods-ns     │  │  gods-data-ns     │  │   │
│  │  │  (app layer) │  │  (data layer)     │  │   │
│  │  │              │  │                   │  │   │
│  │  │ platform-core│  │ postgres          │  │   │
│  │  │ eva engine   │  │ redis             │  │   │
│  │  │ udoc engine  │  │ kafka             │  │   │
│  │  │ gis engine   │  │ cassandra         │  │   │
│  │  │ gods engine  │  │ opensearch        │  │   │
│  │  └─────────────┘  └───────────────────┘  │   │
│  │                                          │   │
│  │  ┌─────────────────────────────────────┐ │   │
│  │  │  gods-ops-ns (operations)           │ │   │
│  │  │  prometheus  grafana  alertmanager  │ │   │
│  │  │  vault       step-ca  minio         │ │   │
│  │  └─────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  NGINX Ingress (external load balancer)  │   │
│  └──────────────────────────────────────────┘   │
│                            │                    │
└────────────────────────────┼────────────────────┘
                             │ HTTPS
                         External users
```

---

## Private Hosting Prerequisites

| Component | Minimum Specification |
|-----------|----------------------|
| Kubernetes nodes | 3 × (8 vCPU, 32 GB RAM, 500 GB SSD) |
| PostgreSQL storage | 1 TB SSD (with 3× replication) |
| Cassandra storage | 2 TB SSD per node (3 nodes) |
| OpenSearch storage | 500 GB SSD per node (3 nodes) |
| Network | 10 Gbps internal; 1 Gbps external |
| Load balancer | Hardware (F5) or software (MetalLB) |

These are minimum specifications for a production deployment supporting up to 100 concurrent users and 10,000 governance decisions per day.

---

## Secrets Management — HashiCorp Vault

Private deployments use HashiCorp Vault for secrets management:

```bash
# Vault setup (one-time)
vault server -config=/etc/vault/config.hcl

# Enable database secrets engine for PostgreSQL
vault secrets enable database
vault write database/config/gods-postgres \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://vault:{{password}}@postgres:5432/gods" \
  allowed_roles="platform-core"

# Create dynamic credentials role
vault write database/roles/platform-core \
  db_name=gods-postgres \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT gods_app TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"
```

Platform-core authenticates to Vault using Kubernetes service account tokens. Vault issues short-lived database credentials (1-hour TTL) that are automatically rotated. No long-lived database passwords in environment variables.

---

## Certificate Authority — step-ca

Private deployments use step-ca as an internal certificate authority:

```bash
# Initialize step-ca
step ca init --name="GODS Internal CA" \
  --dns="ca.gods.internal" \
  --address=":443" \
  --provisioner="admin@gods.internal"

# Issue certificate for platform-core
step ca certificate "platform-core.gods.internal" \
  platform-core.crt platform-core.key
```

All internal service-to-service communication uses mTLS with certificates from the internal CA. The CA certificate is distributed to all cluster nodes as a trusted root.

---

## Backup Strategy for Private Deployments

```bash
# Daily PostgreSQL backup
pg_dump -h postgres.gods-data-ns.svc.cluster.local \
  -U backup_user gods > /backup/gods-$(date +%Y%m%d).sql

# Daily Cassandra snapshot
nodetool snapshot governance_audit

# Daily OpenSearch snapshot (via snapshot API)
curl -X PUT "opensearch:9200/_snapshot/gods_backup/snapshot_$(date +%Y%m%d)" \
  -H "Content-Type: application/json" \
  -d '{"indices": "gods_corpus_*"}'

# Offsite replication (to DR site)
rsync -avz /backup/ dr-site:/backup/gods/
```

Backups are tested monthly via a restore drill — restore to an isolated environment and verify data integrity.
