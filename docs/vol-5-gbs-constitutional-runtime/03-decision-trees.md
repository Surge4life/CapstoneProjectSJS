# Chapter 03 — Decision Trees

## The GBS Decision Tree

The GBS decision logic follows a clear hierarchical structure. This chapter documents the decision tree that every governance request traverses.

---

## Level 1: Pre-Flight Checks

Before any EVA scoring, the runtime checks pre-conditions:

```
Is the model registered with UDOC?
├── No  → BLOCK (MODEL_NOT_REGISTERED)
└── Yes → Continue

Is the model in a sanctioned state?
├── suspended | revoked | expired
│   └── BLOCK (MODEL_SANCTIONED, state_detail)
└── active | probationary → Continue

Is the request jurisdiction valid for this model?
├── Operator declared jurisdiction ≠ request jurisdiction
│   └── ESCALATE (JURISDICTION_MISMATCH) → Sovereignty officer review
└── Jurisdiction valid → Continue

Is the input hash a known replay?
├── Same input_hash + model_id seen in last 60s
│   └── Return cached decision (idempotency)
└── New request → Continue to EVA
```

---

## Level 2: EVA Scoring

EVA scores all six dimensions. Then the aggregate is computed:

```
Compute EC, SI, RC, FA, CC, SC scores (0–100 each)

Compute OVERALL = weighted_average(EC, SI, RC, FA, CC, SC)
  Weights (default, configurable in PolicyPack):
    EC: 0.20, SI: 0.20, RC: 0.20, FA: 0.20, CC: 0.10, SC: 0.10

Check HARD BLOCK thresholds (cannot be overridden by PolicyPack):
  FA < 40  → BLOCK (FAIRNESS_CRITICAL_FAILURE)
  RC < 35  → BLOCK (REGULATORY_CRITICAL_FAILURE)
  SC < 30  → BLOCK (SOVEREIGNTY_CRITICAL_FAILURE)

If any hard threshold triggered → BLOCK immediately
Otherwise → Continue to Policy Engine
```

---

## Level 3: Policy Engine

The active PolicyPack is applied:

```
For each rule in PolicyPack (by priority, highest first):
  Does the rule condition match the EVA scores?
  ├── Yes → Apply rule outcome (APPROVE | REVIEW | ESCALATE | BLOCK)
  │         Record which rule fired
  │         Continue to UDOC enforcement
  └── No  → Try next rule

No rule fired → Apply PolicyPack default outcome (typically REVIEW if OVERALL < 70)
```

---

## Level 4: UDOC Enforcement

The policy outcome is submitted to UDOC for sovereignty and FSM validation:

```
UDOC.enforce(model_id, model_state, jurisdiction, policy_outcome)

Is the model in probationary state?
├── Yes, outcome is APPROVE
│   └── Override to REVIEW (probationary models cannot be auto-approved)
└── No → Proceed with policy outcome

Is there a cross-border sovereignty issue?
├── Yes, no cross-border authorisation on file
│   └── Override to ESCALATE (SOVEREIGNTY_REQUIRED)
└── No → Proceed

Is the operator's overall governance record concerning?
├── Suspension history + this is a borderline APPROVE
│   └── Flag for enhanced monitoring (does not change outcome)
└── No flag → Proceed

Final UDOC outcome: APPROVE | REVIEW | ESCALATE | BLOCK
```

---

## Level 5: Outcome Finalisation

```
Map final outcome:
├── APPROVE  → output is permissible, proceed
├── REVIEW   → human oversight required before proceeding
├── ESCALATE → senior governance review required (compliance/sovereignty officer)
└── BLOCK    → output is prohibited, do not proceed

Create DecisionRecord with:
  - outcome
  - EVA scores
  - rule_fired (which PolicyPack rule triggered)
  - reasoning (human-readable)
  - HMAC seal
  - audit_ref_id (audit chain record)

If BLOCK or ESCALATE → create OversightCase
  - Assign to reviewer per division config
  - Set SLA deadline
  - Notify subject (the entity whose action was blocked)

Publish governance event to Kafka
Return outcome to caller
```

---

## Outcome Meanings for Callers

| Outcome | Meaning | Expected Action |
|---------|---------|----------------|
| `APPROVE` | Governance path passed | Proceed with the AI-informed action |
| `REVIEW` | Human oversight required | Hold action pending human reviewer confirmation |
| `ESCALATE` | Senior review required | Escalate to compliance/sovereignty officer; do not proceed |
| `BLOCK` | Prohibited | Do not proceed; inform subject; oversight case opened |

The caller (the AI system that submitted the governance request) is responsible for respecting the outcome. The GBS Runtime cannot enforce the outcome on the AI system's behalf — it can only record it. Enforcement of the outcome in the calling system is the operator's responsibility under the UDOC agreement.
