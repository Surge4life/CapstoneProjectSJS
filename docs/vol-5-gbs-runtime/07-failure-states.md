# Chapter 07 — Failure States & Fail-Closed Behaviour

## The Fail-Closed Principle

When the GBS Runtime encounters a failure, it fails closed. This means: when in doubt, block.

An AI system that proceeds without governance when governance fails is not a governed system. The GBS Runtime's failure behaviour is as important as its success behaviour.

---

## Failure Categories

### Category 1: EVA Engine Unavailable

**Trigger:** EVA engine timeout (>5s), HTTP error, circuit breaker open  
**Outcome:** `BLOCK` with code `GOVERNANCE_TIMEOUT`  
**Audit record:** Created with `outcome: BLOCK`, `failure_type: EVA_UNAVAILABLE`  
**Oversight case:** Created (the subject should be able to retry once the engine is available)  
**Recovery:** When EVA engine recovers, circuit breaker closes, normal processing resumes

```python
try:
    eva_scores = await governance_bridge.score(request)
except (TimeoutError, EngineUnavailableError, CircuitBreakerOpenError):
    return await create_failure_decision(
        outcome="BLOCK",
        failure_code="GOVERNANCE_TIMEOUT",
        reasoning="Governance engine unavailable. Action blocked pending restoration. Please retry."
    )
```

### Category 2: UDOC Engine Unavailable

**Trigger:** UDOC enforcement engine timeout or error  
**Outcome:** `BLOCK` with code `UDOC_UNAVAILABLE`  
**Audit record:** Created  
**Recovery:** As above

### Category 3: PolicyPack Unavailable

**Trigger:** Policy cache empty (startup), database error during reload  
**Outcome:** System enters `POLICY_DEGRADED` mode — all decisions are `REVIEW` (not APPROVE)  
**Reasoning:** Conservative fallback — all decisions require human review when the policy engine cannot function  
**Recovery:** PolicyPack reloads automatically when database connection restores

### Category 4: Audit Write Failure

**Trigger:** Cassandra unavailable, PostgreSQL connection error  
**Outcome:** The governance request is held (not returned to caller) until the audit write succeeds or fails permanently  
**Retry:** 3 retries with exponential backoff (max 5s total wait)  
**If retry fails:** `BLOCK` with code `AUDIT_WRITE_FAILURE` — the decision cannot be made without an audit record

This is the most severe failure case. A governance decision that cannot be recorded must not be executed.

### Category 5: HSM/Key Service Unavailable

**Trigger:** HMAC signing service unavailable  
**Outcome:** `BLOCK` with code `SEAL_UNAVAILABLE`  
**Reasoning:** An unsealed decision record cannot be trusted

### Category 6: Invalid Model State

**Trigger:** Model record inconsistency (e.g., `active` state but suspended flag set)  
**Outcome:** `ESCALATE` with code `MODEL_STATE_INCONSISTENCY`  
**Audit record:** Includes `system_alert: true`  
**Monitoring alert:** Triggered (this should never happen — it indicates a data integrity issue)

---

## Failure Monitoring

All governance failures are tracked:

```python
# Prometheus metrics for failure tracking
gods_governance_failures_total.labels(failure_code="GOVERNANCE_TIMEOUT").inc()
gods_governance_failures_total.labels(failure_code="AUDIT_WRITE_FAILURE").inc()

# Alert thresholds
GOVERNANCE_TIMEOUT_ALERT = 5  # Any timeout triggers a high-priority alert
AUDIT_WRITE_FAILURE_ALERT = 1  # Any audit write failure triggers critical alert
```

---

## Recovery Procedures

### After EVA Engine Recovery

1. Circuit breaker resets automatically after 30s of successful calls
2. Governance requests resume normal processing
3. Oversight cases created during the failure period should be reviewed (the subjects were blocked unfairly; they should be able to resubmit)

### After Audit Write Recovery

1. Cassandra queue drains automatically — any decisions that were buffered during the outage are written
2. Verify queue drain via `gods-cli audit-status`
3. If any decisions were lost (not just delayed), this is a critical incident — initiate the audit chain reconciliation procedure

### After Complete Platform Restart

1. PolicyPack reloads from database on startup
2. Circuit breakers reset
3. Edge nodes resync via their heartbeat mechanism
4. Run `gods-cli health-check --all` to confirm all systems are operational before resuming governance operations

---

## The Decision on Fail-Open vs Fail-Closed

The fail-closed decision is a values decision, not just a technical one. The alternative — fail-open (allow when governance fails) — would be more permissive in practice during outages, but it would mean:

- AI actions proceed without governance during any infrastructure issue
- Audit records have gaps during failures
- Operators can potentially trigger governance failures deliberately to bypass governance

Fail-closed accepts operational disruption as the cost of governance integrity. This tradeoff is explicitly accepted in the G.O.D.S constitutional framework.
