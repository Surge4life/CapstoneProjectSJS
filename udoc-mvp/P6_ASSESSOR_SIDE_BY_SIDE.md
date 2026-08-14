# P6 — Assessor side-by-side (demo vs live)

**Demo SoT:** https://capstoneprojectsjs.netlify.app/#demo=<slug>  
**Live SoT:** Render services below · Core Neon ≤500MB · no new registration required  
**Smoke checklist:** `UDOC_SMOKE_PASS.md` · `SMOKE_EVIDENCE_TEMPLATE.md`  
**Density residual:** CLOSED 2026-08-13 (login parity all operator + admin surfaces)  
**Last API re-verify:** 2026-08-14 · health ok · demo/ready true · fair=APPROVE · biased=BLOCK

## Minimum pass rule
Each live surface must return **≥4 live function results** (API-backed, not mock) matching the demo interaction pattern.

---

### 1. Sentinel · `#demo=udoc-v7-eva`
| Demo feature | Live URL | Verify |
|---|---|---|
| Command Centre KPIs | `/Sentinel` | DEMO READY + outcome counts + recent decisions |
| Live Evaluation chips | Live Evaluation | Fair ≠ BLOCK · **Biased = BLOCK** (auto-run) |
| 6-D bars + certificate | after Evaluate | dimensions + cert id |
| Full EVA matrix | EVA Command | fair/biased/high/sov on model-001 + KPIs |
| Smoke Pass | top-bar Smoke / Assessor one-click | health · demo/ready · policy · fair · biased |
| 12 Pillars | Pillars tab | ENFORCED count |
| Staff login chips | header / login | 4-role fillLogin |

### 2. Client · `#demo=udoc-mvp-1` / `mvp-2`
| Demo feature | Live | Verify |
|---|---|---|
| Dashboard KPIs + mini-smoke | Client host | **Run client smoke** 4/4 |
| AI Registry | AI Registry | model-001 listed |
| Compliance + sweep | Compliance | sweep returns |
| Bias Monitor + scan | Bias | scan returns counts |
| Govern chips + **Full EVA batch** | Govern | Biased → BLOCK + batch KPIs |
| Cert verify + Evidence | after EVA | VALID / evidence JSON |
| Citizen entry | login + nav | `/citizen.html` no login |

### 3. Citizen · `#demo=udoc-v7-platform` screen-citizen
| Demo feature | Live | Verify |
|---|---|---|
| Home + rights banner | `/citizen.html` | SA rights banner |
| Challenge a Decision | Challenge | case_ref from Core |
| Check My Case | Status | timeline from Neon |
| Know Your Rights | Rights | 6 rights cards |
| Core health pill | top bar | citizen live / online |

### 4. Admin · Core `/udoc-admin` (preferred) + GODS `/admin`
| Demo feature | Live | Verify |
|---|---|---|
| Command Centre + boot + outcome strip | `/udoc-admin` or Admin host | DEMO READY + APPROVE/BLOCK counts |
| EVA chips + **Full EVA batch** | EVA Command | Biased BLOCK + batch terminal |
| HITL Queue + Portals dual-path | Oversight | link opens `/portals` |
| Staff login chips | login / floating #gods-live | 4-role fillLogin |
| Infra links | nav footer | Sentinel / Health / Jobs / Portals / Citizen |

### 5. Sector · Public/Private console
| Demo feature | Live | Verify |
|---|---|---|
| Overview DEMO READY + outcome KPIs | Sector host | seed banner + BLOCK/APPROVE |
| Frameworks list | Frameworks | ≥1 instrument |
| EVA chips + **Full EVA batch** | Decisions · EVA | Biased → BLOCK |
| Switch PUBLIC/PRIVATE | Switch sector | profile reload |
| Oversight → Portals | Oversight | dual-path link |

### 6. 24 Portals (Core `/portals`) + Division surfaces
| Feature | Live | Verify |
|---|---|---|
| Catalog select | `/portals` | open workspace · role chips |
| CITIZEN card | full AI-Rights UI | challenge/status |
| Control + Target | POST `/portal/{key}/control` | `live.oversight` or audit |
| Resolve | Target=`COB-…` + Close/Override | state RESOLVED/OVERRIDDEN |
| SETHS / TS / MADIBA / GBS / EIF | `/seths` `/ts` `/madiba` `/gbs` `/eif-ui` | login chips · guided path · live metrics |

---

## Fail conditions (honest)
- Simulated scores instead of live `/decisions`
- Biased scenario does not BLOCK
- New Render service beyond existing blueprint
- New user registration required for smoke path
- SPA swallows `/citizen.html`

## Task 2 close criteria
Surfaces **1–5** pass under hard-refresh on **live** Render (operator files `SMOKE_EVIDENCE_TEMPLATE.md`).  
API gates A+B verified green 2026-08-13 and 2026-08-14. Client Govern biased=BLOCK still needs one operator UI tick.

**Honesty:** zeros OK · MADIBA ≠ AUM · capital not_deployed · Sovereign-Verified = designed_not_built · website/Netlify last
