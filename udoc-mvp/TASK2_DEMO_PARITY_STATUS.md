# Task 2 status — DEMO PARITY (2026-07-29)

## Source of truth
- `docs/ENGINEERING_CANON.md` + Vols I–XI
- Netlify demos: `udoc-mvp/UDOC_DEMO_INVENTORY.md`

## Phase progress

| Phase | Focus | Status | Commit(s) |
|-------|--------|--------|-----------|
| **P0** | Honest reset + inventory | Done | `1f45982` |
| **P1** | Sentinel v7-eva | Hardened | `931d929`, `5b5757c` |
| **P2** | Client mvp-1/2 | Densified | `8b85a6b`, `33bf036` |
| **P3** | Admin v7-platform | Wired (SW) | `36325f7`, `b40ad85` |
| **P4** | platform-ui merge | Pending | — |
| **P5** | Citizen on client host | **Linked** | `b45e733`, `33bf036` |
| **P6** | Assessor side-by-side | Pending | — |

## P5 latest
- Login page: **Citizen Portal · no login** → `/citizen.html`
- Client nav: **Public → Citizen Portal**
- Dashboard quick action → Citizen
- Existing `citizen.html` + Core `/citizen/*` (Neon) unchanged — no new Render service

## Verify after client deploy
1. Open client host → login card link **Citizen Portal**
2. `/citizen.html` → Challenge → Core case ref
3. Check case status by ref
4. Operator: Dashboard / Govern Biased BLOCK / Bias scan / Smoke on Sentinel

**Task 1** only after Task 2 pass.
