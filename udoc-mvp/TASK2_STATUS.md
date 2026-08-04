# Task 2 status — 2026-08-04 (later session)

**Operator:** Render + GitHub verified OK.

## Core automation (re-verified)

| Check | Result |
|--------|--------|
| `/health` | ok |
| `/udoc/demo/ready` | **true** · auto-heal SUSPENDED→ACTIVE |
| `/decisions/batch` gate | **PASS** |
| EIF | live |
| Admin | pwa-v8 + EIF · Diamond |
| Sector | overlay wired (`116989f7`) |

## UI recovery posture

| File | Live approach |
|------|----------------|
| `sentinel.html` | Bootstrap → loads `cdfb7e1d` full page |
| `app-client.js` | Bootstrap → `cdfb7e1d` + `client-batch-overlay.js` |

**Permanent full embeds** (replace bootstrap) should be done **from your PC** with local git so large files are not truncated:

```bash
# from repo root, with artifacts or last-good trees
cp path/to/sentinel_EIF_BATCH.html platform-core/static/sentinel.html
cp path/to/app-client_BATCH.js udoc-public/app-client.js
git add platform-core/static/sentinel.html udoc-public/app-client.js
git commit -m "fix(ui): permanent Sentinel + Client embeds"
git push origin main
```

Do **not** push PLACEHOLDER text via partial tool writes.

## Surfaces 1–5 — close Task 2

| # | Surface | Pass if |
|---|---------|---------|
| 1 | Sentinel | biased=BLOCK |
| 2 | Client | biased=BLOCK |
| 3 | Citizen | case_ref |
| 4 | Admin | biased=BLOCK + EIF nav |
| 5 | Sector | biased=BLOCK |

**Task 1** = GBS V2 / Canon offline finalize (founder).

## Honesty

Automation gate is green. Bootstrap is intentional recovery, not demo pixel claim. Neon ≤500MB.
