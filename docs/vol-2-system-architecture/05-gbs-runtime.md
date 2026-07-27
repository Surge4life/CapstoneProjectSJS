# Chapter 05 — GBS Runtime (Service Layer)

## Purpose

This chapter documents the GBS Runtime as a *service* within `platform-core` — specifically the `gbs_engine` service that orchestrates the governance path. Volume V covers the constitutional doctrine and rules; this chapter covers the implementation.

---

## Location

- **Service:** `platform-core/app/services/gbs_engine.py`
- **Service:** `platform-core/app/services/governance_bridge.py`
- **External:** `governance-engines/` (EVA, UDOC, GIS engines called over HTTP)

---

## Service Responsibilities

The `gbs_engine` service is the in-process coordinator. It:

1. Validates the incoming governance request (schema, model status, jurisdiction)
2. Calls the EVA engine for 6-dimensional scoring
3. Applies the in-memory PolicyPack rules (policy engine)
4. Calls the UDOC Orchestrator for sovereignty + FSM enforcement
5. Produces the final outcome and reasoning
6. Seals the decision (calls `key_service` for HMAC)
7. Persists the `DecisionRecord`
8. Publishes the event to Kafka

All of this happens within the 50ms target. The steps are designed to minimize blocking I/O — EVA is called asynchronously, and database/Kafka writes are fire-and-forget.

---

## The Policy Pack Cache

The PolicyPack is loaded from the database at service startup and cached in memory. This makes rule evaluation O(n) in memory with no database round-trip per decision.

Cache invalidation: when a compliance officer activates a new PolicyPack version, a cache invalidation event is published to Kafka. Every `platform-core` instance subscribes to this event and reloads the PolicyPack.

```python
# Simplified in-memory policy cache
class PolicyCache:
    _current: PolicyPack | None = None
    _version: int = 0

    async def get(self) -> PolicyPack:
        if self._current is None:
            await self.reload()
        return self._current

    async def reload(self):
        self._current = await db.fetch_active_policy_pack()
        self._version = self._current.version
```

---

## Decision Record Structure

The `DecisionRecord` written by the GBS Runtime:

```python
class DecisionRecord(Base):
    __tablename__ = "decisions"
    __table_args__ = {"schema": "governance"}

    id: UUID
    model_id: UUID
    operator_id: UUID
    tenant_id: UUID
    request_id: UUID            # Client-supplied idempotency key
    input_hash: str             # SHA-256 of model input
    output_hash: str | None     # SHA-256 of model output (for APPROVE only)
    output_category: str

    # EVA scores
    eva_ec_score: Decimal
    eva_si_score: Decimal
    eva_rc_score: Decimal
    eva_fa_score: Decimal
    eva_cc_score: Decimal
    eva_sc_score: Decimal
    eva_overall: Decimal

    outcome: str                # APPROVE | REVIEW | ESCALATE | BLOCK | ERROR
    reasoning: str              # Human-readable explanation
    decision_seal: str          # HMAC-SHA256
    policy_version: int         # GV version active at decision time
    governance_ms: int          # Path latency
    created_at: datetime
    audit_ref_id: UUID
```

---

## Idempotency

The `/decisions` endpoint is idempotent on `request_id`. If a client submits a governance request with a `request_id` that already exists in the database, the existing decision is returned without re-running the governance path.

This protects against duplicate processing in cases where the network drops the response after the server has already written the decision.

---

## The Governance Bridge

The `governance_bridge` service is a thin wrapper that handles the HTTP communication with the external governance engines (`governance-engines/`). It provides:
- Connection pooling to the governance engine
- Timeout enforcement (5s for EVA scoring — if exceeded, BLOCK with `GOVERNANCE_TIMEOUT`)
- Circuit breaker (if EVA fails 5 times in 30s, open the circuit and BLOCK all requests until the circuit resets)
- Retry logic (2 retries with 50ms backoff for transient failures)

The circuit breaker is essential for the fail-closed guarantee. If the EVA engine is degraded, requests should not slip through ungoverned.
