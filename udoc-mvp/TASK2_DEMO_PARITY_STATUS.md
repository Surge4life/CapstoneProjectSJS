# Task 2 status — HONEST RESET (2026-07-29)

## What was wrong

Prior session notes (including Session 14 “series closed”) overstated production readiness.

- Wiring backend endpoints to simplified HTML shells is **not** Task 2 completion.
- Live UIs do **not** match Netlify demo interaction density, navigation, or visual chrome.
- The Engineering Canon under `docs/` (Volumes I–XI) was not used as the build authority.
- Smoke checklists and seed packs are useful ops hygiene — they are **not** demo parity.

## Source of truth (authoritative)

| Source | Path / artefact |
|--------|------------------|
| Engineering Canon index | `docs/ENGINEERING_CANON.md` |
| UI/UX law | `docs/vol-9-ui-ux-design-system/` |
| Implementation order | `docs/vol-6-developer-implementation-guide/` |
| API contracts | `docs/vol-8-api-reference/` |
| DB design | `docs/vol-7-database-design/` |
| Netlify demos (7) | `SJSCAPSTONE_Netlify_Deploy_v5_GBS.zip` → `index.html` `#demo=…` |
| Demo inventory extract | `udoc-mvp/UDOC_DEMO_INVENTORY.md` |

Live site for demos: `https://capstoneprojectsjs.netlify.app/#demo=<slug>`

## The 7 demos (must drive live UI)

| Slug | Title | Approx size | Primary live target |
|------|-------|-------------|---------------------|
| `udoc-mvp-1` | International Standards Dashboard | small | udoc-public Dashboard + Compliance |
| `udoc-mvp-2` | Multi-Framework Compliance Engine | medium | udoc-public Compliance + sector |
| `udoc-v7-platform` | **Featured** Full Platform | **very large** (~295KB body) | udoc-internal + role portals |
| `udoc-v7-eva` | EVA Multi-Dimensional Evaluation | large | Decisions/EVA on all surfaces + Sentinel |
| `udoc-v5-sa` | SA Architecture Lineage | large | lineage panels internal |
| `udoc-platform-ui` | Operational Control v9.3 | large | udoc-internal ops density |
| `udoc-sovereign-console` | Sovereign Governance Console | large | udoc-internal + /admin separation |

### v7 platform nav chrome that live UI still lacks (examples)

Command Centre · AI Registry · Audit Trail · HITL Queue · Compliance · Sovereignty · Incident Command · EVA Command · EVA Audit Log · Bias Monitor · Bill of Rights · Citizen Portal · multi-role launch (Super Admin → Citizen) · Live Audit Stream · full registry tables with SPD/HITL columns.

Citizen demo path (`screen-citizen`): Challenge · Case Status · Explanation · Rights · Help — already partially on `udoc-public/citizen.html`; must reach full tab interaction parity.

## Pass criteria for Task 2 (UDOC only)

A surface is **not** done until:

1. Tab / nav structure mirrors the mapped demo (not a 5-item slim sidebar).
2. Pressing each primary function control returns a **true live** API result (or explicit fail-closed), minimum **4 interactive returns** per surface.
3. Visual language follows Vol IX tokens (navy `#060E1C` / gold `#C9A84C` / status colours / dense professional layout).
4. No new Render services beyond existing quota; fold into client / internal / core only.
5. Neon ≤500MB respected (no bulk user signup).

## Multi-session execution order (UDOC until dusted)

| Phase | Work |
|-------|------|
| **P0** | This reset + demo inventory (done in this commit) |
| **P1** | `udoc-v7-eva` parity on Sentinel + public Decisions (Command Centre density, Run Full EVA, system table) |
| **P2** | `udoc-mvp-1` + `udoc-mvp-2` full chrome on udoc-public Dashboard/Compliance |
| **P3** | `udoc-v7-platform` Command Centre shell on udoc-internal (nav tree + live modules) |
| **P4** | `udoc-platform-ui` + `udoc-sovereign-console` density merge into internal |
| **P5** | Citizen + role-scoped views without extra Render services |
| **P6** | Assessor walkthrough against demos side-by-side |

**Task 1** (full Engineering Canon / MD implementation depth across GODS ecosystem) starts only after Task 2 pass criteria above are met for UDOC surfaces.

## Constraint reminder

Render ~20 services · Neon 500MB · existing hosts only · docs/ is law · demos are the UI acceptance test.
