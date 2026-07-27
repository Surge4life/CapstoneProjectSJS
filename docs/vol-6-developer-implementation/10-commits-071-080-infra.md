# Chapter 10 — Commits 071–080: Infrastructure & Edge Hardware

## Overview

This batch builds the infrastructure layer: Docker configuration, Kubernetes manifests, monitoring setup, hardware bringup, and the CI/CD pipeline.

---

## Commit 071: `[INFRA] ADD: Docker Compose development stack`

**What:** `infra/docker-compose.yml` — complete development environment:
- PostgreSQL 16 with schema initialisation
- Redis 7 for session store and governance cache
- Apache Kafka + Zookeeper for event bus
- Apache Cassandra for audit chain
- OpenSearch for vector + text search
- All services on internal bridge network `gods-network`

Volume mounts for persistent local development data.

---

## Commit 072: `[INFRA] ADD: PostgreSQL init scripts`

**What:** `infra/init-scripts/`:
- `01-schemas.sql` — creates all schemas (iam, governance, seths, madiba, ts, udoc, platform, intelligence, analytics, audit)
- `02-seed-roles.sql` — seeds default RBAC roles with their permission sets

These run automatically when the PostgreSQL Docker container first initialises.

---

## Commit 073: `[INFRA] ADD: Kubernetes manifests — platform-core`

**What:** `infra/k8s/platform-core/`:
- `deployment.yaml` — 3 replicas, rolling update, resource limits
- `service.yaml` — ClusterIP service + LoadBalancer for external access
- `hpa.yaml` — HPA: min 3, max 10 pods, CPU 70% + custom governance latency metric
- `ingress.yaml` — NGINX ingress with mTLS and rate limiting
- `secrets.yaml` — template for secret injection

---

## Commit 074: `[INFRA] ADD: Kubernetes manifests — governance engines`

**What:** `infra/k8s/governance-engines/`:
- EVA engine deployment (2 replicas, stateless)
- UDOC engine deployment (2 replicas)
- GIS engine deployment (2 replicas)
- G.O.D.S engine deployment (2 replicas)
- Internal ClusterIP services (not exposed externally)
- Network policies: only platform-core can call governance engines

---

## Commit 075: `[INFRA] ADD: Monitoring stack — Prometheus + Grafana + Alertmanager`

**What:** `infra/monitoring/`:
- Prometheus configuration with all scrape targets
- Alert rules for governance failures, SLA breaches, security events
- Grafana dashboard JSON files (5 dashboards)
- Alertmanager configuration (PagerDuty + Slack routing)

---

## Commit 076: `[INFRA] ADD: CI/CD pipeline — GitHub Actions`

**What:** `infra/ci/github-actions/`:
- `ci.yml` — runs on every PR: lint, type-check, unit tests, integration tests, smoke tests
- `deploy-render.yml` — deploys to Render on push to `main` (after CI passes)
- `security-scan.yml` — weekly dependency audit + SAST scan

Required status checks configured on `main` branch — no merge without CI pass.

---

## Commit 077: `[EDGE] ADD: hw-bringup boot sequence and self-test`

**What:** `hw-bringup/` complete implementation:
- GRUB configuration for UDOC node boot
- `run_selftest.py` — hardware probe orchestration
- Emulation shims (FPGA, HSM, NIC) for development testing
- Systemd service units for UDOC boot ordering
- `run_emulated.sh` — full emulated boot test

---

## Commit 078: `[EDGE] ADD: Hardware driver contracts and emulation`

**What:** `hw-bringup/drivers/`:
- FPGA PCIe interface contract and emulation
- HSM PKCS#11 client with SoftHSM2 emulation
- NIC sovereignty hook contract and software emulation
- Interface contracts documented as Python ABCs (abstract base classes)

---

## Commit 079: `[INFRA] ADD: Render deployment configuration`

**What:** `render.yaml` — complete Render cloud deployment:
- `platform-core` web service (Python, Dockerfile)
- `gods-governance-eva` web service
- `gods-governance-udoc` web service
- `gods-governance-gis` web service
- `gods-governance-gods` web service
- All frontend apps as static sites
- Environment variable references (not values)

---

## Commit 080: `[INFRA] ADD: Air-gap deployment manifests`

**What:** `infra/k8s/air-gap/`:
- MinIO deployment (S3-compatible object storage)
- HashiCorp Vault deployment (secrets management)
- Step-CA deployment (internal certificate authority)
- Local container registry configuration
- Air-gap network policies (no egress allowed)

Air-gap deployment guide: Volume X, Chapter 07.
