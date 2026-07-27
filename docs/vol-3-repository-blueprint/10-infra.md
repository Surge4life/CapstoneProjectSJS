# Chapter 10 — infra

## What Lives Here

`infra/` contains all infrastructure configuration — Docker, Kubernetes, Terraform, monitoring, and CI/CD definitions. If it configures how the software runs (rather than what the software does), it belongs here.

---

## Directory Structure

```
infra/
├── docker-compose.yml         Full development stack
├── docker-compose.prod.yml    Production overrides (for self-hosted)
│
├── k8s/                       Kubernetes manifests
│   ├── namespace.yaml
│   ├── platform-core/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── hpa.yaml           Horizontal Pod Autoscaler
│   │   ├── ingress.yaml
│   │   └── secrets.yaml       Template (values injected by CI)
│   ├── governance-engines/
│   │   ├── eva-deployment.yaml
│   │   ├── udoc-deployment.yaml
│   │   ├── gis-deployment.yaml
│   │   └── gods-deployment.yaml
│   ├── databases/
│   │   ├── postgres.yaml
│   │   ├── redis.yaml
│   │   ├── kafka.yaml
│   │   ├── cassandra.yaml
│   │   └── opensearch.yaml
│   ├── network-policies/
│   │   ├── default-deny.yaml
│   │   └── allow-rules.yaml
│   └── air-gap/               Air-gap specific overrides
│       ├── minio.yaml          S3-compatible storage
│       ├── vault.yaml          HashiCorp Vault
│       └── step-ca.yaml       Self-hosted certificate authority
│
├── terraform/                 Infrastructure as Code (cloud deployments)
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       ├── vpc/
│       ├── kubernetes/
│       └── databases/
│
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── alerts/
│   │       ├── governance.yml
│   │       ├── infrastructure.yml
│   │       └── security.yml
│   ├── grafana/
│   │   ├── datasources/
│   │   └── dashboards/
│   │       ├── governance-overview.json
│   │       ├── api-performance.json
│   │       ├── audit-chain-health.json
│   │       └── security-posture.json
│   └── alertmanager/
│       └── alertmanager.yml
│
├── ci/
│   ├── github-actions/
│   │   ├── ci.yml             Test + lint on every PR
│   │   ├── deploy-render.yml  Deploy to Render on main push
│   │   └── security-scan.yml  Dependency and SAST scanning
│   └── scripts/
│       ├── run-tests.sh
│       ├── run-smoke-tests.sh
│       └── deploy.sh
│
├── init-scripts/              PostgreSQL initialisation scripts
│   ├── 01-schemas.sql         Create all schemas
│   └── 02-seed-roles.sql      Seed default RBAC roles
│
└── SECURITY.md                Infrastructure security documentation
```

---

## Key Files

### `docker-compose.yml`

The development stack. Starts PostgreSQL, Redis, Kafka, Zookeeper, Cassandra, and OpenSearch with reasonable development defaults. Not for production — no TLS, no auth hardening.

```bash
cd infra
docker compose up -d           # Start all infrastructure services
docker compose down            # Stop all services
docker compose down -v         # Stop and delete all data volumes
```

### `init-scripts/`

SQL scripts run automatically when the PostgreSQL container first starts. They create the database schemas and seed the default RBAC roles. Idempotent — safe to run multiple times.

### `monitoring/`

All monitoring configuration. Prometheus scrape configs, alerting rules, Grafana dashboards. Import dashboards by pointing Grafana at the `dashboards/` directory.

### `ci/`

CI/CD pipeline definitions. GitHub Actions workflows for:
- Running tests on every PR
- Deploying to Render on push to `main`
- Weekly security scans

---

## Infrastructure Ownership

The `infra/` directory is maintained by the developer or team responsible for operations. Changes to:
- Kubernetes manifests require a peer review
- Alerting rules require a compliance review
- Security configurations require a security review
- Network policies require explicit written justification in the PR description
