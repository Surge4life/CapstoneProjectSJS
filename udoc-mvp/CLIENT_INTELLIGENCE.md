# Client Intelligence · Private Knowledge Substrate

**Updated:** 2026-07-31  
**Audience:** Capstone assessors · Client package builders  
**Neon check (2026-07-31):** ~**35 MB** used of 500 MB free · compute ACTIVE — headroom for text corpus, not bulk media archives.

## Intent (EDR-002)

Each **tenant** owns a private knowledge base. Answers are grounded only in that tenant’s active documents. This is the Capstone slice of “own your intelligence” — not a shared GODS internal corpus and not a rented general LLM product claim.

```
Client (JWT role=client · tenant_pk set)
        │
POST /client/knowledge/ingest-text | /ingest
        │
ClientKBDoc rows WHERE tenant_pk = caller
        │
POST /client/knowledge/ask  → retrieval-grounded answer + citations
```

Staff (`admin` / `operator` / …) are **refused** on this surface (403). Internal GODS corpus remains `/intel` — separate table and path.

## Isolation (by construction)

| Rule | Implementation |
|------|----------------|
| Every read/write filtered by `tenant_pk` | `scope_pk(user)` → `_tenant()` in router |
| Cross-tenant doc id cannot leak | `get_doc` requires matching `tenant_pk` |
| Staff cannot browse client KB via this API | `scope_pk` returns `None` for platform roles → 403 |
| Audit events tagged CLIENT | `CLIENT_KB_INGEST` / `QUERY` / `REMOVE` |

**Same Neon database, different rows.** Not a second Neon project per client (would exhaust free quota). Logical isolation is the Capstone model; proven automated cross-tenant tests remain a P1 gap (`UDOC_SAAS_READINESS_GAP.md`).

## API (Core · already live)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/client/knowledge/state` | Doc count · chars · categories |
| GET | `/client/knowledge/docs` | List (no full body) |
| GET | `/client/knowledge/docs/{id}` | Full text (own tenant only) |
| POST | `/client/knowledge/ingest-text` | Title + text |
| POST | `/client/knowledge/ingest` | File upload (PDF/DOCX/TXT · 25MB cap) |
| POST | `/client/knowledge/ask` | Grounded ask |
| DELETE | `/client/knowledge/docs/{id}` | Remove own doc |

## Client UI

- **Client Web:** `udoc-public` → **Company Knowledge** (Client package only)  
- **Client App:** Intelligence / tenancy tabs under `UDOC_PACKAGE=client`  
- Rest of UDOC (Govern, Registry, Sentinel, portals) stays on shared Core governance host — **only KB rows are tenant-private**.

## What is *not* claimed

- Per-client physical database or separate Neon branch per tenant  
- Unlimited file corpora on free 500MB  
- Finished custom foundation-model training product  
- Staff backdoor into client documents via `/client/knowledge`

## How to demo

1. Sign in as a user with **role `client`** and a real **`tenant_pk`** (not platform admin).  
2. Client → Company Knowledge → add text or upload a small policy/SOP.  
3. Ask a question using terms from that text → citations from **your** docs only.  
4. `admin@gods.local` will correctly get **403** on this surface (staff use `/intel`).

## Related

- `EDR-002-knowledge-substrate.md`  
- `platform-core/app/routers/client_knowledge.py`  
- `platform-core/app/services/client_knowledge.py`  
- `ENGINEERING_ROADMAP_CAPSTONE.md` phase D  
