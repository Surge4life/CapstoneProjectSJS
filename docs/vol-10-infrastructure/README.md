# Volume X — Infrastructure White Paper
## Production Deployment Architecture

> This volume documents the complete infrastructure architecture for the G.O.D.S ecosystem, from local development to air-gapped sovereign deployments. Every layer is documented: container orchestration, CI/CD, networking, security, high availability, and disaster recovery.

---

## Capstone live (2026-07-30)

**What is actually running:** Render free services + Neon ≤500MB.  
See [Chapter 13 — Render Deployment](13-render-deployment.md) (rewritten for honesty) and  
[`udoc-mvp/UDOC_LIVE_ENVIRONMENTS.md`](../../udoc-mvp/UDOC_LIVE_ENVIRONMENTS.md).

Chapters 02–12 describe **target** private / hybrid / air-gap tiers. Do not treat Kafka/Cassandra/HSM sections as Capstone live facts.

---

## Contents

| Chapter | Title |
|---------|-------|
| [01](01-overview.md) | Infrastructure Overview |
| [02](02-docker.md) | Docker & Container Strategy |
| [03](03-kubernetes.md) | Kubernetes Orchestration |
| [04](04-ci-cd.md) | CI/CD Pipeline |
| [05](05-private-hosting.md) | Private Hosting |
| [06](06-hybrid-cloud.md) | Hybrid Cloud Architecture |
| [07](07-air-gap.md) | Air-Gap Deployment |
| [08](08-disaster-recovery.md) | Disaster Recovery |
| [09](09-high-availability.md) | High Availability |
| [10](10-scaling.md) | Scaling Strategy |
| [11](11-monitoring-infra.md) | Monitoring & Observability |
| [12](12-security-infrastructure.md) | Infrastructure Security |
| [13](13-render-deployment.md) | Render + Neon (Current Capstone Production) |

---

## Deployment Tiers

The G.O.D.S infrastructure is designed to operate across four deployment tiers, from a single developer's machine to a nationally distributed sovereign network.

| Tier | Name | Hardware | Use Case |
|------|------|----------|----------|
| 0 | Local | Developer laptop | Development & testing |
| 1 | Cloud | Render / AWS / GCP | Pilot & early production (**Capstone is here**) |
| 2 | Private | Dedicated servers | Client enterprise deployments |
| 3 | Sovereign | UDOC hardware node | Air-gapped, national-grade |

All tiers run the same codebase. Configuration differs. The governance guarantees are identical in design; free-tier capacity limits what is proven live.
