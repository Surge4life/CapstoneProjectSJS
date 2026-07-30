# Task 2 status — DEMO PARITY (2026-07-30)

## Source of truth
- `docs/ENGINEERING_CANON.md` · Netlify demos
- `P6_ASSESSOR_SIDE_BY_SIDE.md` (surfaces 1–5 required)
- `UDOC_SMOKE_PASS.md`
- `PORTAL_LIVE_CORE.md`

## Phase progress

| Phase | Focus | Status | Latest commits |
|-------|--------|--------|----------------|
| **P1** | Sentinel | Density | `bc4496e` Full EVA matrix + esc fix |
| **P2** | Client | Density | `c2ada6a` Govern batch + Dashboard |
| **P3** | Admin | Density | `4c3dffe` batch + SW `v4` |
| **P4** | Sector | Density | `06fa828` Full EVA batch + KPIs |
| **P5** | Citizen | Live | public `/citizen.html` + Core `/citizen/*` |
| **P6** | Assessor matrix | Updated | this file + P6 |
| **Portals** | 24 dual-path | Complete | `bcb3ce7` data-driven OversightCase |

## Density wave (2026-07-30)

Every primary surface now has:
- Scenario chips Fair / Biased→BLOCK / High-risk / Sovereignty
- **Run Full EVA batch** (or matrix) with outcome KPIs
- Live `/decisions` only (no simulated scores)
- Prefer `model-001` · DEMO READY banner where applicable

## Close rule (unchanged)

Surfaces **1–5** green on **live** Render after hard-refresh.  
**Do not mark Task 2 complete** until biased = BLOCK is observed on Client + Sentinel + Admin + Sector.  
**Task 1** (docs/ Engineering Canon volume commits) only after Task 2.

## Honesty

Wiring + density upgrades are in repo. Live matrix pass is **operator-verified**, not assumed.
