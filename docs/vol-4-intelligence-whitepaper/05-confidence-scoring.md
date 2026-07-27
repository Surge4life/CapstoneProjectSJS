# Chapter 05 — Confidence Scoring

## What Confidence Means in G.O.D.S Intelligence

A confidence score in G.O.D.S Intelligence is not a measure of how certain the AI is. It is a measure of how well the corpus evidence supports the response. These are different things.

A general AI model might be 95% "confident" in a hallucinated answer. G.O.D.S Intelligence cannot be confident in something it cannot find in the corpus. The confidence score reflects evidence quality, not model certainty.

---

## The Two Dimensions of Confidence

### Dimension 1: Evidence Confidence

How strong is the evidence backing this response?

```python
evidence_confidence = weighted_average([
    source.tier_confidence * source.relevance_score
    for source in top_3_sources
])
```

- Tier 1 sources contribute fully to evidence confidence
- Tier 5 sources cap evidence confidence at 0.40
- A response with only one low-relevance source has low evidence confidence

### Dimension 2: Retrieval Confidence

How closely do the retrieved sources match the query?

```python
retrieval_confidence = max(source.relevance_score for source in top_sources)
```

- If the best-matching source has relevance 0.95, retrieval confidence is high
- If the best match is 0.45, the corpus is only marginally relevant to this query

### Combined Score

```python
raw_confidence = evidence_confidence * retrieval_confidence

# Apply tier floor
max_tier = min(s.tier for s in top_3_sources)
tier_floor = TIER_FLOORS[max_tier]

confidence = min(raw_confidence, tier_floor)
```

---

## Confidence Tiers

| Score Range | Tier | Meaning | System Behaviour |
|------------|------|---------|----------------|
| 0.80 – 1.00 | `HIGH` | Strong evidence, high relevance | Response delivered directly |
| 0.60 – 0.79 | `MEDIUM` | Adequate evidence | Response with confidence disclosure |
| 0.30 – 0.59 | `LOW` | Weak evidence | Response with explicit caveat |
| 0.00 – 0.29 | `INSUFFICIENT` | Evidence does not support a response | Refuses to answer; offers suggestions |

---

## User-Facing Confidence Communication

The confidence tier is always communicated to the user. How it is communicated depends on the tier:

**HIGH (0.80+):**
> The response is based on strong institutional evidence. Sources are cited below.

**MEDIUM (0.60–0.79):**
> This response is based on adequate evidence, but may not cover all aspects of your question. Please review the cited sources.

**LOW (0.30–0.59):**
> The corpus contains limited evidence on this topic. This response should be treated as preliminary — please verify with authoritative sources.

**INSUFFICIENT:**
> The institutional corpus does not contain sufficient evidence to answer this question reliably. [Suggestions for rephrasing or corpus additions are provided.]

The wording of these disclosures is configurable per deployment — institutions may want to use their own voice. The *presence* of the disclosure is not configurable — it is always shown.

---

## Confidence in Governance Decisions

Confidence scores from G.O.D.S Intelligence do not directly affect governance decisions. However, they inform the `declared_confidence` field that the intelligence system passes to the EVA engine when the intelligence output is itself subject to governance.

When a G.O.D.S Intelligence response is used to inform an action (e.g., the intelligence system recommends a learner for a shortlist, and that recommendation is then submitted as a governance request):
- The EVA Confidence Calibration (CC) dimension evaluates whether the `declared_confidence` is appropriate
- A LOW confidence intelligence output submitted as a high-confidence governance request would score poorly on CC
- This provides a governance check on the AI's self-assessment

---

## Calibration Tracking

The system tracks calibration over time per deployment:

```sql
-- Calibration record: how accurate were our confidence scores?
CREATE TABLE intelligence.calibration_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id UUID NOT NULL,
    declared_confidence DECIMAL(4,3),
    declared_tier VARCHAR(20),
    human_rating VARCHAR(20),    -- ACCURATE | INACCURATE (if human reviews the response)
    outcome VARCHAR(20),         -- Was the response actually useful?
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

When users provide feedback on intelligence responses (via the UI), calibration data accumulates. This data is used to:
1. Identify systematic over/under-confidence by topic area
2. Adjust tier weights per domain
3. Identify corpus gaps (topics where confidence is chronically low)
