# Surface 4 · Admin browser recovery

**Status:** Server returns HTTP 200 for Admin HTML + SW + density JS. Browser “won’t load” is almost always **stuck Service Worker / cache** or free-tier cold start — not a missing deploy.

## Login (when page shows)

- Email: `admin@gods.local`
- Password: `admin123`
- API field should be `https://gods-platform-core.onrender.com`

## Fix blank / infinite load on gods-udoc-admin

1. Open the site once to wake Render (wait 30–60s if cold).
2. Chrome/Edge → DevTools (F12) → **Application** → **Service Workers** → **Unregister**.
3. Application → **Clear site data** (or clear cache for this origin).
4. Hard-refresh (Ctrl+Shift+R) **twice**.
5. After SW `pwa-v11` deploys: navigate is network-first (should stop blank cache).

Incognito window is a fast test (no SW).

## Alternate hosts (same Task 2 intent)

| URL | Role |
|-----|------|
| https://gods-udoc-admin.onrender.com/ | Primary Internal package |
| https://gods-platform-core.onrender.com/udoc-admin | Core-hosted UDOC admin SPA |
| https://gods-platform-core.onrender.com/admin | GODS constitutional admin |
| https://gods-platform-core.onrender.com/Sentinel | Already smoke-passed — EVA + policy path |

## Minimum surface-4 evidence if Admin host stays broken in browser

From any machine with auth against Core:

1. `POST /policy/runtime-matrix` gate PASS  
2. `POST /decisions/batch` fair/biased gate PASS  
3. Screenshot Sentinel or Sector batch (already green) + note “Admin host SW recovery pending”

That still proves the **Admin controller path engines** (policy + EVA) without the static Admin PWA.

## Task 2 close posture

Surfaces **1, 2, 3, 5** operator-passed. Surface **4** = engines green; UI host recovery above.
