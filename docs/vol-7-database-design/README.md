# Volume VII — Database Design
## Every Table. Every Relationship. Every Audit Chain.

> The G.O.D.S data architecture is built around one principle: **nothing is ever truly deleted, and everything is auditable**. This volume documents the complete database design across all four divisions plus the platform core.

**Capstone honesty:** live state is **Neon PostgreSQL ≤500MB**. Kafka, Cassandra/WORM, OpenSearch, Redis, and S3 in the stack table are **target** components unless a chapter states they are live.

---

## Contents

| Chapter | Title |
|---------|-------|
| [01](01-schema-overview.md) | Schema Overview & Data Strategy |
| [02](02-core-tables.md) | Core Tables (Users, Auth, RBAC, Tenants) |
| [03](03-udoc-tables.md) | UDOC Tables (Registry, Decisions, Audit) |
| [04](04-seths-tables.md) | SETHS Tables (Learners, Employers, Applications) |
| [05](05-madiba-tables.md) | MADIBA Tables (Capital, Milestones, Investors) |
| [06](06-ts-tables.md) | TS Tables (Projects, SPVs, Partners) |
| [07](07-audit-chain.md) | Immutable Audit Chain (WORM + Merkle) |
| [08](08-event-tables.md) | Event Tables (Kafka → PostgreSQL bridge) |
| [09](09-indexes-and-performance.md) | Index Strategy |
| [10](10-retention-policies.md) | Retention Policies |
| [11](11-migrations.md) | Migration Strategy |

---

## Database Technology Stack

| Purpose | Technology | Why | Capstone live |
|---------|-----------|-----|---------------|
| Primary state | PostgreSQL | ACID, relational, mature | **Yes — Neon** |
| Event streaming | Apache Kafka | High-throughput, ordered, replayable | Designed |
| Immutable audit | Cassandra/WORM | Append-only, hash-chained, distributed | Designed (Neon rows today) |
| Full-text search | OpenSearch | Governance record search | Designed |
| Object storage | S3-compatible | Documents, attachments, model binaries | Designed |
| Cache | Redis | Session, rate limiting, temporary governance state | Designed |

---

## The Audit Principle

Every write operation in the G.O.D.S system produces an audit record. The audit record is:
1. Written to PostgreSQL (queryable, operational) — **live on Neon**
2. Published to Kafka (event stream, replayable) — designed
3. Sealed in Cassandra with HMAC (immutable, hash-chained) — designed
4. Included in a daily Merkle root (tamper-evident) — designed

Deleting an audit record is architecturally impossible. Amending an audit record produces a new audit record that references the original.
