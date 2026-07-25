# Chapter 07 — Immutable Audit Chain

## The Architecture of Permanence

The G.O.D.S audit chain is the technical implementation of the Immutable Audit constitutional pillar. It provides a tamper-evident, cryptographically verifiable record of every significant event in the system's history.

---

## The Three-Layer Audit Stack

### Layer 1: PostgreSQL Audit Index (`audit.audit_refs`)

This is the queryable layer. It is optimised for fast lookup, filtering, and joining against operational tables.

```sql
CREATE TABLE audit.audit_refs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type      VARCHAR(100) NOT NULL,
    event_category  VARCHAR(50) NOT NULL,
    resource_type   VARCHAR(100) NOT NULL,
    resource_id     UUID,
    actor_id        UUID REFERENCES iam.users(id),
    actor_role      VARCHAR(100),
    tenant_id       UUID REFERENCES platform.tenants(id),
    jurisdiction    VARCHAR(10),
    
    -- Hash chain fields
    sequence_num    BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
    previous_hash   VARCHAR(64) NOT NULL,
    event_hash      VARCHAR(64) NOT NULL,  -- SHA256(event content)
    chain_hash      VARCHAR(64) NOT NULL,  -- SHA256(event_hash + previous_hash)
    hmac_seal       TEXT NOT NULL,         -- HMAC-SHA256(chain_hash, HSM_key)
    
    -- Payload
    event_summary   JSONB NOT NULL,        -- Human-readable summary
    cassandra_ref   VARCHAR(255),          -- Reference to Cassandra record
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
    -- No updated_at — audit records are immutable
    -- No deleted_at — audit records cannot be deleted
);

-- Append-only enforcement via trigger
CREATE OR REPLACE FUNCTION enforce_audit_immutability()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' OR TG_OP = 'DELETE' THEN
        RAISE EXCEPTION 'Audit records are immutable. UPDATE and DELETE are not permitted on audit.audit_refs.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_immutability
    BEFORE UPDATE OR DELETE ON audit.audit_refs
    FOR EACH ROW EXECUTE FUNCTION enforce_audit_immutability();
```

---

### Layer 2: Cassandra WORM Storage

The Cassandra layer provides the permanent, distributed, WORM storage of complete event payloads.

**Table schema (Cassandra CQL):**
```cql
CREATE TABLE gods_audit.events (
    tenant_id       UUID,
    event_date      DATE,
    sequence_num    BIGINT,
    event_id        UUID,
    event_type      TEXT,
    event_category  TEXT,
    resource_type   TEXT,
    resource_id     UUID,
    actor_id        UUID,
    jurisdiction    TEXT,
    payload         TEXT,              -- Full JSON payload
    previous_hash   TEXT,
    event_hash      TEXT,
    chain_hash      TEXT,
    hmac_seal       TEXT,
    created_at      TIMESTAMP,
    
    PRIMARY KEY ((tenant_id, event_date), sequence_num, event_id)
) WITH compaction = { 'class': 'LeveledCompactionStrategy' }
  AND gc_grace_seconds = 0             -- Never tombstone (WORM)
  AND default_time_to_live = 0;        -- Never expire
```

Cassandra's append-only semantics at the application level, combined with the `gc_grace_seconds = 0` and no TTL, ensures that written records cannot be made to disappear.

---

### Layer 3: Merkle Root (`audit.merkle_roots`)

A daily Merkle root provides a tamper-evident summary of all audit records for that day.

```sql
CREATE TABLE audit.merkle_roots (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    root_date       DATE NOT NULL UNIQUE,
    merkle_root     VARCHAR(64) NOT NULL,
    record_count    BIGINT NOT NULL,
    first_seq       BIGINT NOT NULL,
    last_seq        BIGINT NOT NULL,
    computed_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    computed_by     VARCHAR(100) NOT NULL DEFAULT 'system',
    published       BOOLEAN NOT NULL DEFAULT false,
    published_at    TIMESTAMPTZ,
    publication_url TEXT           -- URL where this root has been published externally
);
```

---

## The Hash Chain Verification Algorithm

To verify the integrity of the audit chain from record A to record B:

```python
def verify_chain_segment(start_seq: int, end_seq: int) -> VerificationResult:
    records = audit_refs.fetch_by_sequence_range(start_seq, end_seq)
    
    for i, record in enumerate(records):
        if i == 0:
            # First record in segment — verify against its declared previous_hash
            expected_previous = record.previous_hash
        else:
            # Each record's previous_hash must equal the prior record's chain_hash
            expected_previous = records[i-1].chain_hash
            if record.previous_hash != expected_previous:
                return VerificationResult(
                    valid=False,
                    broken_at=record.sequence_num,
                    reason="Hash chain broken: previous_hash mismatch"
                )
        
        # Recompute the chain hash
        recomputed_hash = sha256(record.event_hash + record.previous_hash)
        if recomputed_hash != record.chain_hash:
            return VerificationResult(
                valid=False,
                broken_at=record.sequence_num,
                reason="Hash chain broken: recomputed chain_hash mismatch"
            )
        
        # Verify the HMAC seal
        if not hmac_verify(record.chain_hash, record.hmac_seal, hsm_public_key):
            return VerificationResult(
                valid=False,
                broken_at=record.sequence_num,
                reason="HMAC seal verification failed"
            )
    
    return VerificationResult(valid=True, records_verified=len(records))
```

---

## What a Tampered Record Looks Like

If any audit record is modified after writing:

1. The `event_hash` will no longer match the hash of the event content
2. The `chain_hash` will no longer match `SHA256(event_hash + previous_hash)`
3. The HMAC seal will no longer verify against the `chain_hash`
4. Every subsequent record's `previous_hash` will not match the modified record's `chain_hash`

A single modification to one record is detectable as a broken chain from that point forward. There is no way to modify a record without either breaking the chain (detectable) or re-generating every subsequent hash (requires the HSM key — if the key is in hardware, this is physically impossible without access to the HSM device).

---

## External Verification

The daily Merkle root is designed to be publishable to an external transparency log. When published, any party can verify that a specific audit record existed in the official G.O.D.S audit chain as of a specific date, without access to the G.O.D.S database.

This is the technical foundation of the G.O.D.S governance assurance — not just that audit records exist, but that their existence can be independently verified.
