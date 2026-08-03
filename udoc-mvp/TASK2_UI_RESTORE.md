# Task 2 UI restore (critical)

## What happened
`platform-core/static/sentinel.html` and `udoc-public/app-client.js` on `main` were reduced to placeholders (`SEE_FILE` / `// PLACEHOLDER`) during a tool push. Core API (`/eif`, `/decisions/batch`) remains healthy.

## Last good commit for both files
`cdfb7e1d` (sizes: sentinel ~39287 · app-client ~33928)

## Restore (git push access required)

```bash
git checkout main && git pull
curl -sL "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/cdfb7e1d/platform-core/static/sentinel.html" -o platform-core/static/sentinel.html
curl -sL "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/cdfb7e1d/udoc-public/app-client.js" -o udoc-public/app-client.js
# Optional: use workspace BATCH artifacts if available (EIF nav + batch already patched)
git add platform-core/static/sentinel.html udoc-public/app-client.js
git commit -m "fix(ui): restore Sentinel + app-client after placeholder corruption"
git push origin main
```

## Already live (API)
- `GET /eif/framework` · `POST /eif/nominate`
- `POST /decisions/batch` fair APPROVE / biased BLOCK
- `udoc-mvp/TASK2_OPERATOR_SMOKE.md`
- `platform-core/static/eif.html` · route `/eif-ui` after Core deploy

## After restore — operator smoke
Surfaces 1–5 per `TASK2_OPERATOR_SMOKE.md` (hard-refresh).
