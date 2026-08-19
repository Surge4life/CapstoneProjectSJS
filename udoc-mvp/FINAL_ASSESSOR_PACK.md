# Final Assessor Pack · G.O.D.S Capstone
## Single entry · reading order · live hyperlinks

**Institution:** G.O.D.S Holdings (Pty) Ltd (proposed)  
**Public site:** https://capstoneprojectsjs.netlify.app/  
**Submission target:** **30 October 2026** only  
**Stack:** Free-tier Render + Neon · inspectable Capstone build  
**Density:** Operator surfaces **FROZEN** (see DENSITY_FREEZE.md)

---

## 0. Start here (5 minutes)

| Priority | Open | Why |
|----------|------|-----|
| 1 | https://capstoneprojectsjs.netlify.app/ | Doctrine · four-division narrative |
| 2 | [CAPSTONE_BOOK_CORPUS_GLM_NARRATIVE.md](./CAPSTONE_BOOK_CORPUS_GLM_NARRATIVE.md) | Book → corpus → GLM (deterministic HITL, not LLM) |
| 3 | This file | Live path + honesty + links |
| 4 | Procedure A below | Prove API smoke in 5 minutes |

**Credentials (demo only — single source):** see [ASSESSOR_DEMO_ACCESS.md](./ASSESSOR_DEMO_ACCESS.md)

| Account | Password |
|---------|----------|
| `admin@gods.local` | `admin123` |
| `seths@gods.local` / `ts@gods.local` / `madiba@gods.local` | `staff123` |

---

## 1. What this Capstone is (and is not)

### Is

- **G.O.D.S Holdings** = institution  
- **GBS** = constitutional / franchise standard above divisions (**not** a fifth operating division)  
- **Closed loop:** **S.E.T.H.S → T.S Industries → UDOC → M.A.D.I.B.A**  
- Live, inspectable governance + division operator surfaces on free-tier infrastructure  
- Deterministic **UDOC** decision path (EVA · policy · audit) — LLM is **not** the controller  
- **GLM** = Deterministic Human-In-The-Loop Governance Model (corpus + rules); optional LLM is Layer A only — see [CAPSTONE_BOOK_CORPUS_GLM_NARRATIVE.md](./CAPSTONE_BOOK_CORPUS_GLM_NARRATIVE.md) · pilot [GLM_CAPSTONE_PILOT_SLICE.md](./GLM_CAPSTONE_PILOT_SLICE.md) · seed [glm/](./glm/)

### Is not

- Commercial-scale operations, raised AUM, or deployed capital  
- A claim that Intelligence (corpus ask) is the product  
- Patent **granted** (claim families attorney-ready ≠ granted)  
- Continuous free-tier uptime SLA  

Full bounds: [LIMITATIONS_REGISTER.md](./LIMITATIONS_REGISTER.md)

---

## 2. Ten live environments

| # | Environment | URL |
|---|-------------|-----|
| 1 | **Core** | https://gods-platform-core.onrender.com |
| 2 | **Internal** (staff SPA · **≠ Operator**) | https://gods-platform-internal.onrender.com/ |
| 3 | **Gateway** | https://gods-udoc-gateway.onrender.com/ |
| 4 | **Client** | https://gods-udoc-client.onrender.com/ |
| 5 | **Citizen** | https://gods-udoc-client.onrender.com/citizen.html |
| 6 | **Sector** | https://gods-udoc-sector.onrender.com/ |
| 7 | **UDOC Admin host** | https://gods-udoc-admin.onrender.com/ |
| 8 | **Operator** (**≠ Internal**) | https://gods-udoc-operator.onrender.com/ |
| 9 | **Web / App** | https://gods-udoc-web.onrender.com/ |
| 10 | **Portals SaaS** | https://gods-udoc-portals.onrender.com/ |

Cold start: first hit may take 30–60s on free Render.

Website paste map: [LIVE_SITE_CORRECTION_PACK.md](./LIVE_SITE_CORRECTION_PACK.md)

---

## 3. Procedure A — API smoke (required)

| Step | Link / action | Pass |
|------|---------------|------|
| A1 | https://gods-platform-core.onrender.com/health | `status: ok` |
| A2 | https://gods-platform-core.onrender.com/udoc/demo/ready | `ready: true` |
| A3 | POST `/decisions/batch` `{"scenarios":["fair","biased"]}` | fair ≠ BLOCK · **biased = BLOCK** |

