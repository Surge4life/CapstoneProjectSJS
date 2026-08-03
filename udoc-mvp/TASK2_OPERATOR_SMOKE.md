# Task 2 · Operator smoke gate (surfaces 1–5)

**Date:** 2026-08-03  
**Core:** `https://gods-platform-core.onrender.com` · commit must include `cdfb7e1d`+  
**Rule:** live APIs only · seeded `model-001` · no new user registration

## Minimum Core (already verified in automation)

| Check | Pass |
|--------|------|
| `GET /health` | ok |
| `GET /udoc/demo/ready` → ready true | model-001 ACTIVE · 5 rules |
| `POST /decisions/batch` fair/biased | fair ≠ BLOCK · biased = BLOCK |
| `GET /eif/health` · `/eif/framework` | live |
| `POST /eif/nominate` (staff) | audit LOGGED_PENDING_REVIEW |

## Surface matrix (operator hard-refresh)

| # | Surface | URL | Actions | Pass if |
|---|---------|-----|---------|---------|
| 1 | **Sentinel** | `/Sentinel` | Smoke top-bar · EVA Command → Full EVA matrix · EIF · Diamond nominate | biased=BLOCK · gate PASS · EIF log ok |
| 2 | **Client** | `gods-udoc-client` | Login client@udoc.demo · Govern → Full EVA batch · Company Knowledge chip | biased=BLOCK · SOP ask grounded |
| 3 | **Citizen** | Client `/citizen.html` | Challenge + status (public) | case_ref returned |
| 4 | **Admin** | `gods-udoc-admin` | Hard-refresh ×2 · EVA chips / batch · Intelligence | biased=BLOCK · intel load |
| 5 | **Sector** | `gods-udoc-sector` | Full EVA batch · switch PUBLIC/PRIVATE | biased=BLOCK |

## Close Task 2 when

- Rows 1–5 observed live by operator (or documented with screenshots in SMOKE_EVIDENCE_TEMPLATE)
- Core automation green (this session)

Then **Task 1** (Canon / GBS V2 volume commits) may open after offline doc finalize.

## Honesty

Pixel parity with every Netlify demo is **not** claimed. Fail-closed EVA + policy-to-code + EIF audit + dual Intelligence is the Capstone evidence spine under Neon ≤500MB.
