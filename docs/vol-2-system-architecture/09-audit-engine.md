# Chapter 09 — Audit Engine

## Purpose

The Audit Engine is the immutable record-keeping system of the G.O.D.S ecosystem. Every governance decision, every state change, every significant system event is written to the audit chain through this engine. The audit chain cannot be altered, truncated, or deleted.

The Audit Engine is the most critical service in the G.O.D.S stack. If it fails, the system fails closed.

---

## Location

- **Router:** `platform-core/app/routers/audit.py`
- **Router:** `platform-core/app/routers/lineage.py`
- **Service:** `platform-core/app/services/audit_writer.py`
- **Event bus:** `platform-core/app/services/event_bus.py`

---

## The Audit Chain Architecture

```
Event source (any service)
  ↓
audit_writer.write(event)
  ↓
1. Generate event_id (UUID)
2. Compute previous_hash (last record's hash)
3. Compute current_hash = SHA256(event_id + timestamp + payload + previous_hash)
4. Sign: HMAC-SHA256(current_hash, HSM_key)
5. Write to PostgreSQL (AuditRef table — fast query)
6. Publish to Kafka (audit.events topic)
  ↓
Kafka consumer (async, separate process)
  ↓
7. Write to Cassandra/WORM (permanent, immutable)
8. Update running Merkle tree (for daily Merkle root)
  ↓
Daily scheduled job (APScheduler)
  ↓
9. Compute daily Merkle root
10. Write Merkle root to PostgreSQL (MerkleRoot table)
11. Publish Merkle root to public log (if configured)
```

---

## Event Types

Every event in the G.O.D.S system has a declared type. The event type determines:
- Which Cassandra partition it is stored in
- What fields are required
- What RBAC roles can query it
- How long it is retained in the queryable PostgreSQL layer (indefinitely in Cassandra)

| Event Category | Examples | Retention (PostgreSQL) |
|---------------|---------|----------------------|
| `GOVERNANCE` | Decisions, GBS checks, EVA scores | 7 years |
| `AUTHENTICATION` | Login, logout, token refresh, failures | 2 years |
| `DATA_CHANGE` | Record creates, updates | 7 years |
| `ADMINISTRATIVE` | Role changes, policy updates, suspensions | 7 years |
| `SYSTEM` | Service starts, failures, config changes | 1 year |
| `INTELLIGENCE` | Query requests, responses, corpus updates | 3 years |

All events are permanent in Cassandra regardless of PostgreSQL retention.

---

## The Lineage Router

The `lineage` router provides **provenance tracking** — the ability to trace any data item back through its complete history of changes.

### GET /lineage/{resource_type}/{resource_id}

Returns the complete change history for a specific resource.

**Response:**
```json
{
  "resource_type": "Decision",
  "resource_id": "uuid",
  "lineage": [
    {
      "event_id": "uuid",
      "timestamp": "datetime",
      "event_type": "GOVERNANCE.DECISION_CREATED",
      "actor": { "id": "uuid", "role": "operator" },
      "changes": { "status": { "from": null, "to": "BLOCK" } },
      "hash": "sha256-hash",
      "verified": true
    },
    {
      "event_id": "uuid",
      "timestamp": "datetime",
      "event_type": "GOVERNANCE.OVERSIGHT_CASE_OPENED",
      "actor": { "id": "system", "role": "system" },
      "changes": { "oversight_case_id": "uuid" },
      "hash": "sha256-hash",
      "verified": true
    }
  ],
  "chain_integrity": "VERIFIED",
  "merkle_inclusion_proof": "base64-encoded-proof"
}
```

The `chain_integrity: VERIFIED` status means every hash in the chain has been re-verified against its predecessor and the HMAC signature.

---

## Merkle Inclusion Proofs

Any audit record can be proven to exist in the official audit chain using a Merkle inclusion proof. This proof:
1. Identifies the specific record's leaf hash
2. Provides the sibling hashes needed to reconstruct the path to the daily Merkle root
3. Provides the official Merkle root for that day

A third party can verify the proof independently without access to the G.O.D.S database, using only:
- The audit record content
- The inclusion proof
- The publicly published daily Merkle root

This makes the audit chain **externally verifiable**.

---

## What Triggers an Audit Record

Every one of these actions produces an audit record. This list is exhaustive — if an action is not on this list and it affects system state, adding it to the audit writer is a required code change, not an optional enhancement.

- User authentication (success and failure)
- Role assignment and revocation
- Policy rule creation, update, or activation
- AI model registration, certification, suspension, resumption, decommissioning
- Governance decision (every decision, regardless of outcome)
- OversightCase creation, assignment, and resolution
- Document upload and download
- Cross-jurisdiction data flow authorisation
- Administrator action (any admin endpoint)
- Service configuration change
- Compliance scan result
- System startup and shutdown
- Scheduled job execution
