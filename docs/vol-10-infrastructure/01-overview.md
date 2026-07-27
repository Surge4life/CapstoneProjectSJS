# Chapter 01 — Infrastructure Overview

## The G.O.D.S Infrastructure Philosophy

Infrastructure for the G.O.D.S ecosystem is governed by the same constitutional principles as the application it supports. The infrastructure must be:

- **Auditable** — every infrastructure change is tracked
- **Sovereign** — control of the infrastructure is held by the operator, not by a cloud provider
- **Resilient** — the governance platform must not have single points of failure
- **Portable** — deployable to cloud, private data centre, or air-gapped network
- **Transparent** — the configuration is defined as code, not applied manually

---

## Infrastructure Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Compute | Docker / Kubernetes | Container orchestration |
| Application DB | PostgreSQL 16 | Operational data |
| Session store | Redis 7 | Sessions, token revocation, policy cache |
| Event bus | Apache Kafka | Asynchronous event streaming |
| Audit chain | Apache Cassandra | Immutable append-only event log |
| Search / vectors | OpenSearch | Corpus retrieval (text + vector) |
| Object storage | S3-compatible (AWS S3 / MinIO) | Document and file storage |
| Secrets | HashiCorp Vault (self-hosted) / Render secrets | Secrets management |
| Certificate authority | Let's Encrypt (cloud) / step-ca (private) | TLS certificates |
| Monitoring | Prometheus + Grafana + Alertmanager | Metrics, dashboards, alerting |
| Tracing | OpenTelemetry → Jaeger or Tempo | Distributed request tracing |
| CI/CD | GitHub Actions | Automated test and deploy pipeline |

---

## Deployment Target Matrix

| Feature | Local Dev | Render (Cloud) | Kubernetes (Private) | Air-Gap |
|---------|----------|----------------|---------------------|---------|
| PostgreSQL | Docker | Render PostgreSQL | Kubernetes StatefulSet | Kubernetes StatefulSet |
| Redis | Docker | Render Redis | Kubernetes StatefulSet | Kubernetes StatefulSet |
| Kafka | Docker | Render private service | Kubernetes StatefulSet | Kubernetes StatefulSet |
| Cassandra | Docker | Render private service | Kubernetes StatefulSet | Kubernetes StatefulSet |
| OpenSearch | Docker | Render private service | Kubernetes StatefulSet | Kubernetes StatefulSet |
| Object storage | Local MinIO | AWS S3 | MinIO or cloud S3 | MinIO |
| TLS | Disabled | Render (automatic) | cert-manager + Let's Encrypt | step-ca (internal CA) |
| Secrets | .env file | Render secrets | HashiCorp Vault | HashiCorp Vault |
| Monitoring | Optional | Render metrics | Prometheus stack | Prometheus stack |

---

## Service Dependencies Map

```
                    ┌──────────────────────────┐
                    │     platform-core         │
                    │    (FastAPI backend)       │
                    └──┬───────────────────┬────┘
                       │                   │
           ┌───────────┴──────────┐  ┌─────┴────────────────┐
           │  governance-engines  │  │  data layer           │
           │  eva / udoc / gis    │  │  postgres redis kafka  │
           │  gods               │  │  cassandra opensearch  │
           └──────────────────────┘  └────────────────────────┘
                                              │
                                   ┌──────────┴──────────┐
                                   │  object storage      │
                                   │  S3 / MinIO          │
                                   └──────────────────────┘
```

All inter-service communication within the Kubernetes cluster is over internal ClusterIP services. Only `platform-core` is exposed externally (via the Ingress controller).

---

## Network Segmentation

```
Internet
    ↓ HTTPS (443)
NGINX Ingress (TLS termination, rate limiting, WAF rules)
    ↓ HTTP (internal)
platform-core ClusterIP
    ↓ HTTP (internal, ClusterIP only)
governance-engines (eva, udoc, gis, gods)
    ↓ Connection pooling
Data layer (postgres, redis, kafka, cassandra, opensearch)
```

**Network policy enforcement:** Kubernetes NetworkPolicy objects enforce zero-trust networking within the cluster. A pod that does not have an explicit allow rule cannot communicate with any other pod.

---

## Infrastructure Ownership and Change Control

All infrastructure is defined as code in `infra/`. Changes to infrastructure configuration follow the same review process as application code:

| Change Type | Review Required | Approvers |
|-------------|----------------|-----------|
| Monitoring alert rules | Peer review | Developer + compliance |
| Network policy changes | Security review | Developer + security |
| Kubernetes resource limits | Peer review | Developer |
| Database configuration | DBA review | Developer + DBA |
| Security configuration | Security review | Senior developer |
| New infrastructure service | Architecture review | Lead + infrastructure |
