# Install G.O.D.S UDOC on your phone (no APK needed)

All four surfaces are now installable PWAs — standalone home-screen apps, served from Render over HTTPS.
Same SSO and routing as the browser; content stays fresh from the server (no rebuilds).

## Android (Chrome)
1. Open the surface you want:
   - Unified sign-on:  https://gods-udoc-gateway.onrender.com  (recommended — routes you by role)
   - Or a console directly: gods-udoc-admin / gods-udoc-client / gods-udoc-operator .onrender.com
2. Menu (⋮) ▸ **Add to Home screen** / **Install app** ▸ Install.
3. Launch from the home-screen icon — it opens standalone (no browser bar). Sign in once.

## iPhone/iPad (Safari)
1. Open the surface URL in Safari.
2. Share ▸ **Add to Home Screen** ▸ Add.
3. Launch from the icon (standalone).

## Notes
- Installable because each surface ships a web manifest + service worker + icons; verified active.
- The service worker caches only the app shell and **never** the API, so your data is always live.
- Offline: the shell loads and shows a reconnect path; live data needs a connection.
- This is the interim while the signed APK (gods-mobile) is built on your machine — both point at the same live system.
