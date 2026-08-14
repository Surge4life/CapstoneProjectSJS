# Production density + Capstone track

**Updated:** 2026-08-14 07:20 SAST

## Density track — REOPENED (panel density)

Login parity remains in place on all operator + admin surfaces.
**Panel/KPI density residual NOT closed** — live surfaces were thinner than denser local builds:

| Surface | Live size | Denser local | Action |
|---------|-----------|--------------|--------|
| `/divisions` | ~20k | ~49k PROD | **pushing denser now** |
| `/Sentinel` | ~19k | ~39k RESTORE (older APIs) | keep live (has Assessor + chips) |
| `/portals` | ~16k | ~27k RESTORE | next session |
| `/seths` `/ts` `/madiba` `/gbs` `/eif-ui` | ~15–17k | incremental | next |
| `/udoc-admin` | ~24k | enhance via JS | residual |
| `/admin` GODS | ~185k | floating #gods-live + chips | functional |

Staff: `admin@gods.local` / `admin123` · `seths@` / `madiba@` / `ts@` gods.local / `staff123`

## Admin live status (2026-08-14)

| Surface | HTTP | Notes |
|---------|------|-------|
| `/admin` | 200 | large console + admin-gods-live.js inject |
| `/udoc-admin` | 200 | thinner; chips present |
| Protected APIs without token | 401 | expected (routes exist) |
| `constitutional/pillars` | 404 | residual alias gap |

## Capstone assessor track — OPEN in parallel

Website / Netlify §7 still **last**. Density first until operator surfaces match denser builds.

Honesty unchanged: zeros OK · MADIBA ≠ AUM · capital not_deployed · Sovereign-Verified = designed_not_built
