# Task 2 status — DEMO PARITY (2026-07-29)

## Source of truth
- `docs/ENGINEERING_CANON.md` + Vols I–XI
- Netlify demos: `udoc-mvp/UDOC_DEMO_INVENTORY.md`
- Live demos: https://capstoneprojectsjs.netlify.app/#demo=<slug>

## Phase progress

| Phase | Focus | Status | Commit(s) |
|-------|--------|--------|-----------|
| **P0** | Honest reset + inventory | Done | `1f45982`, `bea3ef1` |
| **P1** | `udoc-v7-eva` → Sentinel Command shell | Done (density) | `931d929` |
| **P2** | `mvp-1` / `mvp-2` → client nav + views | Done (nav + live APIs) | `4be3a84`, `1335729` |
| **P3** | `udoc-v7-platform` → udoc-internal | **In progress** | `86a53ba` (`admin-v7-enhance.js`) |
| **P4** | platform-ui + sovereign-console merge | Pending | — |
| **P5** | Citizen + roles on existing hosts | Partial (citizen.html) | — |
| **P6** | Assessor side-by-side vs demos | Pending | — |

## P3 notes
- `udoc-internal/admin-v7-enhance.js` relabels nav to v7 Command Centre language, injects Infrastructure links (Sentinel, API Health, Jobs, 24 Portals), wraps Overview with `/udoc/demo/ready` boot banner, fixes `esc`.
- **Wire:** `udoc-internal/index.html` must load `<script src="/admin-v7-enhance.js"></script>` before the service-worker block (next CONTINUE if not yet on live host).

## Pass criteria (unchanged)
1. Nav/tabs match mapped demo  
2. ≥4 primary controls return live API results (or fail-closed)  
3. Vol IX tokens  
4. Existing Render hosts only · Neon ≤500MB  

**Task 1** (full Canon / GODS ecosystem) starts only after Task 2 pass.
