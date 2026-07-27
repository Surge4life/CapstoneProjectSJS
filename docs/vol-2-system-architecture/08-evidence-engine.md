# Chapter 08 — Evidence Engine

## Purpose

The Evidence Engine is responsible for ranking, weighting, and scoring retrieved corpus evidence before it reaches the response synthesis step. It operationalises the Evidence Hierarchy (Volume IV, Chapter 04) as code.

---

## Location

- **Service:** Embedded in `platform-core/app/services/gods_intelligence.py` as the `EvidenceRanker` class
- **Related:** Volume IV Chapter 04 (Evidence Hierarchy) for the conceptual model

---

## The Evidence Ranker

The `EvidenceRanker` takes a list of retrieved chunks and produces a ranked, scored evidence set:

```python
@dataclass
class EvidenceItem:
    chunk_id: UUID
    doc_id: UUID
    doc_title: str
    doc_tier: int               # 1–5
    text: str
    relevance_score: float      # 0.0–1.0 (from retrieval)
    tier_weight: float          # From tier → weight mapping
    evidence_score: float       # relevance_score * tier_weight
    excerpt: str                # The most relevant sentence(s)

class EvidenceRanker:
    TIER_WEIGHTS = {1: 1.0, 2: 0.90, 3: 0.75, 4: 0.60, 5: 0.40}
    TIER_FLOORS  = {1: 1.0, 2: 0.90, 3: 0.75, 4: 0.60, 5: 0.40}

    def rank(self, chunks: list[Chunk]) -> list[EvidenceItem]:
        items = []
        for chunk in chunks:
            weight = self.TIER_WEIGHTS[chunk.doc.tier]
            score  = chunk.relevance_score * weight
            items.append(EvidenceItem(
                chunk_id=chunk.id,
                doc_id=chunk.doc_id,
                doc_title=chunk.doc.title,
                doc_tier=chunk.doc.tier,
                text=chunk.text,
                relevance_score=chunk.relevance_score,
                tier_weight=weight,
                evidence_score=score,
                excerpt=self._extract_excerpt(chunk.text, query)
            ))
        return sorted(items, key=lambda x: x.evidence_score, reverse=True)

    def compute_confidence(self, items: list[EvidenceItem]) -> tuple[float, str]:
        if not items:
            return 0.0, "INSUFFICIENT"

        top_score = items[0].evidence_score
        max_tier  = min(i.doc_tier for i in items[:3])  # Best tier in top 3
        floor     = self.TIER_FLOORS[max_tier]
        raw       = min(top_score, floor)

        if raw >= 0.80: tier_label = "HIGH"
        elif raw >= 0.60: tier_label = "MEDIUM"
        elif raw >= 0.30: tier_label = "LOW"
        else: tier_label = "INSUFFICIENT"

        return raw, tier_label
```

---

## Source Deduplication

Multiple chunks from the same document can be retrieved. The Evidence Engine deduplicates at the document level before producing the source list shown to the user:

```python
def deduplicate_sources(items: list[EvidenceItem]) -> list[SourceReference]:
    seen = {}
    for item in items:
        if item.doc_id not in seen or item.evidence_score > seen[item.doc_id].score:
            seen[item.doc_id] = SourceReference(
                doc_id=item.doc_id,
                doc_title=item.doc_title,
                doc_tier=item.doc_tier,
                score=item.evidence_score,
                excerpts=[item.excerpt]
            )
        else:
            seen[item.doc_id].excerpts.append(item.excerpt)
    return sorted(seen.values(), key=lambda x: x.score, reverse=True)
```

The user sees one source entry per document, with the most relevant excerpts from that document.

---

## Excerpt Extraction

The excerpt shown to the user is the most relevant portion of the chunk. Extraction uses sentence-level scoring:

1. Split chunk into sentences
2. Score each sentence by semantic similarity to the query
3. Return the top 1–3 sentences (max 300 characters)

This ensures that even if a large chunk was retrieved for its general relevance, the excerpt shown is the specific part that answers the question.

---

## The Hallucination Guard

The Evidence Engine enforces a strict rule: **the synthesis step only receives the evidence items, not the query rephrased or interpreted**. The LLM synthesis model is instructed:

> "Answer the following question using ONLY the evidence provided. If the evidence does not support an answer, state that the information is not available in the corpus. Do not draw on any knowledge outside the provided evidence."

The synthesis temperature is set to 0.1 (near-deterministic) for factual queries. This further reduces the risk of generating content not supported by the evidence.

The Evidence Engine does not guarantee zero hallucination — no system can. But it creates strong structural incentives against hallucination and makes any hallucination clearly attributable (the response cites sources, so a hallucinated claim will not have a supporting source citation, making it detectable).
