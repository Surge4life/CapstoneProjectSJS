# Chapter 09 — Intelligence Endpoints

## Base Path: `/intelligence`

Intelligence endpoints provide access to G.O.D.S Intelligence — corpus management and query.

---

## Queries

### `POST /intelligence/query`

Submit an intelligence query.

**Required role:** Any authenticated user (corpus scoped to own tenant)

**Request body:**
```json
{
  "query": "What are the employer obligations under the Employment Equity Act for companies with more than 50 employees?",
  "session_id": "uuid (optional — for multi-turn context)",
  "include_platform_corpus": true,
  "top_k": 10,
  "external_consultation": false
}
```

**Response:** `200 OK`
```json
{
  "query_id": "uuid",
  "answer": "Employers with more than 50 employees or with an annual turnover above the threshold for their sector are designated employers under the Employment Equity Act (No. 55 of 1998). Designated employers must...",
  "confidence": 0.89,
  "confidence_tier": "HIGH",
  "sources": [
    {
      "doc_id": "uuid",
      "doc_title": "Employment Equity Act No. 55 of 1998",
      "doc_tier": 1,
      "excerpt": "A designated employer means an employer who employs 50 or more employees...",
      "score": 0.93
    },
    {
      "doc_id": "uuid",
      "doc_title": "Department of Employment and Labour: EEA Guidance",
      "doc_tier": 2,
      "excerpt": "Annual reporting obligations for designated employers require...",
      "score": 0.84
    }
  ],
  "pre_check_passed": true,
  "post_check_passed": true,
  "external_consultation_used": false,
  "total_ms": 287
}
```

**Constitutional refusal response (when query violates limits):**
```json
{
  "query_id": "uuid",
  "answer": null,
  "refused": true,
  "refusal_reason": "CONSTITUTIONAL_LIMIT_2",
  "refusal_explanation": "This query requests legal advice on a specific situation. G.O.D.S Intelligence provides regulatory information. Please consult a qualified legal practitioner for advice on your specific situation.",
  "suggested_alternatives": ["Ask what the law says about X", "Ask about your regulatory obligations"]
}
```

---

### `GET /intelligence/queries`

List intelligence query records for the authenticated user.

**Query parameters:** `from_date`, `to_date`, `confidence_tier`, `refused`

---

### `GET /intelligence/queries/{query_id}`

Full query record with all evidence items and confidence breakdown.

---

## Corpus Management

### `GET /client-knowledge/corpus`

List corpus documents for the authenticated user's tenant.

**Query parameters:** `tier`, `status` (`active` \| `archived`), `doc_type`, `uploaded_by`

---

### `POST /client-knowledge/corpus/upload`

Upload a document to the corpus.

**Content-Type:** `multipart/form-data`

**Form fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | The document file |
| `title` | string | Yes | Document title |
| `doc_type` | string | Yes | `policy` \| `regulation` \| `guidance` \| `research` \| `internal` \| `other` |
| `tier` | int | Yes | Evidence tier 1–5 |
| `copyright_status` | string | Yes | See Chapter 12 for valid values |
| `description` | string | No | Document description |

**Response:** `202 Accepted` — Document submitted for ingestion. Poll status via `GET /client-knowledge/corpus/{doc_id}/status`.

---

### `GET /client-knowledge/corpus/{doc_id}/status`

Ingestion status for a recently uploaded document.

**Response:**
```json
{
  "doc_id": "uuid",
  "status": "indexed | indexing | failed",
  "chunks_created": 47,
  "indexing_started_at": "2025-01-15T10:30:00Z",
  "indexed_at": "2025-01-15T10:31:15Z",
  "error": null
}
```

---

### `POST /client-knowledge/corpus/{doc_id}/archive`

Archive a corpus document (removes from retrieval, retains record).

**Required role:** `corpus_admin` or `division_admin`

---

### `POST /client-knowledge/corpus/export`

Request a full corpus export.

**Response:** `202 Accepted` — Export job started. Download URL provided when complete (poll via `GET /client-knowledge/corpus/export/{job_id}`).

---

## Corpus Health

### `GET /intelligence/health`

Intelligence system health — corpus coverage, query hit rate, calibration status.

**Required role:** `division_admin`, `compliance`, `gods_admin`

**Response:**
```json
{
  "corpus_stats": {
    "total_documents": 847,
    "total_chunks": 38420,
    "by_tier": { "1": 45, "2": 123, "3": 312, "4": 198, "5": 169 },
    "stale_documents": 12
  },
  "query_stats_30d": {
    "total_queries": 14823,
    "high_confidence_rate": 0.73,
    "insufficient_confidence_rate": 0.08,
    "refused_queries": 142
  },
  "calibration": {
    "feedback_count_30d": 234,
    "positive_rate": 0.81
  }
}
```
