# P6 — Assessor side-by-side (demo vs live)

**Demo SoT:** https://capstoneprojectsjs.netlify.app/#demo=<slug>  
**Live SoT:** Render services below · Core Neon ≤500MB · no new registration required  
**Smoke checklist:** `UDOC_SMOKE_PASS.md`  
**Density wave:** 2026-07-30 — Full EVA batch on Client / Sentinel / Admin / Sector

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
| Smoke Pass | top-bar Smoke | health · demo/ready · policy · fair · biased |
| 12 Pillars | Pillars tab | ENFORCED count |

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

### 4. Admin · `#demo=udoc-v7-platform`
| Demo feature | Live | Verify |
|---|---|---|
| Command Centre + boot + outcome strip | Admin host (hard-refresh ×2 for SW **v4**) | DEMO READY + APPROVE/BLOCK counts |
| EVA chips + **Full EVA batch** | EVA Command | Biased BLOCK + batch terminal |
| HITL Queue + Portals dual-path | Oversight | link opens `/portals` |
| Infra links | nav footer | Sentinel / Health / Jobs / Portals / Citizen |

### 5. Sector · Public/Private console
| Demo feature | Live | Verify |
|---|---|---|
| Overview DEMO READY + outcome KPIs | Sector host | seed banner + BLOCK/APPROVE |
| Frameworks list | Frameworks | ≥1 instrument |
| EVA chips + **Full EVA batch** | Decisions · EVA | Biased → BLOCK |
| Switch PUBLIC/PRIVATE | Switch sector | profile reload |
| Oversight → Portals | Oversight | dual-path link |

### 6. 24 Portals (Core `/portals`)
| Feature | Live | Verify |
|---|---|---|
| Catalog select | `/portals` | open workspace |
| CITIZEN card | full AI-Rights UI | challenge/status |
| Control + Target | POST `/portal/{key}/control` | `live.oversight` or audit |
| Resolve | Target=`COB-…` + Close/Override | state RESOLVED/OVERRIDDEN |

---

## Fail conditions (honest)
- Simulated scores instead of live `/decisions`
- Biased scenario does not BLOCK
- New Render service beyond existing blueprint
- New user registration required for smoke path
- SPA swallows `/citizen.html`

## Task 2 close criteria
Surfaces **1–5** pass under hard-refresh on **live** Render. Then Task 1 (docs/ Engineering Canon volume commits) may start.
