# Intelligence dual path · Client vs Internal

**Updated:** 2026-08-01  
**Live Admin:** https://gods-udoc-admin.onrender.com → **Intelligence** (hard-refresh for SW v7)  
**Live Client:** https://gods-udoc-client.onrender.com → **Company Knowledge**

---

## Two corpora (do not mix)

| | **Internal · GODS Intelligence** | **Client · Company Knowledge** |
|--|----------------------------------|--------------------------------|
| Host | `gods-udoc-admin` | `gods-udoc-client` |
| Login | `admin@gods.local` (staff) | `client@udoc.demo` / tenant client |
| API | `/intel/*` | `/client/knowledge/*` |
| Table | `knowledge_docs` (GODS archive) | `client_kb_docs` (`tenant_pk`) |
| Client sees it? | **No** (`client_exposed: false`) | **Own tenant only** |
| Purpose | Holdings / GBS / Canon / EIF substrate | Client business SOPs & policies |
| Neon rule | Short text extracts | Short text extracts |

Drive (~11GB) stays **external**. Neon holds working excerpts only.

---

## Operator checklist

### Internal (staff)

1. Open Admin → hard-refresh (load `intel-density.js` + SW **v7**).  
2. **Intelligence** → confirm document list (e.g. EIF paste).  
3. Prefer **Category** `GBS` / `CANON` / `EIF` / `POLICY` when adding extracts (improves gap report).  
4. Ask using words that appear in the extract.  
5. Gap table shows ABSENT/THIN/COVERED for institutional categories.

### Client (tenant)

1. Sign in as **client** role with `tenant_pk` (demo: `client@udoc.demo` / `client123`).  
2. **Company Knowledge** → seed SOPs or paste one short SOP.  
3. Ask with terms from that text.  
4. Admin cannot open this surface (403) — correct.

### Governance engines (shared host, not the KB)

EVA / policy-to-code / Sentinel remain **platform** governance. Client models get **usage only** (see `CLIENT_GOVERNANCE_INTELLIGENCE.md`).

---

## Related

- `CLIENT_INTELLIGENCE.md`  
- `CLIENT_GOVERNANCE_INTELLIGENCE.md`  
- `CORPUS_NEON_VS_DRIVE.md`  
- `EDR-002-knowledge-substrate.md`  
