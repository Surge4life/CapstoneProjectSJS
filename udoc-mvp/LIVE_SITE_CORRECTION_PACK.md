# Live Site Correction Pack — capstoneprojectsjs.netlify.app

**Updated:** 2026-08-12  
**Purpose:** Paste-ready honesty + GBS four-division alignment for the public Netlify Capstone / Holdings narrative.  
**How to use:** The site is a single large `index.html` with text embedded in JS variables, template literals, and JSON. Locate each string with enough surrounding context, then replace. Do not assume a global find-replace is safe.

**Live Core (SoT for Capstone claims):** https://gods-platform-core.onrender.com  
**Assessor entry:** `udoc-mvp/CAPSTONE_ASSESSOR_PACK.md`  
**Deadline:** 30 October 2026

---

## Priority this week (human paste)

**§7 below is the highest-priority Netlify paste.** Sections 1–6 remain valid if old strings still appear on the public site.

---

## 1. UDOC status language (appears in multiple places)

**FIND (or similar):**
```
Architecture designed. No code written. No clients engaged. Build commences at seed capital close.
```
and/or
```
v9.3 IP instrument attorney-ready. Build begins at seed close.
```

**REPLACE WITH:**
```
Capstone build live: backend routes deployed and tested (gods-platform-core.onrender.com / Neon Postgres). Governance gate, EVA engine, GIS decision framework, and audit-chain issuing in production on free-tier limits. Full commercial multi-plane platform and enterprise architecture build commence at seed capital close. Zero commercial clients engaged; zero client data processed.
```

---

## 2. Nova X Quantum™ — remove entirely

**Action:** Delete the entire competitor-table row that references Nova X Quantum™. No replacement row is required.

---

## 3. Unemployment statistics (Stats SA QLFS Q1 2026)

**FIND:**
- `32.9%` (official national) → **REPLACE with `32.7%`**
- `62.4%` (youth) → **REPLACE with `60.9%`** (official youth 15–24)
- Where expanded (LU3) is shown, use **`43.7%`** and label it clearly as expanded.

**Label example:**
```
Unemployment (Q1 2026): 32.7% official · 43.7% expanded (LU3) — Stats SA QLFS Q1 2026
Youth unemployment 15–24: 60.9% official — Stats SA QLFS Q1 2026
```

---

## 4. Document count clarification

**FIND** any display of “103 documents” or mixed 73/103 without explanation.

**REPLACE / ADD one clarifying sentence near the count:**
```
73 documents were formally registered in the March 2026 master data room index. After the July 2026 GBS-SETHS Institutional Readiness Package and Canon layer, the formal primary register stands at 94 instruments. 103+ remains the count of total institutional files including all versions and supporting materials.
```

---

## 5. SA Draft AI Policy GG 54477 — withdrawal correction

**FIND** any claim that GG 54477 / Draft National AI Policy is an active framework under public comment or enforcement.

**REPLACE WITH:**
```
South Africa’s Draft National AI Policy (Government Gazette 54477, April 2026) was withdrawn by the Minister of Communications and Digital Technologies on 26 April 2026 after fabricated academic citations were identified in the draft. A revised draft is targeted for Cabinet submission around November 2026. In the interim there is no adopted binding national AI-specific legislation. POPIA remains the operative data-protection law. UDOC’s compliance design continues to reference the standing National AI Policy Framework (NAIFP, August 2024) together with POPIA, the EU AI Act, NIST AI RMF, and ISO/IEC 42001.
```

---

## 6. Introduce GBS on the homepage narrative

**Suggested short block** (insert after the four-division loop description or in the Architecture section):

```
Global Belief System (GBS) — Constitutional Doctrine Layer

GBS is the July 2026 unifying doctrine and franchise-governance layer that sits above the four divisions. It is not a religion or ideology. It is the 80% constitutional core (Twelve Pillars, CET/CTE methodology, Skills Passport, Phase 6 lifetime re-entry) that never moves, paired with a 20% localisation allowance so a licensed node can adapt language, vocational pathways, and regulatory wrapper to its jurisdiction. G.O.D.S. is the institution; GBS is the standard the institution’s franchise operates under. Full definition: The G.O.D.S. Canon and GBS-SETHS Consolidated Super Framework v3.0 (Data Room Section H / I).
```

