# Permanent UI embed (local only)

Large static files (`sentinel.html` ~42KB, `app-client.js` ~34KB) must be committed from a full local tree.

## Sources

- Last-good commit: `cdfb7e1d` (working client + sentinel)
- BATCH variants: include `/decisions/batch` wiring

## Commands

```bash
git checkout main && git pull

# Option A — last good
curl -sL "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/cdfb7e1d/platform-core/static/sentinel.html" \
  -o platform-core/static/sentinel.html
curl -sL "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/cdfb7e1d/udoc-public/app-client.js" \
  -o udoc-public/app-client.js

# Option B — if you have BATCH artifacts locally
# cp artifacts/sentinel_EIF_BATCH.html platform-core/static/sentinel.html
# cp artifacts/app-client_BATCH.js udoc-public/app-client.js

# Verify sizes (must be >> 2KB)
wc -c platform-core/static/sentinel.html udoc-public/app-client.js

git add platform-core/static/sentinel.html udoc-public/app-client.js
git commit -m "fix(ui): permanent Sentinel + Client embeds (no bootstrap)"
git push origin main
```

After Render deploys, hard-refresh Client + open `/Sentinel` — should not show "Loading…" bootstrap flash.
