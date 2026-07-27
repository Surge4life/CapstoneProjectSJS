# Chapter 04 — Policy Framework

## What Is a PolicyPack?

A PolicyPack is the configurable governance ruleset for a deployment. It defines:
- What EVA score thresholds trigger what outcomes
- How the weights of the six EVA dimensions are balanced
- What exceptions or elevated scrutiny rules apply
- The default outcome when no specific rule fires

A PolicyPack is versioned, audited, and requires compliance officer authorisation to activate. It is the primary tool by which institutions customise governance behaviour within the bounds set by the constitutional framework.

---

## PolicyPack Structure

```python
@dataclass
class PolicyPack:
    id: UUID
    version: int
    name: str                          # "Standard Employment Governance v3"
    description: str
    status: str                        # draft | review | active | archived
    activated_by: UUID                 # Compliance officer who activated it
    activated_at: datetime | None
    
    # EVA dimension weights (must sum to 1.0)
    weight_ec: Decimal                 # Ethical Cooperation
    weight_si: Decimal                 # Societal Impact
    weight_rc: Decimal                 # Regulatory Compliance
    weight_fa: Decimal                 # Fairness
    weight_cc: Decimal                 # Confidence Calibration
    weight_sc: Decimal                 # Sovereignty Compliance
    
    # Hard block thresholds (minimum scores below which auto-BLOCK)
    hard_block_fa: int                 # Default: 40
    hard_block_rc: int                 # Default: 35
    hard_block_sc: int                 # Default: 30
    
    # Rules (evaluated in priority order)
    rules: list[PolicyRule]
    
    # Default outcome when no rule fires
    default_outcome: str               # Default: REVIEW
```

---

## PolicyRule Structure

```python
@dataclass
class PolicyRule:
    id: UUID
    policy_pack_id: UUID
    priority: int                      # Lower number = evaluated first
    name: str                          # "High-Risk Employment Decision"
    description: str
    
    # Condition (all fields must match — logical AND)
    condition: PolicyCondition
    
    # Outcome when condition matches
    outcome: str                       # APPROVE | REVIEW | ESCALATE | BLOCK
    
    # Human-readable reasoning template
    reasoning_template: str            # "{model_name} scored {fa_score} on Fairness..."

@dataclass  
class PolicyCondition:
    # EVA thresholds (optional — None = not evaluated)
    min_overall: int | None
    max_overall: int | None
    min_ec: int | None
    max_ec: int | None
    min_fa: int | None
    max_fa: int | None
    min_rc: int | None
    max_rc: int | None
    min_si: int | None
    max_si: int | None
    min_cc: int | None
    max_cc: int | None
    min_sc: int | None
    max_sc: int | None
    
    # Contextual conditions
    output_categories: list[str] | None  # Only apply to certain output types
    jurisdictions: list[str] | None      # Only apply to certain jurisdictions
    operator_in_probation: bool | None   # Only apply to probationary operators
```

---

## Example PolicyPack Rules (Default/Standard)

```json
{
  "rules": [
    {
      "priority": 1,
      "name": "Excellent Governance — Auto Approve",
      "condition": { "min_overall": 90, "min_fa": 80 },
      "outcome": "APPROVE",
      "reasoning_template": "Model scored {overall} overall with excellent fairness ({fa_score}). Auto-approved."
    },
    {
      "priority": 2,
      "name": "Good Governance — Approve with Monitoring",
      "condition": { "min_overall": 75, "min_fa": 70, "min_rc": 80 },
      "outcome": "APPROVE",
      "reasoning_template": "Model meets all governance thresholds. Approved with standard monitoring."
    },
    {
      "priority": 3,
      "name": "Fairness Concern — Mandatory Review",
      "condition": { "max_fa": 69 },
      "outcome": "REVIEW",
      "reasoning_template": "Fairness score ({fa_score}) below threshold. Human review required."
    },
    {
      "priority": 4,
      "name": "Moderate Governance — Human Review",
      "condition": { "min_overall": 60, "max_overall": 74 },
      "outcome": "REVIEW",
      "reasoning_template": "Model scored {overall} overall. Human oversight required."
    },
    {
      "priority": 5,
      "name": "Poor Governance — Escalate",
      "condition": { "min_overall": 40, "max_overall": 59 },
      "outcome": "ESCALATE",
      "reasoning_template": "Model scored {overall} overall. Senior governance review required."
    }
  ],
  "default_outcome": "BLOCK"
}
```

The default outcome is `BLOCK` — if no rule matches (e.g., `overall < 40`), the action is blocked. This is the fail-closed principle applied to policy.

---

## PolicyPack Lifecycle

```
DRAFT → REVIEW → ACTIVE
                    ↓
                ARCHIVED (when a new version is activated)
```

- **DRAFT:** Compliance officer is drafting the policy. Not applied to any decisions.
- **REVIEW:** Policy has been submitted for review. A senior compliance officer or `gods_admin` must approve.
- **ACTIVE:** Exactly one PolicyPack is active at any time. Activating a new pack archives the previous one.
- **ARCHIVED:** Retained permanently. Historical decisions reference the policy version that was active when they were made.

PolicyPack activation is recorded in the audit chain. Every historical decision can be re-evaluated with the PolicyPack that was active at the time — the version is embedded in the `DecisionRecord`.
