# P6 — Assessor side-by-side (demo vs live)

**Demo SoT:** https://capstoneprojectsjs.netlify.app/#demo=<slug>  
**Live SoT:** Render services below · Core Neon ≤500MB · no new registration required  
**Smoke checklist:** `UDOC_SMOKE_PASS.md`

## Minimum pass rule
Each live surface must return **≥4 live function results** (API-backed, not mock) matching the demo interaction pattern.

---

### 1. Sentinel · `#demo=udoc-v7-eva`
| Demo feature | Live URL | Verify |
|---|---|---|
| Command Centre KPIs | `/Sentinel` | DEMO READY + outcome counts |
| Live Evaluation chips | Live Evaluation | Fair ≠ BLOCK · **Biased = BLOCK** (auto-run) |
| 6-D bars + certificate | after Evaluate | dimensions + cert id |
| Smoke Pass | top-bar Smoke | health · demo/ready · policy · fair · biased |
| Run Full EVA | EVA Command | batch table ≥1 row |
| 12 Pillars | Pillars tab | ENFORCED count |

### 2. Client · `#demo=udoc-mvp-1` / `mvp-2`
| Demo feature | Live | Verify |
|---|---|---|
| Dashboard KPIs + mini-smoke | Client host | **Run client smoke** 4/4 |
| AI Registry | AI Registry | model-001 listed |
| Compliance + sweep | Compliance | sweep returns |
| Bias Monitor + scan | Bias | scan returns counts |
| Govern scenario chips | Govern | Biased → BLOCK + terminal |
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
| Command Centre + boot | Admin host (hard-refresh ×2) | DEMO READY banner |
| EVA Command chips | Decisions / EVA | Fair / Biased terminal |
| HITL Queue label | Oversight | relabelled |
| Infra links | nav footer | Sentinel / Health / Jobs / Portals / Citizen |

### 5. Sector · Public/Private console
| Demo feature | Live | Verify |
|---|---|---|
| Overview DEMO READY | Sector host | seed banner |
| Frameworks list | Frameworks | ≥1 instrument |
| EVA scenario chips | Decisions · EVA | Biased → BLOCK |
| Switch PUBLIC/PRIVATE | Switch sector | profile reload |

### 6. Portals SaaS (optional depth)
| Feature | Live | Verify |
|---|---|---|
| Role + sector filters | Portals host | visible portal count |
| Open portal controls | drawer | control list |
| Run control | POST | toast ref |
| Citizen link | login card | opens citizen |

---

## Fail conditions (honest)
- Simulated scores instead of live `/decisions`
- Biased scenario does not BLOCK
- New Render service beyond existing blueprint
- New user registration required for smoke path
- SPA swallows `/citizen.html`

## Task 2 close criteria
Surfaces **1–5** pass under hard-refresh. Then Task 1 (docs/ Engineering Canon volume commits) may start.
