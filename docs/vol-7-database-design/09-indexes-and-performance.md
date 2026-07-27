# Chapter 09 — Indexes and Performance

## Index Strategy

Indexes are not added speculatively. Every index in the G.O.D.S schema exists to serve a specific query pattern that has been identified from the application code. This chapter documents the major indexes and the queries they serve.

---

## Index Philosophy

**Rule 1: Every foreign key has an index.** Foreign keys without indexes cause sequential scans on JOIN operations. All foreign keys are indexed by default.

**Rule 2: Every filter column in a hot query has an index.** If a column appears in a `WHERE` clause on a frequently executed query, it has an index.

**Rule 3: Partial indexes for common filtered queries.** If a query always filters on a specific value (e.g., `WHERE status = 'pending'`), a partial index covering only that subset is more efficient than a full index.

**Rule 4: No redundant indexes.** If an index on `(a, b)` exists, a separate index on `(a)` alone is redundant (the multi-column index satisfies queries on `a` alone). Redundant indexes waste storage and slow writes.

**Rule 5: Indexes are reviewed at every migration.** When a new query is added to the application, the team checks whether the existing indexes cover it.

---

## Critical Indexes (Governance Hot Path)

These indexes serve the governance decision path — the most latency-sensitive queries in the system.

```sql
-- Model lookup by ID (called on every governance request)
-- Covered by primary key — no additional index needed

-- Active model check (governance pre-flight)
CREATE UNIQUE INDEX udoc_ai_models_active_by_operator_idx
    ON udoc.ai_models(operator_id, model_name, model_version)
    WHERE status NOT IN ('revoked', 'decommissioned');

-- Governance decisions for a model (dashboard)
CREATE INDEX governance_decisions_model_idx
    ON governance.decisions(model_id, created_at DESC);

-- Open oversight cases (SLA monitoring hot query)
CREATE INDEX governance_oversight_open_idx
    ON governance.oversight_cases(assigned_to, review_deadline)
    WHERE status NOT IN ('resolved', 'escalated');

-- Policy pack version lookup (called on every decision)
CREATE UNIQUE INDEX governance_policy_packs_active_idx
    ON governance.policy_packs(tenant_id)
    WHERE status = 'active';
```

---

## SETHS Performance Indexes

```sql
-- Learner opportunity search (most common SETHS query)
CREATE INDEX seths_opportunities_active_search_idx
    ON seths.opportunities(province, nqf_level_required, remote_ok, status)
    WHERE status = 'active';

-- Application pipeline (employer view)
CREATE INDEX seths_applications_employer_idx
    ON seths.applications(opportunity_id, status, created_at DESC);

-- Learner's own applications (learner view)
CREATE INDEX seths_applications_learner_idx
    ON seths.applications(learner_id, status, created_at DESC);

-- Document lookup by learner
CREATE INDEX seths_documents_learner_type_idx
    ON seths.documents(learner_id, document_type, created_at DESC)
    WHERE deleted_at IS NULL;
```

---

## Audit Chain Indexes (Cassandra)

Cassandra's indexes work differently from PostgreSQL. The audit chain's primary query patterns are:

```cql
-- Fetch a specific record (for audit inspection)
SELECT * FROM governance_audit.decision_events
WHERE bucket_date = '2025-01-15'
AND event_id = ?;                    -- Covered by partition + clustering key

-- Verify chain for a date range
SELECT * FROM governance_audit.decision_events
WHERE bucket_date IN ('2025-01-15', '2025-01-16', ...)
ORDER BY sequence_id ASC;           -- Covered by partition + clustering key

-- Lookup by model_id (secondary index — use sparingly)
CREATE INDEX ON governance_audit.decision_events(model_id);
-- Note: Secondary indexes in Cassandra are expensive at scale.
-- For frequent model-scoped queries, materialise a separate table:

CREATE TABLE governance_audit.model_decision_summary (
    model_id        UUID,
    bucket_date     DATE,
    decision_count  INT,
    block_count     INT,
    approve_count   INT,
    PRIMARY KEY ((model_id), bucket_date)
) WITH CLUSTERING ORDER BY (bucket_date DESC);
```

---

## Query Explain Plans (Key Queries)

### Governance Dashboard — Open Oversight Cases

```sql
EXPLAIN ANALYZE
SELECT oc.id, oc.decision_id, oc.review_deadline, u.email
FROM governance.oversight_cases oc
JOIN iam.users u ON u.id = oc.assigned_to
WHERE oc.status NOT IN ('resolved', 'escalated')
  AND oc.tenant_id = $1
ORDER BY oc.review_deadline ASC
LIMIT 50;

-- Uses: governance_oversight_open_idx (partial)
-- Expected: Index Scan → Nested Loop → Index Scan on users
-- Target: < 5ms at 10,000 open cases
```

### SETHS — Opportunity Search

```sql
EXPLAIN ANALYZE
SELECT id, title, employer_id, nqf_level_required, salary_min, salary_max
FROM seths.opportunities
WHERE status = 'active'
  AND province = $1
  AND nqf_level_required >= $2
  AND nqf_level_required <= $3
ORDER BY created_at DESC
LIMIT 20;

-- Uses: seths_opportunities_active_search_idx
-- Target: < 10ms at 100,000 active opportunities
```

---

## Connection Pooling

G.O.D.S uses PgBouncer in transaction-mode pooling:

| Service | Pool Size | Notes |
|---------|----------|-------|
| platform-core | 20 connections per pod | 3 pods = 60 total connections |
| Analytics engine | 5 connections | Read-heavy, separate pool |
| Governance engines | 5 connections each | Lightweight DB use |

PgBouncer configuration in `infra/k8s/databases/pgbouncer.yaml`. PostgreSQL `max_connections` set to 200 (leaves headroom for admin connections).

---

## Slow Query Monitoring

```sql
-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slow queries
SELECT query, calls, total_time/calls as avg_ms, rows/calls as avg_rows
FROM pg_stat_statements
WHERE total_time/calls > 50   -- Queries averaging > 50ms
ORDER BY total_time/calls DESC
LIMIT 20;
```

Any query averaging > 50ms on the governance hot path is an incident. Queries > 100ms on non-hot-path endpoints are a performance improvement target.
