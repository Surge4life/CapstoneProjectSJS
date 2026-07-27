# Chapter 10 — Auditability & Explainability

## Why Auditability Matters for AI

AI systems that cannot be audited cannot be trusted. Not because they are necessarily untrustworthy, but because trust without auditability is faith — and governance cannot be based on faith.

G.O.D.S Intelligence is designed to be audited. Every query, every response, every source citation, every confidence score is recorded. An authorised auditor can reconstruct exactly what the intelligence system said, to whom, when, based on what evidence, with what level of confidence.

---

## The Intelligence Audit Record

Every query creates an `IntelligenceQueryRecord`:

```sql
CREATE TABLE intelligence.query_records (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id            UUID NOT NULL UNIQUE,
    user_id             UUID NOT NULL REFERENCES iam.users(id),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),
    session_id          UUID NOT NULL,
    corpus_namespace    VARCHAR(100) NOT NULL,

    -- Query
    query_text          TEXT NOT NULL,
    query_hash          VARCHAR(64) NOT NULL,   -- SHA-256 of query text

    -- Response
    response_text       TEXT NOT NULL,
    confidence          DECIMAL(4,3) NOT NULL,
    confidence_tier     VARCHAR(20) NOT NULL,

    -- Sources (stored as JSONB array)
    sources             JSONB NOT NULL,
    source_count        INTEGER NOT NULL,

    -- Constitutional checks
    pre_check_result    VARCHAR(10) NOT NULL,   -- PASS | FAIL
    post_check_result   VARCHAR(10) NOT NULL,   -- PASS | FAIL
    constitutional_violations JSONB,            -- If FAIL

    -- External consultation
    external_consultation_used BOOLEAN NOT NULL DEFAULT false,
    external_service    VARCHAR(100),

    -- Performance
    retrieval_ms        INTEGER,
    synthesis_ms        INTEGER,
    total_ms            INTEGER,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_ref_id        UUID NOT NULL REFERENCES audit.audit_refs(id)
);
```

This record is created atomically with the response delivery. The query cannot be answered without creating the audit record.

---

## Explainability at Every Level

G.O.D.S Intelligence provides explainability at three levels:

### Level 1: Response-Level Explainability (user-facing)

Every response includes:
- The answer
- The confidence tier and score
- The sources used (with excerpts)
- Whether external consultation was used

This is always shown to the user in the UI.

### Level 2: Evidence-Level Explainability (accessible via UI)

The user can expand any source citation to see:
- The full document title and metadata
- The specific excerpt retrieved
- The evidence tier of the document
- The relevance score for this source in this query

### Level 3: System-Level Explainability (accessible to compliance officers)

Compliance officers can access the full query audit record, including:
- The raw retrieved chunks before deduplication
- The evidence ranker scores for each chunk
- The pre-check and post-check results
- Whether any constitutional limits were triggered (and which ones)
- The synthesis prompt used (the instruction given to the synthesis model)
- The raw synthesis output before post-check

---

## Explainability for Refused Queries

When the system refuses to answer (constitutional pre-check fails), the refusal is itself explainable:

```json
{
  "query_id": "uuid",
  "answer": null,
  "refused": true,
  "refusal_reason": "CONSTITUTIONAL_LIMIT_6",
  "refusal_explanation": "This query requests content that would constitute legal advice. G.O.D.S Intelligence provides regulatory information but cannot advise on specific legal situations. Please consult a qualified legal practitioner.",
  "suggested_alternatives": [
    "Ask about what the law says on this topic (regulatory information)",
    "Ask about what governance records exist related to this matter"
  ]
}
```

The user knows why they were refused. The refusal is logged with the same audit record as a successful response.

---

## Audit Access Control

| Record Type | Who Can Access |
|------------|---------------|
| Own query records | The querying user |
| Division query records | `division_admin`, `compliance` |
| All query records | `gods_admin`, `external_auditor` |
| Constitutional violation records | `compliance`, `gods_admin` |

Query record access is itself logged. An auditor reading query records creates an audit record of that access.
