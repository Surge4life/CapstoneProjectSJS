# Task 2 status — DEMO PARITY (2026-07-29)

## Source of truth
- `docs/ENGINEERING_CANON.md` + Vols I–XI
- Netlify demos: `udoc-mvp/UDOC_DEMO_INVENTORY.md`
- Assessor matrix: `udoc-mvp/P6_ASSESSOR_SIDE_BY_SIDE.md`

## Phase progress

| Phase | Focus | Status | Commit(s) |
|-------|--------|--------|-----------|
| **P0** | Honest reset + inventory | Done | `1f45982` |
| **P1** | Sentinel v7-eva | Hardened | `5b5757c` |
| **P2** | Client mvp-1/2 | Densified + mini-smoke | `33bf036`, `2122670` |
| **P3** | Admin v7-platform | Densified (SW v3) | `747e25f`, `ae3168a` |
| **P4** | platform-ui features | Partial via Sentinel+admin | — |
| **P5** | Citizen on client host | Linked | `b45e733` |
| **P6** | Assessor side-by-side | Checklist live | `7bff621` |

## P2 latest (`2122670`)
Dashboard **Run client smoke** = 4 live checks:
1. `/health`
2. `/udoc/demo/ready`
3. EVA fair ≠ BLOCK
4. EVA biased = BLOCK

## Verify (after client deploy)
1. Client Dashboard → **Run client smoke** → 4/4 PASS
2. Govern → Biased → BLOCK + terminal
3. Citizen link → challenge → case_ref
4. Sentinel Smoke PASS
5. Admin hard-refresh ×2 → EVA chips

Walk `P6_ASSESSOR_SIDE_BY_SIDE.md` before closing Task 2.
**Task 1** only after Task 2 pass.
