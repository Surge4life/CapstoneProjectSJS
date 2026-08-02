# Intelligence dual path · Client vs Internal

**Updated:** 2026-08-02  
**Live Admin:** https://gods-udoc-admin.onrender.com → **Intelligence** (hard-refresh)  
**Live Client:** https://gods-udoc-client.onrender.com → **Company Knowledge**

---

## Two corpora (do not mix)

| | **Internal · GODS Intelligence** | **Client · Company Knowledge** |
|--|----------------------------------|--------------------------------|
| Host | `gods-udoc-admin` | `gods-udoc-client` |
| Login | `admin@gods.local` (staff) | `client@udoc.demo` / `client123` |
| API | `/intel/*` | `/client/knowledge/*` |
| Table | `knowledge_docs` (GODS archive) | `client_kb_docs` (`tenant_pk`) |
| Client sees it? | **No** (`client_exposed: false`) | **Own tenant only** |
| Purpose | Holdings / GBS / Canon / EIF substrate | Client business SOPs & policies |
| Neon rule | Short text extracts | Short text extracts |

Drive (~11GB) stays **external**. Neon holds working excerpts only.

---

## Live demo proof (2026-08-02)

### Client

| Check | Result |
|--------|--------|
| Seed | 2 docs · Leave SOP + POPIA · ~689 chars |
| Ask *leave advance notice* | Grounded: **five working days** |
| Admin on Client KB | **403 Forbidden** (correct isolation) |

### Internal

| Check | Result |
|--------|--------|
| Archive | 1 doc · **EIF** · 14 205 chars · Stage 1 Assistive · `client_exposed: false` |
| Gaps | **EIF = THIN** (1 doc; COVERED needs ≥2) |
| Ask *What is EIF instruction?* | Grounded + citation |
| Ask *human primacy pillar* | Grounded + citation |
| Ask *constitutional governance* | Grounded + citation |
| Re-label | `PATCH /intel/docs/{id}` GENERAL→EIF verified live |

---

## Operator checklist

### Internal (staff)

1. Admin → hard-refresh (`intel-density.js`).  
2. **Intelligence** → list; use **Re-label** → **EIF/GBS/CANON** → **Set**.  
3. Prefer category on ingest.  
4. Quick-ask chips or free text (words must appear in the extract).  
5. Gap table: ABSENT / THIN / COVERED.

### Client (tenant)

1. `client@udoc.demo` / `client123`.  
2. **Company Knowledge** → Demo proof chips.  
3. Admin cannot open this surface (403).

### Governance engines

EVA / policy-to-code / Sentinel = platform governance. Client models = **usage only**.

---

## Freeze note (Intelligence track)

Dual path is **operable for Capstone evidence**: isolation, grounded retrieval, Neon-light extracts, no LLM-as-controller. Further corpus growth = short extracts only under 500 MB.

---

## Related

- `CLIENT_INTELLIGENCE.md`  
- `CLIENT_GOVERNANCE_INTELLIGENCE.md`  
- `CORPUS_NEON_VS_DRIVE.md`  
- `EDR-002-knowledge-substrate.md`  