**S.E.T.H.S. name line:** Until founder confirms the canonical expansion, either leave current homepage wording or switch to “Systematically Engineered Transfer of Human Systems” to match Framework v1/v2/v3. One sentence from founder settles this permanently.

---

## 7. GBS-UDOC four-division freeze — PRIMARY PASTE (August 2026)

**Context:** Login density closed on Core. GBS freeze live at `/gbs`. Sync the Netlify Capstone / Holdings narrative to the same honesty before external outreach.

**FIND** language that treats UDOC only as a verifier for other divisions, invents commercial Sovereign-Verified certificates, or claims franchise geographic scale / institutional AUM.

**REPLACE / ADD** near the four-division architecture or Capstone Live section:

```
Four-divisional GBS architecture (complete set)

• S.E.T.H.S. — GBS-SETHS — develops human capability
• T.S. Industries — GBS-T.S. — develops trusted systems
• M.A.D.I.B.A. / EIF — recognises exceptional individual contribution (EIF Diamond pathway)
• UDOC — GBS-UDOC — recognises exceptional systems platforms (Sovereign-Verified pathway)

Symmetry: two divisions develop (people / systems); two recognise exceptional achievement in what was built (individuals / platforms).

Sovereign-Verified is GBS-UDOC’s top systems certification tier — the parallel to EIF Diamond for individuals. Capstone status: designed_not_built (production-specified; not issued as live external certification on the free-tier environment). EVA evaluation and audit-trail infrastructure are live on gods-platform-core under Render/Neon limits.

Honesty bounds (do not exceed on public site):
• capital not_deployed
• MADIBA ledger ≠ AUM
• geographic franchise scale = post-seed (demo delivery nodes may exist)
• EIF nominate = audit trail only (no funding / no award issuance)
• zero commercial clients · zero client data processed

Live Capstone surfaces (inspectable):
• https://gods-platform-core.onrender.com/gbs — four-division freeze · pillars · nodes
• https://gods-platform-core.onrender.com/Sentinel — EVA command · fair ≠ BLOCK · biased = BLOCK
• https://gods-platform-core.onrender.com/divisions — operator loop SETHS → TS → MADIBA
• https://gods-platform-core.onrender.com/portals — controls + CITIZEN challenge
• https://gods-udoc-gateway.onrender.com/ — surface map
• https://gods-udoc-client.onrender.com/citizen.html — public AI-rights path
```

**Do not claim on the public site:** franchise geographic scale, institutional AUM, live Sovereign-Verified certificates issued, hardware-enforced governance on arbitrary cloud hosts, or commercial multi-tenant SaaS readiness.

---

## Verification after edits

1. Hard-refresh Netlify and search for old strings (Nova X, 32.9%, “no code written”, active GG 54477).
2. Confirm Capstone Live links open Core surfaces above.
3. Re-check no accidental claim of commercial clients, raised capital, or filed patents.
4. Before any external demo: re-hit `/udoc/demo/ready` then `/Sentinel` Assessor one-click (fair ≠ BLOCK, biased = BLOCK).

---

## Smoke status at pack refresh (2026-08-12)

| Check | Result |
|-------|--------|
| `GET /health` | `status: ok` |
| `GET /udoc/demo/ready` | `ready: true` (auto-healed model-001 SUSPENDED→ACTIVE) |
| EVA fair | **APPROVE** |
| EVA biased | **BLOCK** |
| Gate | `fair_neq_block` + `biased_eq_block` **true** |

---

## Related

- `udoc-mvp/CAPSTONE_ASSESSOR_PACK.md` — assessor 20-minute path  
- `udoc-mvp/SUBMISSION_TIMELINE.md` — runway to 30 Oct 2026  
- `GODS_Master_Data_Room_Index_v3_GBS.docx` — institutional register  
- `udoc-mvp/DIVISION_SURFACE_DENSITY_PLAN.md` — login density CLOSED · Capstone track open  
