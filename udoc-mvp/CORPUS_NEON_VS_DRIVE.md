# Client corpus · Neon vs Google Drive (11GB)

**Updated:** 2026-08-01  
**Constraint:** Neon free ≤ **500MB** total for the whole Capstone DB  
**Observed (2026-07-31):** ~35MB used — headroom for **text extracts**, not media archives

---

## Why “unable to find in corpus” / empty answers

Client Intelligence is **retrieval-grounded**. If the tenant has **zero** `ClientKBDoc` rows (or no matching terms), the engine correctly returns that the knowledge base is empty or that no passage matched.

That is **not a Neon failure**. It means **nothing was ingested for that tenant** yet — by design when the operator refuses to dump an 11GB Drive into a 500MB database.

---

## Two stores (do not merge)

| Store | Role | What goes here |
|-------|------|----------------|
| **Google Drive (~11GB portfolio)** | Authoritative **offline / institutional** archive — patents, demos, media, full packs | Full files, large PDFs, videos, version history |
| **Neon `client_kb_docs`** | **Live Capstone substrate** for grounded ask + future Compiler objects | Short **text extracts** (SOPs, policy clauses, FAQs) — kilobytes to low megabytes per tenant |

**Rule:** Drive holds the library. Neon holds the **working excerpts** the deterministic engine can cite under free tier.

Never pipe the full 11GB portfolio into Neon. That would exhaust the Capstone database and break EVA / audit / registry for everyone.

---

## Capstone demo pattern

1. Pick **one** short SOP or policy paragraph from Drive (or invent a 200–800 word sample).  
2. Client Web → **Company Knowledge** → **Add text** (or upload a small `.txt` / short PDF).  
3. Ask using **words that appear in that text**.  
4. Expect citations from **your** docs only.

Optional: startup seed installs **tiny** demo passages for existing tenants (`gov-dsd`, `acme-bank`) so ask is demonstrable without Drive sync — still Neon-light.

---

## Post-Capstone (intent only)

- Connectors to Drive / SharePoint as **external** corpus indexes (metadata + excerpts in DB, blobs outside Neon).  
- Knowledge Compiler over curated packs, not bulk binary dump.  
- Enterprise storage tiers when commercial infra exists.

---

## Related

- `CLIENT_INTELLIGENCE.md`  
- `CLIENT_GOVERNANCE_INTELLIGENCE.md`  
- `EDR-003` free-tier limits  
- Live API: `/client/knowledge/*`  
