# P6 — Assessor side-by-side (demo vs live)

**Demo SoT:** https://capstoneprojectsjs.netlify.app/#demo=<slug>  
**Live SoT:** Render services below · Core Neon ≤500MB · no new registration required

## Minimum pass rule
Each live surface must return **≥4 live function results** (API-backed, not mock) matching the demo interaction pattern.

---

### 1. Sentinel · `#demo=udoc-v7-eva`
| Demo feature | Live URL | Verify |
|---|---|---|
| Command Centre KPIs | `/Sentinel` | DEMO READY + outcome counts |
| Live Evaluation chips | Live Evaluation tab | Fair ≠ BLOCK · **Biased = BLOCK** (auto-run) |
| 6-D bars + certificate | after Evaluate | dimensions + cert id |
| Smoke Pass | top-bar Smoke | health · demo/ready · policy · fair · biased |
| Run Full EVA | EVA Command | batch table ≥1 row |
| 12 Pillars | Pillars tab | ENFORCED count |

### 2. Client · `#demo=udoc-mvp-1` / `mvp-2`
| Demo feature | Live | Verify |
|---|---|---|
| Dashboard KPIs | Client host | APPROVE/BLOCK/ESCALATE + seed banner |
| AI Registry | AI Registry | model-001 listed |
| Compliance frameworks + sweep | Compliance | sweep button returns |
| Bias Monitor + scan | Bias | scan returns counts |
| Govern scenario chips | Govern | Biased → BLOCK + terminal |
| Sovereignty | Sovereignty | ZA jurisdiction |
| Citizen entry | login link + nav | `/citizen.html` no login |

### 3. Citizen · `#demo=udoc-v7-platform` screen-citizen
| Demo feature | Live | Verify |
|---|---|---|
| Home + rights banner | `/citizen.html` | SA rights banner |
| Challenge a Decision | Challenge | case_ref from Core |
| Check My Case | Status | timeline from Neon |
| Know Your Rights | Rights | 6 rights cards |
| Core health pill | top bar | citizen live / core online |

### 4. Admin · `#demo=udoc-v7-platform`
| Demo feature | Live | Verify |
|---|---|---|
| Command Centre label + boot | `/udoc-admin` (hard-refresh ×2) | DEMO READY banner |
| EVA Command chips | Decisions / EVA | Fair / Biased terminal output |
| HITL Queue label | Oversight | relabelled |
| Infra: Sentinel / Health / Jobs / Portals / Citizen | nav footer | links open |

---

## Fail conditions (honest)
- Simulated scores instead of live `/decisions`
- Biased scenario does not BLOCK
- New Render service added beyond quota
- New user registration required for smoke path
- SPA swallows `/citizen.html`

## Task 2 close criteria
All four surfaces pass the table above under hard-refresh. Then Task 1 (docs/ Engineering Canon volume commits) may start.
