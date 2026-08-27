# Chapter 08 — Approval Workflows & Oversight

## The Human in the Loop

The GBS Runtime produces governance outcomes. For `APPROVE` outcomes, the outcome is final — the action proceeds. For `REVIEW`, `ESCALATE`, and `BLOCK` outcomes, a human must be involved. This chapter documents those human-in-the-loop workflows.

---

## REVIEW Workflow

A `REVIEW` outcome means: the governance evaluation was inconclusive or borderline. A human reviewer must confirm before the action proceeds.

```
REVIEW decision created
    ↓
OversightCase created (type: STANDARD_REVIEW)
    ↓
Assigned to: division's designated reviewer (round-robin or by specialty)
    ↓
SLA: 48 hours (configurable)
    ↓
Reviewer receives notification + case summary
    ↓
Reviewer examines:
  - Decision record (EVA scores, policy rule that triggered REVIEW)
  - Subject profile (the entity whose action requires review)
  - Supporting documents (if any)
  - Historical pattern (previous decisions on this subject/model)
    ↓
Reviewer action options:
  ├── CONFIRM APPROVE → Action proceeds
  ├── CONFIRM BLOCK   → Action blocked, with reviewer reasoning
  ├── REQUEST INFO    → Case held, more information requested
  └── ESCALATE        → Elevate to compliance officer (promotes to ESCALATE workflow)
    ↓
Decision finalized:
  OversightCase status: resolved
  Outcome override recorded in DecisionRecord
  Subject notified
```

---

## ESCALATE Workflow

An `ESCALATE` outcome means: this requires senior governance review. A compliance officer or sovereignty officer must handle this case.

```
ESCALATE decision created
    ↓
OversightCase created (type: ESCALATED_REVIEW)
    ↓
Assigned to: compliance officer pool (or designated individual)
    ↓
SLA: 24 hours (shorter SLA — escalations are more urgent)
    ↓
Compliance officer action options:
  ├── CONFIRM APPROVE → Action proceeds
  ├── CONFIRM BLOCK   → Action blocked
  ├── ISSUE POLICY GUIDANCE → Resolve and update PolicyPack
  └── REFER TO SOVEREIGNTY → Refers to sovereignty officer if SC is the issue
    ↓
Decision finalized with documented reasoning
Subject notified
Governance report updated
```

---

## BLOCK Workflow (Challenge Process)

A `BLOCK` outcome immediately prevents the action. But the subject has the right to challenge:

```
BLOCK decision created
    ↓
OversightCase created (type: BLOCK_CHALLENGE)
    ↓
Subject notified:
  "Action blocked. See reason: [EVA score summary + policy rule]"
  "You may challenge this decision via [challenge link]"
    ↓
Subject option 1: Accept and provide additional information
  → Provides context that the EVA engine couldn't assess
  → Case reviewed with additional context
  → Reviewer may override the BLOCK

Subject option 2: Formal challenge
  → Escalates to compliance officer
  → Compliance officer reviews full record
  → Decision: Uphold block OR override with documented justification

Subject option 3: Accept the block
  → OversightCase resolved with no action
  → Block stands

SLA: 72 hours for initial response; challenge process has longer SLA
```

---

## SLA Enforcement

SLA timers are enforced by the notification engine (see Volume II, Chapter 10):

| Case Type | Initial SLA | Escalation Trigger |
|-----------|------------|-------------------|
| STANDARD_REVIEW | 48 hours | 24 hours remaining → warning to reviewer |
| ESCALATED_REVIEW | 24 hours | 12 hours remaining → warning |
| BLOCK_CHALLENGE | 72 hours for initial; 7 days for full challenge | Day 5 → warning |

When SLA is breached:
1. `GOVERNANCE.SLA_BREACH` audit event created
2. Compliance officer alerted
3. Case flagged as `sla_breached: true`
4. Governance report shows as SLA breach

SLA breaches appear in compliance reports. A pattern of SLA breaches indicates either understaffing or a PolicyPack that generates too many review/escalation outcomes.

---

## The Oversight Case Interface

Oversight cases are managed through `platform-web` (compliance officers) and `platform-internal` (supervisors). The case interface shows:

1. **Case header** — type, status, SLA countdown, subject
2. **Decision record** — full EVA scores with dimension-by-dimension explanation
3. **Subject profile** — relevant facts about the entity whose action was blocked
4. **Policy analysis** — which rule triggered, what the thresholds were, how close to the boundary
5. **Action history** — previous decisions on this subject/model
6. **Documents** — any supporting evidence
7. **Action panel** — confirm/override/escalate/request-info buttons
8. **Notes** — reviewer notes (required for any override)
