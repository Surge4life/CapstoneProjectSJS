# Chapter 05 — Intelligence vs Governance

## The Critical Distinction

The G.O.D.S ecosystem contains two distinct categories of capability that are often conflated in other platforms. In G.O.D.S, they are architecturally separate and constitutionally subordinate to each other in a defined order.

| Category | What It Does | How It Works | Who Controls It |
|----------|-------------|-------------|----------------|
| **Intelligence** | Answers questions, generates content, analyses data, produces recommendations | Probabilistic — produces the best available answer given the evidence | Bounded by governance |
| **Governance** | Decides whether an intelligence output is permissible, appropriate, and compliant | Deterministic — produces the same outcome for the same input every time | Constitutional — cannot be overridden |

**The relationship is one-directional: Governance constrains Intelligence. Intelligence does not influence Governance.**

---

## Why This Distinction Matters

Consider a scenario: a learner applies for a job through SETHS. The G.O.D.S Intelligence system analyses their application and produces a recommendation. That recommendation passes through the GBS Constitutional Runtime before it is acted upon.

If the recommendation is within constitutional boundaries — it is proportionate, non-discriminatory, evidence-based, and within the learner's stated consent — the governance engine `APPROVE`s it and it proceeds.

If the recommendation would, for example, discriminate on a protected characteristic — even if the statistical model believes this produces a better outcome — the governance engine `BLOCK`s it. The fact that the intelligence system produced the recommendation with high confidence is irrelevant. Constitutional rules are not probabilistic.

This is the intelligence-governance relationship: Intelligence proposes. Governance decides.

---

## Technical Architecture of the Separation

The separation is enforced architecturally, not just by policy.

### Intelligence Layer (`gods_intelligence` service, `intelligence` router)

- Operates on the corpus (internal knowledge base)
- Returns: answer, evidence references, confidence score, corpus sources
- Has no access to: governance decision records, oversight cases, policy enforcement
- Cannot: modify governance configuration, approve or block requests, access the Kafka audit bus directly

### Governance Layer (`governance-engines`, `decisions` router, `gbs_engine` service)

- Operates on: the EVA score, PolicyPack rules, constitutional checks
- Returns: outcome (`APPROVE | REVIEW | ESCALATE | BLOCK`), reasoning, seal
- Has no access to: the intelligence corpus contents (only the metadata and risk assessment of the intelligence output)
- Cannot: be influenced by confidence scores from the intelligence layer

### The Interface

The only interface between the two layers is the governance request payload. This payload contains:

```json
{
  "request_id": "uuid",
  "model_id": "registered-model-id",
  "input_hash": "sha256-of-input",
  "output_hash": "sha256-of-output",
  "output_category": "recommendation | generation | classification | retrieval",
  "declared_confidence": 0.87,
  "affecting_subjects": ["subject-id-1"],
  "jurisdiction": "ZA",
  "operator_id": "operator-uuid"
}
```

The governance engine never sees the content of the intelligence output. It sees only the metadata. This preserves the separation: governance rules apply to the *category and risk profile* of an action, not to its specific content.

---

## When Intelligence and Governance Interact at the UI Level

At the user interface level, users may experience intelligence and governance as seamless. A learner submits an application, receives feedback, and is told whether it was approved. They do not see the internal separation.

This is by design. The separation is an engineering and governance principle, not a user experience principle. The user experience is unified. The system internals are separated.

---

## The Override Question

**Can an administrator use the intelligence system to override governance?**

No. The intelligence system has no write access to governance configuration. An administrator who wants to change governance thresholds must do so through the `policy` router, with elevated RBAC permissions, with a full audit record of the change, and — depending on deployment configuration — with multi-party authorisation.

The intelligence system can *suggest* that a policy change might be appropriate, based on analysis of governance outcomes. That suggestion is a recommendation. Acting on it requires human decision-making through the proper governance channels.
