# Citizen / 24-User Portals — Session 1

**Date:** 2026-07-28  
**Task:** Port the UDOC demo 24-user portal functioning system into the live environment.

## Source of truth
- Demo / live code: `udoc-portals/index.html`
- APIs used (must return true for min 4 functions):
  1. `GET /access/profiles` — catalog of 24 Sovereign-Operator portals
  2. `GET /portal/{key}` — open a portal (controls, systems, activity)
  3. `POST /portal/{key}/control` — run a control on that portal
  4. `GET /access/matrix` (or `/access/profiles` matrix path) — capability matrix

## Session 1 delivered
1. **Deploy** `udoc-portals` as Render static service `gods-udoc-portals` (added to `render.yaml`).
2. **Gateway** surfaces the Portals entry (5th tile + direct link).
3. No rewrite of portal function logic — the existing console already implements the four live API loops above.

## Expected live URL (after Render picks up blueprint)
- `https://gods-udoc-portals.onrender.com`

## Session 2 (next, if needed)
- SSO hash support on `udoc-portals` (parity with operator/client)
- Verify the four endpoints against live Neon-backed core after deploy
- Any citizen-specific naming / public-facing label adjustments you require

## Honesty
This is software deployment of an existing portal console, not new hardware infrastructure. Free Render + Neon remain the capacity constraint.
