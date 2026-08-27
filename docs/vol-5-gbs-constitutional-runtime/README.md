# Volume V — GBS Constitutional Runtime
## Every Rule. Every Decision Tree. Every Policy.

> The GBS (Governance and Behavioural Standards) Constitutional Runtime is the **designed** deterministic core of the G.O.D.S ecosystem. Unlike probabilistic AI systems, the GBS Runtime is specified to produce the same output for the same input — always. It is the non-bypassable governance layer **in design**.

**Capstone honesty:** live UDOC on Render + Neon proves EVA fair≠BLOCK / biased=BLOCK on `model-001`. Kafka, Cassandra/WORM, HSM, and Dilithium seals in the path below are **target architecture**, not Capstone live facts. See [`udoc-mvp/LIMITATIONS_REGISTER.md`](../../udoc-mvp/LIMITATIONS_REGISTER.md) and [Vol X Ch 13](../vol-10-infrastructure/13-render-deployment.md).

**Folder merge (2026-08-27):** chapters previously split under `docs/vol-5-gbs-runtime/` now live here.

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

Every AI request that enters the G.O.D.S ecosystem must traverse the governance path. There are no exceptions, no overrides, no bypass routes **in the constitutional design**. The path is:

```
AI Request
  → Attachment (agent / sidecar / gateway / edge)
  → platform-core /decisions
    → EVA 6-D risk score
    → UDOC Orchestrator: sovereignty(SVS) → FSM → enforce
  → Decision: {APPROVE | REVIEW | ESCALATE | BLOCK}
    → HMAC / Dilithium-reference seal          [designed]
  → Kafka event_bus                            [designed]
    → audit_writer
    → Cassandra/WORM hash-chain + Merkle root  [designed]
  → Response to caller
  → FAIL-CLOSED if engine/HSM unreachable for CRITICAL class
```

**Live Capstone subset:** `POST /decisions` and `POST /decisions/batch` on platform-core, demo pack `model-001`, Neon-backed audit rows. Designed path remains the law; live path is the proven slice.

This volume documents every step, every decision point, every failure mode.
