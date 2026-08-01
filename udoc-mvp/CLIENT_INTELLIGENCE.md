# Client Intelligence · Private Knowledge Substrate

**Updated:** 2026-08-01  
**Audience:** Capstone assessors · Client package builders  
**Neon:** text-first under ≤500MB · not a foundation-model farm  
**Authority doc for separation of layers:** `CLIENT_GOVERNANCE_INTELLIGENCE.md`

## Intent

Each **tenant** owns a private business corpus. That corpus is the **reference material** for grounded assistance and, over time, for Knowledge Compiler objects that **deterministic** UDOC / GBS-aligned engines can cite.

**Not in this path:** client agentic / generic / recursive LLMs as controllers of UDOC. Those are **Layer A** (client operational AI). UDOC is **Layer B** (governance). GODS Intelligence / GIS is **Layer C** (Holdings constitutional substrate). See `CLIENT_GOVERNANCE_INTELLIGENCE.md`.

```
Client (JWT role=client · tenant_pk set)
        │
POST /client/knowledge/ingest-text | /ingest
        │
ClientKBDoc rows WHERE tenant_pk = caller
        │
POST /client/knowledge/ask  → retrieval-grounded answer + citations
        │
(UDOC Primacy) Govern / decisions / policy — usage only for any client model
```

Staff (`admin` / `operator` / …) are **refused** on this surface (403). Internal GODS corpus remains `/intel` — separate table and path.

## Growth rule

As the client **expands the business corpus**, the **substrate** available to grounded ask (and later Compiler → engine attachment) expands. That is **document growth under governance**, not automatic LLM weight training on Neon.

## Isolation (by construction)

| Rule | Implementation |
|------|----------------|
| Every read/write filtered by `tenant_pk` | `scope_pk(user)` → `_tenant()` in router |
| Cross-tenant doc id cannot leak | `get_doc` requires matching `tenant_pk` |
| Staff cannot browse client KB via this API | platform roles → 403 |
| Audit events tagged CLIENT | `CLIENT_KB_INGEST` / `QUERY` / `REMOVE` |
| Client models cannot amend UDOC engines | Primacy controller — usage APIs only |

**Same Neon database, different rows.** Logical isolation is the Capstone model.

## API (Core · live)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/client/knowledge/state` | Doc count · chars · categories |
| GET | `/client/knowledge/docs` | List (no full body) |
| GET | `/client/knowledge/docs/{id}` | Full text (own tenant only) |
| POST | `/client/knowledge/ingest-text` | Title + text |
| POST | `/client/knowledge/ingest` | File upload (PDF/DOCX/TXT · 25MB cap) |
| POST | `/client/knowledge/ask` | Grounded ask (deterministic retrieval) |
| DELETE | `/client/knowledge/docs/{id}` | Remove own doc |

## Client UI

- **Client Web:** **Company Knowledge** (Client package only)  
- **Client App:** Intelligence / tenancy under `UDOC_PACKAGE=client`  
- Shared UDOC host for Govern / Registry / Sentinel — **KB rows tenant-private**

## What is *not* claimed

- Per-client physical DB or Neon branch  
- Client LLM fine-tune product on free tier  
- Client model control of GIS / constitutional packs  
- Staff backdoor into client documents via `/client/knowledge`  
- Equivalence of GODS Intelligence with “just another UDOC EVA call”

## How to demo

1. Sign in as **role `client`** with **`tenant_pk`**.  
2. Company Knowledge → add SOP / policy text.  
3. Ask with terms from that text → citations from **your** docs.  
4. Govern: fair ≠ BLOCK · biased = BLOCK (UDOC engines, not the KB LLM).  
5. `admin@gods.local` → **403** on Client KB (correct).

## Related

- `CLIENT_GOVERNANCE_INTELLIGENCE.md` (layers · Primacy · engines · patent posture)  
- `EDR-002-knowledge-substrate.md`  
- `platform-core/app/routers/client_knowledge.py`  
- `platform-core/app/services/client_knowledge.py`  
