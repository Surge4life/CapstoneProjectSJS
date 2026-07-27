# Chapter 06 — Audit Records

## The GBS Audit Trail

Every governance decision creates an immutable audit record. The audit trail is the mechanism by which the constitutional promise of accountability is kept: every AI-informed decision that passed through G.O.D.S can be examined, verified, and challenged.

---

## The Dual-Write Architecture

Governance decisions are written to two places simultaneously:

### Write 1: PostgreSQL (Operational)

`governance.decisions` — the fast, queryable operational record. Used for:
- Compliance dashboards
- Oversight case management
- Real-time governance monitoring
- API queries (`GET /decisions/{id}`)

This record is mutable in one direction only: the `oversight_outcome` field can be updated when an oversight case resolves. The core decision fields (outcome, EVA scores, seal) can never be modified.

### Write 2: Cassandra (Immutable)

`governance_audit.decision_events` — the append-only, cryptographically sealed audit chain. Used for:
- Long-term auditability
- Audit chain integrity verification
- External audit reports
- Proof of governance record completeness

Once written, Cassandra records are permanent. There is no update operation. There is no delete operation. The record is forever.

---

## The Audit Record Structure

The Cassandra audit record for a governance decision:

```cql
CREATE TABLE governance_audit.decision_events (
    bucket_date     DATE,           -- Partition key: date of the event
    sequence_id     BIGINT,         -- Clustering key: monotonically increasing within day
    event_id        UUID,
    decision_id     UUID,
    model_id        UUID,
    operator_id     UUID,
    tenant_id       UUID,
    
    -- The core decision
    outcome         TEXT,           -- APPROVE | REVIEW | ESCALATE | BLOCK
    eva_scores      TEXT,           -- JSON: {ec, si, rc, fa, cc, sc, overall}
    policy_version  INT,
    reasoning       TEXT,
    decision_seal   TEXT,           -- HMAC-SHA256
    
    -- Chain integrity
    prev_record_hash TEXT,          -- SHA-256 of previous record in this bucket
    chain_hash      TEXT,           -- SHA-256 of this record's content
    
    -- Context
    input_hash      TEXT,           -- SHA-256 of model input
    output_category TEXT,
    jurisdiction    TEXT,
    governance_ms   INT,
    
    created_at      TIMESTAMPTZ,
    
    PRIMARY KEY ((bucket_date), sequence_id)
) WITH CLUSTERING ORDER BY (sequence_id ASC);
```

---

## The Hash Chain

Each audit record includes `prev_record_hash` — the SHA-256 of the previous record in the same day's bucket. This creates a hash chain:

```
Record 1: prev_hash = "0000...0000" (genesis)
           chain_hash = SHA256(all_fields)

Record 2: prev_hash = Record 1's chain_hash
           chain_hash = SHA256(all_fields including prev_hash)

Record 3: prev_hash = Record 2's chain_hash
           chain_hash = SHA256(all_fields including prev_hash)
```

To verify the chain: recompute each `chain_hash` and verify it matches the stored value; verify each `prev_hash` matches the previous record's `chain_hash`. Any tampering with a record breaks every subsequent hash in the chain — it's immediately detectable.

Daily Merkle roots are computed at midnight, sealing the day's bucket.

---

## Audit Record for Other Event Types

Governance decisions are not the only events in the audit chain. The complete list:

| Event Type | When Created |
|-----------|-------------|
| `GOVERNANCE.DECISION` | Every governance decision |
| `GOVERNANCE.OVERSIGHT_OPENED` | Every oversight case opened |
| `GOVERNANCE.OVERSIGHT_RESOLVED` | Every oversight case resolved |
| `GOVERNANCE.SLA_BREACH` | Every SLA deadline breach |
| `GOVERNANCE.POLICY_ACTIVATED` | PolicyPack activation |
| `GOVERNANCE.MODEL_SUSPENDED` | Model suspension |
| `GOVERNANCE.MODEL_CERTIFIED` | Model certification |
| `AUTH.LOGIN` | Every successful login |
| `AUTH.LOGOUT` | Every logout |
| `AUTH.PERMISSION_DENIED` | Every RBAC denial |
| `AUTH.ADMIN_ACTION` | Every gods_admin action |
| `DATA_CHANGE.DOCUMENT_UPLOADED` | Document upload |
| `DATA_CHANGE.DOCUMENT_DOWNLOADED` | Document download |
| `DATA_CHANGE.DOCUMENT_INTEGRITY_FAILURE` | Document tamper detection |
| `SYSTEM.AUDIT_CHAIN_ANOMALY` | Chain verification failure |
| `SYSTEM.CONFIGURATION_CHANGE` | Platform configuration change |

---

## Audit Record Access

| Role | Access Level |
|------|-------------|
| `gods_admin` | Full access — all events, all tenants |
| `external_auditor` | Read-only — all events, time-limited access |
| `compliance` | Read access — all events within scope |
| `operator` | Read-only — own model's governance decisions |
| `learner` | Read-only — decisions affecting own records |
| Other roles | No direct audit access |

Reading audit records is itself audited (`DATA_CHANGE.AUDIT_RECORD_ACCESSED`).
