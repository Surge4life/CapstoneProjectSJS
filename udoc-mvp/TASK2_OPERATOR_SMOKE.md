# Task 2 · Operator smoke gate (surfaces 1–5)

**Updated:** 2026-08-03 09:45 SAST  
**Core:** https://gods-platform-core.onrender.com · deploy includes `006df18b` (Sentinel bootstrap)

## UI restore note

`sentinel.html` and `app-client.js` were briefly corrupted to placeholders. They now **bootstrap** the last-good files from commit `cdfb7e1d` (CORS `*`). Client also loads `client-batch-overlay.js` for `/decisions/batch`.

| Surface | After hard-refresh |
|---------|-------------------|
| `/Sentinel` | Bootstrap → full EVA Command Centre |
| Client `app-client.js` | Bootstrap → full Govern + batch |
| `/eif-ui` | Static EIF Diamond console (no bootstrap needed) |

## Automation verified (this session)

| Check | Result |
|--------|--------|
| `GET /health` | ok |
| `GET /version` | `006df18b` |
| `GET /eif/health` · `/eif/framework` | live |
| `GET /eif-ui` | 200 |
| `GET /Sentinel` | bootstrap HTML (not SEE_FILE) |
| `model-001` | re-ACTIVE when SUSPENDED |
| `POST /decisions/batch` fair/biased | APPROVE / BLOCK · gate PASS |

## Operator matrix (tick live)

| # | Surface | Actions | Pass if |
|---|---------|---------|---------|
| 1 | **Sentinel** | Open `/Sentinel` · wait for full UI · Smoke · Full EVA matrix · optional `/eif-ui` | biased=BLOCK · not SEE_FILE |
| 2 | **Client** | Hard-refresh · login `client@udoc.demo` · Govern → Full EVA batch | biased=BLOCK |
| 3 | **Citizen** | Client `/citizen.html` challenge | case_ref |
| 4 | **Admin** | Hard-refresh ×2 · EVA / Intelligence | biased=BLOCK · intel load |
| 5 | **Sector** | Full EVA · PUBLIC/PRIVATE | biased=BLOCK |

## Close Task 2 when

Operator ticks 1–5 **or** documents with screenshots. Core automation already green.

**Task 1** (GBS/Canon V2) stays offline until founder finalizes docs.

## Honesty

Pixel parity with every Netlify demo is not claimed. Fail-closed EVA + batch + EIF audit + dual Intelligence is the Capstone spine under Neon ≤500MB.
