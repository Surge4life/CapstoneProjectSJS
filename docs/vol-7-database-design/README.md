# Volume VII — Database Design
## Every Table. Every Relationship. Every Audit Chain.

> The G.O.D.S data architecture is built around one principle: **nothing is ever truly deleted, and everything is auditable**. This volume documents the complete database design across all four divisions plus the platform core.

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
| [09](09-indexes.md) | Index Strategy |
| [10](10-retention-policies.md) | Retention Policies |
| [11](11-migrations.md) | Migration Strategy |

---

## Database Technology Stack

| Purpose | Technology | Why |
|---------|-----------|-----|
| Primary state | PostgreSQL | ACID, relational, mature |
| Event streaming | Apache Kafka | High-throughput, ordered, replayable |
| Immutable audit | Cassandra/WORM | Append-only, hash-chained, distributed |
| Full-text search | OpenSearch | Governance record search |
| Object storage | S3-compatible | Documents, attachments, model binaries |
| Cache | Redis | Session, rate limiting, temporary governance state |

---

## The Audit Principle

Every write operation in the G.O.D.S system produces an audit record. The audit record is:
1. Written to PostgreSQL (queryable, operational)
2. Published to Kafka (event stream, replayable)
3. Sealed in Cassandra with HMAC (immutable, hash-chained)
4. Included in a daily Merkle root (tamper-evident)

Deleting an audit record is architecturally impossible. Amending an audit record produces a new audit record that references the original.
