# Volume V — GBS Constitutional Runtime
## Every Rule. Every Decision Tree. Every Policy.

> The GBS (Governance and Behavioural Standards) Constitutional Runtime is the deterministic core of the G.O.D.S ecosystem. Unlike probabilistic AI systems, the GBS Runtime produces the same output for the same input — always. It is the non-bypassable governance layer.

---

## Contents

| Chapter | Title |
|---------|-------|
| [01](01-overview.md) | Runtime Overview |
| [02](02-deterministic-engines.md) | The Deterministic Engines |
| [03](03-decision-trees.md) | Decision Trees |
| [04](04-policy-framework.md) | Policy Framework (Policy-to-Code) |
| [05](05-constitutional-checks.md) | Constitutional Checks |
| [06](06-audit-records.md) | Audit Records |
| [07](07-failure-states.md) | Failure States & Fail-Closed Behaviour |
| [08](08-approval-workflows.md) | Approval Workflows |
| [09](09-eva-scoring.md) | EVA 6-Dimensional Sovereign Risk Scoring |
| [10](10-sovereignty-fsm.md) | Sovereignty Finite State Machine (SVS→FSM) |

---

## The Governance Path

Every AI request that enters the G.O.D.S ecosystem must traverse the governance path. There are no exceptions, no overrides, no bypass routes. The path is:

```
AI Request
  → Attachment (agent / sidecar / gateway / edge)
  → platform-core /decisions
    → EVA 6-D risk score
    → UDOC Orchestrator: sovereignty(SVS) → FSM → enforce
  → Decision: {APPROVE | REVIEW | ESCALATE | BLOCK}
    → HMAC / Dilithium-reference seal
  → Kafka event_bus
    → audit_writer
    → Cassandra/WORM hash-chain + Merkle root
  → Response to caller
  → FAIL-CLOSED if engine/HSM unreachable for CRITICAL class
```

This path is documented in full in this volume. Every step, every decision point, every failure mode.
