# Intelligence dual path · Client vs Internal

**Updated:** 2026-08-02  
**Live Admin:** https://gods-udoc-admin.onrender.com → **Intelligence** (hard-refresh for SW v7)  
**Live Client:** https://gods-udoc-client.onrender.com → **Company Knowledge** (density + demo chips)

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

| Check | Result |
|--------|--------|
| Client seed | 2 docs · Leave SOP + POPIA note · ~689 chars |
| Client ask *leave advance notice* | Grounded: **five working days** |
| Client UI | Empty-state when 0 docs · **Demo proof** chips when seeded |
| Internal | EIF paste may show as **GENERAL** until re-labelled |
| Gaps | Prefer category **EIF / GBS / CANON** so maturity % rises |

---

## Operator checklist

### Internal (staff)

1. Open Admin → hard-refresh (`intel-density.js` + SW **v7**).  
2. **Intelligence** → document list.  
3. **Re-label** dropdown: set **GENERAL → EIF** (or GBS/CANON) → **Set** (`PATCH /intel/docs/{id}`).  
4. Prefer **Category** on ingest: GBS · CANON · EIF · POLICY · SOP · CONSTITUTION.  
5. Ask using words that appear in the extract.  
6. Gap table: ABSENT / THIN / COVERED by institutional category.

### Client (tenant)

1. Sign in **`client@udoc.demo` / `client123`** (default on Client login form).  
2. **Company Knowledge** → green **Demo proof** strip if seed present.  
3. Click **Leave notice?** or **POPIA safeguards?** for grounded answers.  
4. Admin **cannot** open this surface (403) — correct.

### Governance engines (shared host, not the KB)

EVA / policy-to-code / Sentinel remain **platform** governance. Client models get **usage only** (see `CLIENT_GOVERNANCE_INTELLIGENCE.md`).

---

## Related

- `CLIENT_INTELLIGENCE.md`  
- `CLIENT_GOVERNANCE_INTELLIGENCE.md`  
- `CORPUS_NEON_VS_DRIVE.md`  
- `EDR-002-knowledge-substrate.md`  
