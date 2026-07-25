# Chapter 04 — Evidence Hierarchy

## The G.O.D.S Evidence Hierarchy

Not all evidence is equal. In a governance system, the quality and authority of evidence matters deeply. A claim backed by a primary legislative source carries more weight than a claim backed by an informal summary. G.O.D.S Intelligence operationalises this through a formal evidence hierarchy.

---

## The Five Evidence Tiers

### Tier 1: Constitutional Sources
**Authority level:** Highest  
**Examples:** Legislation (Acts of Parliament), regulations, constitutional provisions, official government gazettes, binding court orders  
**Treatment:** Used verbatim where possible. Paraphrase only when required for clarity, with explicit flagging that this is a paraphrase.  
**Confidence contribution:** High — a response backed primarily by Tier 1 evidence receives the highest confidence score contribution from the evidence dimension.

### Tier 2: Institutional Primary Sources
**Authority level:** High  
**Examples:** Board resolutions, official policy documents, constitutional frameworks (like this Engineering Canon), founding documents, audited financial statements, certified certifications  
**Treatment:** Quoted with source reference. Used to interpret Tier 1 sources in context.  
**Confidence contribution:** High within institutional scope; medium when used to interpret external matters.

### Tier 3: Expert and Professional Sources
**Authority level:** Medium-high  
**Examples:** Legal opinions, accredited qualification records, professional certifications, peer-reviewed analysis, industry standards (ISO, NQF standards)  
**Treatment:** Used with explicit expert attribution. Disagreements between experts are noted.  
**Confidence contribution:** Medium-high.

### Tier 4: Operational Records
**Authority level:** Medium  
**Examples:** Internal meeting minutes, operational reports, correspondence, system-generated records, audit trail extracts  
**Treatment:** Used for factual claims about what happened, not for normative claims about what should happen.  
**Confidence contribution:** Medium for factual claims; low for normative claims.

### Tier 5: Secondary and Contextual Sources
**Authority level:** Low-medium  
**Examples:** Summaries, briefing notes, training materials, informal guidance, external reference material  
**Treatment:** Used only for context and orientation, not for primary claims. Always superseded by higher-tier evidence when available.  
**Confidence contribution:** Low.

---

## How Evidence Tier Affects Confidence Scoring

The confidence score for a G.O.D.S Intelligence response has two dimensions:
1. **Evidence confidence:** How strong is the evidence backing this response?
2. **Retrieval confidence:** How closely does the retrieved evidence match the query?

The overall confidence score is the product of these two dimensions, bounded by the minimum tier confidence:

```
evidence_confidence = weighted_average(
    source.tier_confidence * source.relevance_score
    for source in retrieved_sources
)

retrieval_confidence = semantic_similarity(query, best_source)

raw_confidence = evidence_confidence * retrieval_confidence

# Apply tier floor: if only Tier 5 sources retrieved, confidence ≤ 0.40
confidence = min(raw_confidence, tier_floor(max_tier_in_sources))
```

### Tier Confidence Floors

| Highest Tier in Response | Maximum Confidence Score |
|-------------------------|------------------------|
| Tier 1 (Constitutional) | 1.00 |
| Tier 2 (Institutional Primary) | 0.90 |
| Tier 3 (Expert/Professional) | 0.75 |
| Tier 4 (Operational) | 0.60 |
| Tier 5 (Secondary) | 0.40 |
| No sources (no retrieval) | 0.00 — refuses to answer |

---

## Corpus Curation by Tier

The corpus management system (see Chapter 02) tracks the evidence tier of every document in the corpus. When a document is uploaded, the uploader must declare its tier. A compliance officer can override the declared tier.

Documents in Tier 1 and Tier 2 require elevated upload permissions — not anyone can add a policy document to the institutional corpus. The permission required:

| Tier | Upload Permission | Verification Required |
|------|-----------------|----------------------|
| 1 | `corpus_admin` | Source URL or original document link |
| 2 | `corpus_manager` | Approval record reference |
| 3 | `corpus_editor` | Expert credential or publication reference |
| 4 | `corpus_contributor` | Internal record reference |
| 5 | `corpus_contributor` | None |

This ensures that the evidence hierarchy is maintained by the people who upload documents, not just in the response generation logic.

---

## The "Insufficient Evidence" Response

When no retrieved evidence supports a query above a minimum confidence threshold (default: 0.30), G.O.D.S Intelligence returns an `INSUFFICIENT_EVIDENCE` response:

```json
{
  "answer": null,
  "confidence": 0.0,
  "confidence_tier": "INSUFFICIENT",
  "insufficient_evidence_reason": "No corpus sources with sufficient relevance found for this query.",
  "suggestions": [
    "Try rephrasing the query",
    "Check if relevant documents have been added to the corpus",
    "Consider an external consultation if this query falls outside institutional knowledge"
  ]
}
```

The system never invents an answer when evidence is insufficient. This is an architectural guarantee, not a best-effort aspiration.
