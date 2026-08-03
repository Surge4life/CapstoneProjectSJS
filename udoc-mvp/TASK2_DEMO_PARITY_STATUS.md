# Task 2 status — DEMO PARITY (2026-08-03)

## Source of truth
- Netlify demos · `P6_ASSESSOR_SIDE_BY_SIDE.md` · `UDOC_SMOKE_PASS.md`
- Live Core: `https://gods-platform-core.onrender.com`

## Priority vs Task 1
**Task 2 first.** Task 1 (Engineering Canon volume work / GIS–GBS production docs under GODS Holdings) starts only after Task 2 minimum live smoke is green and surfaces 1–5 are operator-checkable.

## Minimum live smoke (Core API · 2026-08-03)

| Check | Result |
|--------|--------|
| `GET /health` | ok |
| `GET /udoc/demo/ready` | **ready: true** · model-001 ACTIVE · 5 rules |
| EVA fair · model-001 | **APPROVE** |
| EVA biased · model-001 | **BLOCK** (DI + SPD policy) |
| EVA high · model-001 | **BLOCK** (risk + HITL policy) |
| Citizen health | surface live |
| Sentinel / Client / Admin hosts | HTTP 200 |

**TASK2_MIN_SMOKE = PASS** on Core API.

## Demo-seed protection (this session)
High-risk BLOCK no longer permanently sets `model-001` to BLOCKED (other models still fail-closed). Keeps Full EVA matrix re-runnable for assessors.

## Phase progress

| Phase | Focus | Status |
|-------|--------|--------|
| P1 Sentinel | Density + smoke | Live |
| P2 Client | Density + mini-smoke + KB | Live |
| P3 Admin | Density + Intelligence | Live |
| P4 Sector | Density | Live (operator UI check) |
| P5 Citizen | Public path | Live |
| P6 Assessor matrix | Doc + Core API green | **Core API green; operator hard-refresh 1–5 still recommended** |
| Portals | Dual-path | Live |

## Close rule (honest)
- **Core minimum** (health + ready + fair≠BLOCK + biased=BLOCK): **PASS 2026-08-03**
- **Full Task 2 close**: operator confirms biased=BLOCK on Client Govern + Sentinel + Admin EVA after hard-refresh
- Then **Task 1** may open (Canon / GIS–GBS documentation track)

## Honesty
Pixel parity with every Netlify demo screen is not claimed. Live fail-closed EVA + policy-to-code + dual Intelligence + portals path is the Capstone evidence spine under Neon ≤500MB.
