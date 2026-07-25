# Volume II — System Architecture
## Every Service. Every Engine. Every Module.

> This volume documents the complete technical architecture of the G.O.D.S ecosystem. Every service is described with its purpose, its responsibilities, its interfaces, and its position in the governance chain.

---

## Contents

| Chapter | Title |
|---------|-------|
| [01](01-overview.md) | Architecture Overview & Service Map |
| [02](02-authentication.md) | Authentication Service |
| [03](03-rbac.md) | Role-Based Access Control (RBAC) |
| [04](04-udoc-engine.md) | UDOC Engine |
| [05](05-gbs-runtime.md) | GBS Runtime |
| [06](06-gods-intelligence.md) | G.O.D.S Intelligence |
| [07](07-corpus-engine.md) | Corpus Engine |
| [08](08-evidence-engine.md) | Evidence Engine |
| [09](09-audit-engine.md) | Audit Engine |
| [10](10-notification-engine.md) | Notification Engine |
| [11](11-document-engine.md) | Document Engine |
| [12](12-reporting-engine.md) | Reporting Engine |
| [13](13-franchise-engine.md) | Franchise Engine |
| [14](14-seths-engine.md) | SETHS Engine |
| [15](15-employer-engine.md) | Employer Engine |
| [16](16-learner-engine.md) | Learner Engine |
| [17](17-certification-engine.md) | Certification Engine |
| [18](18-deployment-engine.md) | Deployment Engine |
| [19](19-monitoring-engine.md) | Monitoring Engine |

---

## The Five Hardware Planes

The software architecture maps directly onto the five planes of the UDOC hardware specification:

| Plane | Focus | Software Boundary |
|-------|-------|-------------------|
| 1 — Embedded Governance Fabric | Low-latency, fail-closed | `udoc-agent`, `udoc-sidecar`, `udoc-gateway`, `udoc-edge` |
| 2 — Ingestion & Control | Fast NVMe, mTLS | `platform-core` ingress, auth, mTLS |
| 3 — Governance & Processing | CPU/RAM balanced | `platform-core` FastAPI + `governance-engines` |
| 4 — Immutable Data Operations | Storage endurance | PostgreSQL + Kafka + Cassandra/WORM + OpenSearch |
| 5 — Security & Operations | Trust isolation | HSM/TPM (PKCS#11), key hierarchy, bastion, SIEM |
