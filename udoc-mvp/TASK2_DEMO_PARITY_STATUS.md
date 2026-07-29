# Task 2 status — DEMO PARITY (2026-07-29)

## Source of truth
- `docs/ENGINEERING_CANON.md` + Vols I–XI
- Netlify demos: `udoc-mvp/UDOC_DEMO_INVENTORY.md`
- Assessor matrix: `udoc-mvp/P6_ASSESSOR_SIDE_BY_SIDE.md`
- Smoke checklist: `UDOC_SMOKE_PASS.md`

## Phase progress

| Phase | Focus | Status | Commit(s) |
|-------|--------|--------|-----------|
| **P0** | Honest reset + inventory | Done | `1f45982` |
| **P1** | Sentinel v7-eva | Hardened | `5b5757c` |
| **P2** | Client mvp-1/2 + mini-smoke | Densified | `2122670` |
| **P3** | Admin v7-platform | Densified (SW v3) | `747e25f` |
| **P4** | platform-ui features | Partial | — |
| **P5** | Citizen on client host | Linked | `b45e733` |
| **P6** | Assessor side-by-side | Checklist + smoke aligned | `7bff621`, `12124b3` |

## Access (existing hosts only)
- Gateway → Citizen / Portals SaaS / Sentinel links (`fa703f8`)
- Client Dashboard → **Run client smoke** 4/4
- Admin → hard-refresh ×2 for SW v3

## Task 2 close rule
Walk `P6_ASSESSOR_SIDE_BY_SIDE.md` + `UDOC_SMOKE_PASS.md` green on live Render.  
**Task 1** only after that.
