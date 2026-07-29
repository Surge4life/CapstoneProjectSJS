# Task 2 status — DEMO PARITY (2026-07-29)

## Source of truth
- `docs/ENGINEERING_CANON.md` + Vols I–XI
- Netlify demos: `udoc-mvp/UDOC_DEMO_INVENTORY.md`
- Live demos: https://capstoneprojectsjs.netlify.app/#demo=<slug>

## Phase progress

| Phase | Focus | Status | Commit(s) |
|-------|--------|--------|-----------|
| **P0** | Honest reset + inventory | Done | `1f45982`, `bea3ef1` |
| **P1** | `udoc-v7-eva` → Sentinel Command shell | Done | `931d929` |
| **P2** | `mvp-1` / `mvp-2` → client nav + views | Done | `4be3a84`, `1335729` |
| **P3** | `udoc-v7-platform` → udoc-internal | **Wired** | `36325f7`, `b40ad85` |
| **P4** | platform-ui + sovereign-console merge | Pending | — |
| **P5** | Citizen + roles on existing hosts | Partial | — |
| **P6** | Assessor side-by-side vs demos | Pending | — |

## P3 delivery
- `udoc-internal/admin-v7-enhance.js` — v7 nav labels, Command Centre boot banner, Fair/Biased/High-risk/Sovereignty chips on EVA Command, HITL title parity, fixed `esc`, Infrastructure links (Sentinel / API Health / Jobs / 24 Portals)
- `udoc-internal/sw.js` (cache **v2**) — injects `<script src="/admin-v7-enhance.js">` into HTML navigations

### Verify (admin host)
1. Hard-refresh udoc-admin twice (so SW v2 activates)
2. Overview → **Command Centre** + DEMO READY banner
3. EVA Command → scenario chips → Biased **BLOCK**
4. HITL Queue label + cases table
5. Infra links open Sentinel / api-health / jobs / portals

## Pass criteria
1. Nav/tabs match mapped demo  
2. ≥4 primary controls return live API results (or fail-closed)  
3. Vol IX tokens  
4. Existing Render hosts only · Neon ≤500MB  

**Task 1** only after Task 2 pass.
