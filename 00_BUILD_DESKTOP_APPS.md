> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# Building the G.O.D.S Desktop (.exe) Applications

Five desktop apps via Electron. Each opens your live G.O.D.S site in a native window and
connects live to your deployed backend — no stale bundles.

| App | Build dir | Window opens |
|---|---|---|
| UDOC Control | udoc-desktop | platform-core (API/docs) |
| SETHS | seths-desktop | portals site |
| MADIBA | madiba-desktop | portals site |
| TS Industries | ts-desktop | portals site |
| GODS Portals | portals-desktop | portals site |

(SETHS/MADIBA/TS point at the portals site by default since those are the live ones; once you
deploy dedicated sites for each, edit APP_URL in that project's main.js — one line.)

## Prerequisites (your Windows desktop)
- Node.js 18+ — https://nodejs.org   (that's all; Electron downloads itself)

## Build any .exe
```bash
cd portals-desktop        # or udoc-/seths-/madiba-/ts-desktop
npm install
npm run dist
```
Produces in `release/`:
- an **installer** `.exe` (Start-menu + desktop shortcut), and
- a **portable** `.exe` (double-click to run, no install).

## Test instantly (no build)
```bash
cd portals-desktop && npm install && npm start
```
Opens the app in a desktop window right away.

## Two ways to get desktop apps (you have both)
1. **PWA install (now, zero build):** open the live site in Edge/Chrome → Install icon in the
   address bar → installs as a standalone desktop app with its own icon + Start-menu entry.
2. **Electron .exe (this):** real distributable `.exe` files you can share/install.

## Why not pre-compiled here
Electron downloads its runtime binary on first install; the build sandbox is firewall-blocked
from that download (same limit as the Android SDK). On your desktop it just works.
