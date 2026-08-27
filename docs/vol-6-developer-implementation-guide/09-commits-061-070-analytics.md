# Chapter 09 — Commits 061–070: G.O.D.S Intelligence & Analytics

## Overview

This batch builds the intelligence system (corpus, retrieval, synthesis) and the analytics/reporting layer.

---

## Commit 061: `[DB] MIGRATE: Add intelligence schema — knowledge docs, query records, calibration`

**What:**
- `platform.knowledge_docs` — corpus document metadata
- `platform.knowledge_chunks` — chunk tracking table
- `intelligence.query_records` — full query audit records
- `intelligence.calibration_records` — user feedback for calibration

---

## Commit 062: `[CORE] ADD: Corpus ingestion pipeline`

**What:** `gods_intelligence.py` — corpus management:
- `upload_document()` — validate, extract text, chunk, embed, index
- `update_document()` — create new version, re-index
- `archive_document()` — mark archived, remove from retrieval
- `get_corpus_health()` — freshness, coverage, query hit rate metrics

---

## Commit 063: `[CORE] ADD: Retrieval service — hybrid BM25 + vector search`

**What:**
- OpenSearch integration: k-NN vector search + BM25 keyword search
- Reciprocal Rank Fusion for result merging
- Tier-weighted evidence ranking (EvidenceRanker class)
- Confidence score computation (evidence_confidence × retrieval_confidence)

---

## Commit 064: `[CORE] ADD: Intelligence query pipeline — pre-check, retrieve, synthesise, post-check`

**What:** Complete intelligence query flow:
- Constitutional pre-check (10 constitutional limits evaluated)
- Namespace-scoped retrieval
- Synthesis (LLM call with evidence-only instruction)
- Constitutional post-check (claim attribution verification)
- Query record creation
- Response delivery with confidence and source citations

---

## Commit 065: `[CORE] ADD: Client knowledge service — multi-tenant corpus management`

**What:** `client_knowledge.py`:
- Tenant corpus isolation
- Knowledge pack licensing
- Tenant corpus limits enforcement
- Corpus export endpoint

---

## Commit 066: `[UI] ADD: Intelligence console in platform-web`

**What:** Intelligence section of the admin console:
- Corpus management: upload, manage, archive documents
- Query log viewer: browse all intelligence queries
- Calibration dashboard: confidence accuracy tracking
- Coverage analysis: identify query categories with low hit rates

---

## Commit 067: `[DB] MIGRATE: Add analytics and reporting schema`

**What:**
- `analytics.report_requests` — report generation queue
- `analytics.report_records` — generated report metadata
- `analytics.bias_scores` — per-employer bias tracking
- `analytics.governance_metrics` — aggregated governance metrics (daily)

---

## Commit 068: `[CORE] ADD: Analytics engine — metrics, bias detection, reporting`

**What:** `analytics_engine.py`:
- Governance metrics aggregation (daily batch)
- Employer bias score computation (weekly batch)
- On-demand report generation
- Scheduled reports (APScheduler)
- Report storage and signed URL generation

---

## Commit 069: `[CORE] ADD: Governance API router — compliance dashboards and reporting`

**What:** `platform-core/app/routers/analytics.py`:
- `GET /analytics/governance-summary` — live governance metrics
- `POST /analytics/reports/generate` — on-demand report generation
- `GET /analytics/reports/{id}` — report status and download
- `GET /analytics/bias-scores` — employer bias score overview (compliance role)

---

## Commit 070: `[TEST] ADD: Intelligence and analytics tests`

**What:**
- Corpus ingestion pipeline (upload → index → retrieve)
- Hybrid search accuracy tests (known-answer query set)
- Constitutional pre-check and post-check enforcement
- Confidence score computation
- Report generation (mock data)
- Bias score computation

`tests/test_intelligence.py` — 30 test cases  
`tests/test_analytics.py` — 15 test cases
