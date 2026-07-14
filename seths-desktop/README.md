# SETHS — Desktop App (.exe via Electron)

Wraps the live SETHS site in a native desktop window. It loads your deployed
G.O.D.S site directly, so the desktop app is always current and connects live to your backend.

Default URL: `https://gods-portals.onrender.com` (override with the GODS_URL env var, or edit APP_URL in main.js).

## Build the .exe (on your Windows desktop — Node 18+ installed)
```bash
cd seths-desktop
npm install
npm run dist          # builds an installer .exe + a portable .exe into release/
```
Output in `release/`:
- `SETHS Setup 1.0.0.exe`  — installer (creates Start-menu + desktop shortcut)
- `SETHS 1.0.0.exe`        — portable (run directly, no install)

## Test before building
```bash
npm install
npm start             # opens the app in a desktop window immediately
```

## Notes
- Electron downloads its runtime on first `npm install` (couldn't happen in the build sandbox;
  works on your machine). That's why this isn't pre-compiled.
- Free-tier backend sleeps after 15 min idle; if the window shows "could not reach", wait ~30s
  and reopen while it wakes.