**Dated evidence:** [SMOKE_EVIDENCE_2026-08-16.md](./SMOKE_EVIDENCE_2026-08-16.md) — PASS on 2026-08-16.

---

## 4. Procedure B — Four-division live path (15–20 min)

| Step | URL | Login | Verify |
|------|-----|-------|--------|
| B1 | https://gods-platform-core.onrender.com/gbs | — | Four-division freeze · honesty tags |
| B2 | https://gods-platform-core.onrender.com/seths | seths@ / staff123 | Metrics · enrol/advance |
| B3 | https://gods-platform-core.onrender.com/ts | ts@ / staff123 | Metrics/projects · handoff |
| B4 | https://gods-platform-core.onrender.com/Sentinel | — | EVA fair APPROVE · **biased BLOCK** |
| B5 | https://gods-platform-core.onrender.com/madiba | madiba@ / staff123 | Ledger · **≠ AUM** · not_deployed |
| B6 | https://gods-platform-core.onrender.com/divisions | staff | Combined operator |

Detail: [ASSESSOR_ENVIRONMENTAL_PROCEDURES.md](./ASSESSOR_ENVIRONMENTAL_PROCEDURES.md)

---

## 5. Procedure C — Governance & internal

| Step | URL | Verify |
|------|-----|--------|
| C1 | https://gods-platform-core.onrender.com/admin | GODS Admin · multi-page · **not Intelligence-only** |
| C2 | https://gods-platform-core.onrender.com/udoc-admin | UDOC controller · Layers / Control |
| C3 | https://gods-platform-core.onrender.com/portals | Catalog · control · CITIZEN path |
| C4 | https://gods-platform-internal.onrender.com/ | Launcher: Overview · SETHS · TS · MADIBA · UDOC · Intelligence |

---

## 6. Procedure D — Client / public (optional)

| Step | URL |
|------|-----|
| D1 | https://gods-udoc-gateway.onrender.com/ |
| D2 | https://gods-udoc-client.onrender.com/ |
| D3 | https://gods-udoc-client.onrender.com/citizen.html |
| D4 | https://gods-udoc-sector.onrender.com/ |

---

## 7. Honesty checklist (visible on live UI)

- [ ] Capital **not_deployed**  
- [ ] MADIBA **≠ AUM**  
- [ ] Sovereign-Verified **designed_not_built** where stated  
- [ ] UDOC **deterministic** controller  
- [ ] Free-tier / demo scale · zeros OK  
- [ ] Pre-registration · planning estimates not trading history  

---

## 8. Full document reading order

| # | Document | Role |
|---|----------|------|
| 1 | **FINAL_ASSESSOR_PACK.md** (this file) | Entry + hyperlinks |
| 2 | ASSESSOR_ENVIRONMENTAL_PROCEDURES.md | Step-by-step A–D |
| 3 | ASSESSOR_LIVE_TEST_PACK.md | Link index |
| 4 | ASSESSOR_DEMO_ACCESS.md | Credentials only |
| 5 | SMOKE_EVIDENCE_2026-08-16.md | Dated API smoke |
| 6 | CAPSTONE_ASSESSOR_PACK.md | Narrative context |
| 7 | LIVE_SITE_CORRECTION_PACK.md | Netlify alignment |
| 8 | DENSITY_FREEZE.md | Density closed |
| 9 | VERIFY_REDTEAM_CHECKLIST.md | High-stakes claims gate |
| 10 | GODS_INTELLIGENCE_OPERATING_METHOD.md | Method layer under UDOC |
| 11 | LIMITATIONS_REGISTER.md | Explicit non-claims |
| 12 | CAPSTONE_BOOK_CORPUS_GLM_NARRATIVE.md | Book → corpus → GLM |
| 13 | glm/GLM_INTEL_SEED_CHUNKS.md | Neon-safe intel seed |

---

## 9. Recommended 30-minute session

1. Site overview (5 min)  
2. Procedure A — smoke (5 min)  
3. Procedure B — four-division path (15 min)  
4. Procedure C1 + C4 — Admin + Internal (5 min)  

---

## 10. Contact / Capstone frame

- Founder architecture: public site · Data Room instruments  
- Live Capstone = proof of **controlled, inspectable governance loop**, not commercial certainty  
- Deadline stamp: **30 October 2026** only  

---

*End of Final Assessor Pack · open the live URLs · verify smoke · walk the loop*
