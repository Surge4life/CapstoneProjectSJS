# Task 2 status — DEMO PARITY (2026-07-29)

## Source of truth
- `docs/ENGINEERING_CANON.md` + Vols I–XI
- Netlify demos: `udoc-mvp/UDOC_DEMO_INVENTORY.md`
- Live demos: https://capstoneprojectsjs.netlify.app/#demo=<slug>

## Phase progress

| Phase | Focus | Status | Commit(s) |
|-------|--------|--------|-----------|
| **P0** | Honest reset + inventory | Done | `1f45982`, `bea3ef1` |
| **P1** | `udoc-v7-eva` → Sentinel | Done | `931d929` |
| **P2** | `mvp-1` / `mvp-2` → client | **Densified** | `4be3a84`, `1335729`, `8b85a6b` |
| **P3** | `udoc-v7-platform` → admin | **Wired** | `36325f7`, `b40ad85` |
| **P4** | platform-ui merge | Pending | — |
| **P5** | Citizen + roles | Partial | — |
| **P6** | Assessor side-by-side | Pending | — |

## P2 latest (`8b85a6b`)
- Fixed HTML `esc` (entities)
- Dashboard: APPROVE / BLOCK / ESCALATE outcome KPIs from regulator summary
- Bias Monitor: live `/bias/scan` button + incident feed
- Govern: Fair / Biased→BLOCK / High-risk / Sovereignty chips + terminal EVA
- Compliance: multi-framework cards + sweep

## P3
- `admin-v7-enhance.js` + SW v2 inject on navigate
- Hard-refresh admin **twice** so SW activates

## Verify (client host after deploy)
1. Sign in → Command Dashboard (boot READY, outcome KPIs)
2. Govern → Biased → **BLOCK** + policy ENFORCED
3. Bias Monitor → Run bias scan
4. Compliance → Run sweep
5. AI Registry / Audit / Sovereignty tabs populate from live APIs

**Task 1** only after Task 2 pass.
