# Chapter 01 — GBS Runtime Overview

## The Deterministic Core

The GBS Constitutional Runtime is the non-bypassable governance engine at the centre of the G.O.D.S ecosystem. It is the system's conscience — and unlike a human conscience, it cannot be argued with, bribed, tired out, or distracted.

The GBS Runtime is deterministic. Given the same input under the same policy configuration, it will always produce the same output. This is not a limitation — it is the point. Governance that produces different outcomes under identical conditions is not governance.

---

## What the GBS Runtime Is Not

**It is not a machine learning model.** There is no training, no probabilistic output, no confidence interval. The output is always one of four values: `APPROVE`, `REVIEW`, `ESCALATE`, or `BLOCK`.

**It is not configurable by operators.** Operators (businesses deploying AI models) can configure many things in the G.O.D.S ecosystem. They cannot configure the GBS Runtime. They can influence governance *thresholds* (within permitted bounds via PolicyPack) but they cannot modify the constitutional checks themselves.

**It is not an AI system.** The GBS Runtime does not learn from past decisions. It applies rules. Those rules are authored by humans, reviewed by compliance officers, and activated through a formal governance process.

---

## Components of the GBS Runtime

```
GBS Constitutional Runtime
├── EVA Engine           (6-dimensional risk scoring — probabilistic input)
├── Constitutional Checker (deterministic rule evaluation)
├── Policy Engine        (Policy-to-Code rule application)
├── UDOC Orchestrator    (SVS → FSM → Enforce)
└── Decision Sealer      (HMAC + audit record)
```

### EVA Engine
Input: governance request payload  
Output: 6-dimensional risk score (0–100 per dimension) + overall GBS score  
Nature: **Probabilistic** — uses statistical models and historical calibration  
Role: Risk assessment input to the constitutional checker

### Constitutional Checker
Input: EVA scores + constitutional rules (hardcoded)  
Output: Initial outcome determination  
Nature: **Deterministic** — hardcoded constitutional rules that cannot be overridden  
Role: Identifies absolute constitutional violations (any dimension = 0 → BLOCK regardless of overall score)

### Policy Engine
Input: EVA scores + PolicyPack rules for the deployment  
Output: Policy-based outcome determination  
Nature: **Deterministic** — rule-based evaluation of the PolicyPack  
Role: Applies jurisdiction-specific and deployment-specific rules

### UDOC Orchestrator
Input: Outcome from Policy Engine + model registry state  
Output: Final enforced outcome  
Nature: **Deterministic** — FSM-based state machine  
Role: Verifies the model is in an active state, applies sovereignty checks, enforces the final decision

### Decision Sealer
Input: Final outcome + full reasoning chain  
Output: Sealed `DecisionRecord`  
Nature: Cryptographic — HMAC signature + Dilithium reference  
Role: Produces the tamper-evident audit record

---

## The 50ms Governance Guarantee

The GBS Runtime is engineered to complete the full governance path in under 50 milliseconds under normal operating conditions. This is not a soft target — it is a constitutional requirement. Governance that adds 10 seconds of latency to every AI request is not deployable governance.

Engineering choices made to meet the 50ms target:
- EVA engine runs in-process (no network call) for the hot path
- Policy rules are cached in memory (loaded at startup, refreshed on update)
- UDOC Orchestrator state machine runs in-memory
- Database writes are asynchronous (decision is sealed before the write completes)
- Kafka publish is fire-and-forget (the caller does not wait for the event to be consumed)

The asynchronous writes mean there is a brief window where a decision exists (has been communicated to the caller) but has not yet been committed to the database. This window is bounded by the database write latency (typically <5ms). The decision is sealed before it is communicated — the seal is the authoritative record.

---

## Failure Modes

The GBS Runtime has three failure modes. All three are fail-closed:

| Failure | Response | Recovery |
|---------|---------|---------|
| EVA engine error | `BLOCK` with `GOVERNANCE_ERROR` reason + OversightCase | Auto-retry; OversightCase remains open until reviewed |
| Database write failure | Decision still communicated as sealed; write retried from Kafka | Kafka consumer retries; alert generated if retries exhausted |
| UDOC Orchestrator unreachable | `BLOCK` with `GOVERNANCE_UNAVAILABLE` reason | Service health check; automatic recovery on reconnection |
