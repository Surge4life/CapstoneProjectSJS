# Chapter 06 — GBS Doctrine

## Governance and Behavioural Standards: The Constitutional Doctrine

GBS — Governance and Behavioural Standards — is the constitutional framework that defines the rules every AI system must follow when operating within the G.O.D.S ecosystem. It is not a checklist. It is a runtime. It executes on every governed request.

---

## The GBS Mandate

GBS exists because voluntary compliance fails. Organisations and AI systems that intend to behave ethically still produce harmful outcomes when there is no systematic check. Intention is not architecture.

GBS replaces intention with verification. Every AI action is checked against the GBS rule set before it produces an output that affects a human being. The check is automatic, consistent, and logged.

---

## The Six GBS Dimensions (EVA Framework)

The EVA (Evaluating Valiant Algorithms) engine scores every AI request across six dimensions. These dimensions are the operationalised form of the GBS doctrine.

### Dimension 1: Ethical Cooperation

Does the action align with the cooperative ethical framework of the deployment context? This checks for:
- Actions that exploit power imbalances
- Actions that benefit one party at systematic harm to another
- Actions that violate trust relationships established in the system

**Score range:** 0–100 (100 = fully aligned)

---

### Dimension 2: Societal Impact

What is the likely societal effect of this action at scale? A single action may be benign. A pattern of identical actions may be harmful. The EVA engine evaluates:
- Impact on marginalised communities
- Compounding effects of automated decisions
- Alignment with declared public interest outcomes

**Score range:** 0–100 (100 = positive societal impact)

---

### Dimension 3: Regulatory Compliance

Does the action comply with applicable law and regulation in the declared jurisdiction? The GBS engine maintains a policy set (managed via the `policy` router and `PolicyPack` model) that translates regulatory requirements into executable rules.

Current jurisdictional coverage:
- South Africa: POPIA, BBBEE Act, Employment Equity Act, NQF Act, Labour Relations Act
- Extensible to other jurisdictions via policy packs

**Score range:** 0–100 (100 = fully compliant)

---

### Dimension 4: Fairness

Is the action consistent across similarly situated individuals, regardless of protected characteristics? The bias detection component checks:
- Demographic parity
- Equal opportunity metrics
- Calibration across groups
- Historical outcome consistency

**Score range:** 0–100 (100 = full fairness)

---

### Dimension 5: Confidence Calibration

Is the AI system appropriately confident in its output? Overconfident outputs in high-stakes domains are treated as higher risk. The governance engine checks:
- Declared confidence vs historical calibration for this model
- Confidence appropriateness for the output category
- Whether the confidence level warrants automatic approval or human review

**Score range:** 0–100 (100 = well-calibrated, appropriate confidence)

---

### Dimension 6: Sovereignty Compliance

Does the action comply with the sovereignty declarations of the deployment jurisdiction? This checks:
- Data residency requirements
- Cross-border data flow authorisations
- Operator authorisation for the requested action type
- Subject consent status

**Score range:** 0–100 (100 = full sovereignty compliance)

---

## The GBS Outcome Thresholds

The six dimension scores are weighted and combined into an overall GBS score. The thresholds map scores to outcomes:

| GBS Score | Outcome | Meaning |
|-----------|---------|---------|
| 85–100 | `APPROVE` | Request proceeds automatically |
| 65–84 | `REVIEW` | Request proceeds; flagged for review |
| 40–64 | `ESCALATE` | Request held; human review required before proceeding |
| 0–39 | `BLOCK` | Request rejected; OversightCase created |
| Any dimension = 0 | `BLOCK` | Absolute constitutional violation, regardless of overall score |

The thresholds are configurable per deployment via `PolicyPack`. The `any dimension = 0 → BLOCK` rule is not configurable. It is hardcoded.

---

## GBS Policy-to-Code

The GBS doctrine is implemented via a Policy-to-Code engine (managed by the `policy` router). This engine translates human-readable policy rules into executable rule objects that the GBS Runtime applies.

A policy rule object:
```json
{
  "rule_id": "uuid",
  "name": "No employment decisions on protected characteristics",
  "dimension": "fairness",
  "jurisdiction": "ZA",
  "applies_to": ["seths", "workforce"],
  "condition": "output.references_characteristic IN ['race', 'gender', 'disability', 'pregnancy']",
  "action": "BLOCK",
  "explanation": "Employment decisions referencing protected characteristics violate the Employment Equity Act (No. 55 of 1998) and GBS Fairness Dimension.",
  "version": 3,
  "effective_date": "2024-01-01",
  "supersedes": "rule-id-of-version-2"
}
```

Policy rules are versioned. Changes to policy rules are audited. Historical policy rule versions are preserved so that past decisions can be re-evaluated under the rules that were in effect at the time.
