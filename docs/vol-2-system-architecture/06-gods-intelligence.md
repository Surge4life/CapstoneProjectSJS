# Chapter 06 — G.O.D.S Intelligence

## Purpose

G.O.D.S Intelligence is the institutional knowledge system of the G.O.D.S ecosystem. It provides AI-powered knowledge retrieval, analysis, and synthesis across the platform's internal corpus — with constitutional boundaries enforced by the GBS Runtime.

G.O.D.S Intelligence is not a general-purpose AI. It is a constitutionally bounded institutional intelligence system. It knows what it is authorised to know and responds within what it is authorised to say.

---

## Location

- **Router:** `platform-core/app/routers/intelligence.py`
- **Router:** `platform-core/app/routers/client_knowledge.py`
- **Service:** `platform-core/app/services/gods_intelligence.py`
- **Service:** `platform-core/app/services/client_knowledge.py`
- **Engine:** `governance-engines/gods/`

---

## Architecture

G.O.D.S Intelligence is a Retrieval-Augmented Generation (RAG) system with constitutional constraints. Its architecture:

```
User Query
  ↓
Constitutional pre-check (GBS — is this query permitted?)
  ↓
Corpus retrieval (internal knowledge base — vector search)
  ↓
Evidence ranking (by confidence tier — see Volume IV)
  ↓
Response synthesis (LLM-assisted, bounded by retrieved evidence)
  ↓
Constitutional post-check (GBS — is this response permissible?)
  ↓
Confidence score calculation
  ↓
Response with: answer, evidence references, confidence, sources
```

---

## The Internal Corpus

The G.O.D.S Intelligence corpus is the institutional knowledge base. It is:
- **Owned** by the deploying institution (not by G.O.D.S Holdings or any external party)
- **Curated** — only approved documents are ingested (see Volume IV, Chapter 14)
- **Versioned** — every corpus update is recorded with who uploaded what and when
- **Audited** — every query and response is logged

The corpus is managed via the `KnowledgeDoc` model. Documents are uploaded, chunked, embedded, and stored in OpenSearch for vector retrieval.

---

## Client Corpora (Multi-Tenancy)

SaaS clients can maintain their own private corpora via the `client_knowledge` router. These are completely isolated from:
- The platform's internal corpus
- Other clients' corpora
- Any cross-tenant query path

A client corpus query only has access to:
1. Documents the client has uploaded
2. Shared knowledge that the client has explicitly licensed from the platform corpus

This is enforced at the data layer (tenant_id on every KnowledgeDoc row) and at the service layer (client_knowledge service validates tenant scope before every query).

---

## Constitutional Boundaries of Intelligence

G.O.D.S Intelligence operates within strict constitutional boundaries:

| Boundary | Rule |
|----------|------|
| Scope | Can only answer questions within its authorised corpus |
| Confidence | Must declare a confidence score; low-confidence responses are flagged |
| Attribution | Every claim must be backed by a corpus reference |
| Jurisdiction | Cannot provide legal or regulatory advice — can provide regulatory information with citation |
| Identity | Cannot impersonate individuals or entities |
| Decisions | Cannot make governance decisions — these always go through the GBS Runtime |
| Hallucination | Response is bounded to retrieved evidence — synthesis is post-retrieval, not pre-retrieval |

These boundaries are enforced by the constitutional pre-check and post-check steps in the query pipeline. A query that would require violating any of these boundaries receives a constitutional refusal response, not an attempt to answer.

---

## External Consultation (Optional, User-Initiated)

G.O.D.S Intelligence can be configured to consult external AI services when the internal corpus does not contain sufficient evidence. This is:
- **Optional** — off by default, must be explicitly enabled per deployment
- **User-initiated** — the user must explicitly request external consultation
- **Audited** — every external consultation is logged with: external service used, query sent, response received
- **Bounded** — the external response is treated as low-confidence evidence, not as authoritative

External consultation never sends PII, sensitive data, or classified information to external services. The query is sanitised before transmission. This sanitisation is automatic and audited.

---

## Response Format

Every G.O.D.S Intelligence response includes:

```json
{
  "query_id": "uuid",
  "answer": "string — synthesised response",
  "confidence": 0.82,
  "confidence_tier": "HIGH | MEDIUM | LOW | INSUFFICIENT",
  "sources": [
    {
      "doc_id": "uuid",
      "doc_title": "string",
      "excerpt": "string — relevant passage",
      "relevance_score": 0.94
    }
  ],
  "constitutional_checks": {
    "pre_check": "PASS",
    "post_check": "PASS"
  },
  "external_consultation": false,
  "timestamp": "datetime",
  "audited": true
}
```

A confidence tier of `INSUFFICIENT` means the corpus does not contain enough evidence to answer the query reliably. The system does not guess.
