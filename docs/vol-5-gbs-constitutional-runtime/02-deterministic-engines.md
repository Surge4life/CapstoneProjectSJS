# Chapter 02 — Deterministic Engines

## What Makes GBS Deterministic?

The GBS Runtime is deterministic by design. Given identical inputs — the same model, the same request, the same PolicyPack version — the GBS Runtime produces the same outcome every time. This is not incidental. It is a constitutional requirement.

A governance system that produces different outcomes for the same inputs cannot be trusted. Auditability requires reproducibility: you must be able to verify that the outcome recorded in the audit chain matches what the system would produce if you re-ran the same inputs today.

---

## Sources of Determinism

### Deterministic Source 1: The EVA Engine

The EVA engine produces deterministic scores because:
- Every scoring function is a weighted formula over well-defined inputs
- There are no random elements in the scoring logic
- Floating point arithmetic is consistent (same hardware, same Python version)
- The output is rounded to two decimal places before comparison against thresholds

```python
# EVA FA (Fairness) scorer — fully deterministic
def score_fa(affecting_subjects: list[SubjectDescriptor]) -> float:
    if not affecting_subjects:
        return 100.0  # No subjects affected = neutral fairness score

    protected_characteristic_exposure = sum(
        s.protected_characteristic_weight for s in affecting_subjects
    )
    equitable_distribution = compute_equitable_distribution(affecting_subjects)
    historical_bias_factor = get_historical_bias_factor(model_id)

    raw = (
        0.50 * (1.0 - protected_characteristic_exposure)
        + 0.30 * equitable_distribution
        + 0.20 * (1.0 - historical_bias_factor)
    ) * 100

    return round(raw, 2)
```

No randomness. Every call with the same inputs produces the same score.

### Deterministic Source 2: The Policy Engine

PolicyPack rules are evaluated in order:
1. Rules are processed from highest priority to lowest
2. The first rule that fires wins (explicit `outcome` in the rule)
3. If no rule fires, the default outcome applies
4. Rule evaluation is pure predicate logic over the EVA scores

```python
def evaluate_policy(eva_scores: EVAScores, policy_pack: PolicyPack) -> PolicyOutcome:
    for rule in sorted(policy_pack.rules, key=lambda r: r.priority):
        if rule.condition.matches(eva_scores):
            return PolicyOutcome(
                outcome=rule.outcome,
                rule_id=rule.id,
                rule_name=rule.name,
                reasoning=rule.reasoning_template.format(scores=eva_scores)
            )
    return policy_pack.default_outcome
```

The same EVA scores + same PolicyPack = same PolicyOutcome. Always.

### Deterministic Source 3: UDOC FSM

The UDOC FSM transitions are deterministic. Given a model's current state and the governance context, there is exactly one valid transition. See Chapter 10 for the full FSM specification.

### Deterministic Source 4: No Randomness in the Critical Path

Randomness is explicitly excluded from the governance critical path. UUIDs are generated before the path begins. The `request_id` is supplied by the client (idempotency key). Timestamps are recorded from the system clock. None of these are used in outcome determination.

---

## Reproducibility Guarantee

The `decision_seal` on every `DecisionRecord` includes:

```
HMAC-SHA256(
  decision_id +
  model_id +
  input_hash +
  outcome +
  eva_ec + eva_si + eva_rc + eva_fa + eva_cc + eva_sc +
  policy_version +
  timestamp
)
```

To verify a decision:
1. Re-run the GBS path with the same inputs (model state, EVA scores, PolicyPack version)
2. Verify the output matches the recorded outcome and EVA scores
3. Verify the HMAC seal matches

If the system is truly deterministic, step 2 will always match. If it doesn't, the system has been modified — which is itself a governance event.

---

## Controlled Non-Determinism

One element is intentionally variable: the **reasoning text**. The human-readable explanation included in the decision record is generated with a templating system, not a fixed string. While the outcome is deterministic, the phrasing of the reasoning may vary slightly across deployments (e.g., different language settings, different PolicyPack reasoning templates).

This is documented explicitly so auditors understand: the outcome is deterministic and verifiable; the reasoning text is templated and may vary.
