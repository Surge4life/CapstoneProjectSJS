# Task 2 status — DEMO PARITY (2026-07-29)

## Source of truth
- `docs/ENGINEERING_CANON.md` + Vols I–XI
- Netlify demos: `udoc-mvp/UDOC_DEMO_INVENTORY.md`
- Live: https://capstoneprojectsjs.netlify.app/#demo=<slug>

## Phase progress

| Phase | Focus | Status | Commit(s) |
|-------|--------|--------|-----------|
| **P0** | Honest reset + inventory | Done | `1f45982`, `bea3ef1` |
| **P1** | `udoc-v7-eva` → Sentinel | **Hardened** | `931d929`, `5b5757c` |
| **P2** | `mvp-1` / `mvp-2` → client | Densified | `4be3a84`, `1335729`, `8b85a6b` |
| **P3** | `udoc-v7-platform` → admin | Wired (SW) | `36325f7`, `b40ad85` |
| **P4** | platform-ui merge | Pending | — |
| **P5** | Citizen + roles | Partial | — |
| **P6** | Assessor side-by-side | Pending | — |

## P1 latest (`5b5757c`)
- Fixed HTML `esc` entities on Sentinel
- Scenario chips **auto-run** EVA on click (Fair / Biased→BLOCK / High-risk / Sovereignty)
- Smoke still asserts fair ≠ BLOCK and biased = BLOCK

## Verify after platform-core deploy
1. `/Sentinel` → Live Evaluation → click **Biased** → **BLOCK** (no extra button press)
2. Top-bar **Smoke** → all PASS
3. Client host: Govern Biased BLOCK · Bias scan · Compliance sweep
4. Admin: hard-refresh twice for SW v2 enhance

**Task 1** only after Task 2 pass.
