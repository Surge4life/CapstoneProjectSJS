# UDOC — Render hosting + in-app OTA updates

How the mobile UDOC app connects to the hosted eco-system, and how a commit to GitHub `main`
goes live **in the app** without a re-install.

```
  GitHub (main)  ──push──▶  Render (auto-deploy)
                              ├─ gods-platform-core   (FastAPI API)      ▶ https://<api>.onrender.com
                              └─ gods-udoc-web         (UDOC web / PWA)   ▶ https://<web>.onrender.com
                                                                              ▲
  UDOC mobile (Capacitor WebView) ── server.url ──────────────────────────────┘
                                   loads the live web app → new deploy = new bundle on next load
```

## 1) Deploy the eco-system to Render (one-time)
1. Push this repo to GitHub.
2. Render → **New → Blueprint** → select the repo. `render.yaml` provisions two services:
   - **gods-platform-core** — the UDOC governance API (`/health`, `/auth/login`, `/decisions`, `/policy/*`, …). Render injects the git commit, exposed at **`GET /version`**.
   - **gods-udoc-web** — the UDOC web app / PWA (static build of `udoc-app`).
3. Both have `autoDeploy: true` on `main` → every push redeploys automatically.

## 2) Point the app at the hosted API
- **In-app:** the UDOC app has a Connect screen — enter your API URL (`https://<api>.onrender.com`). It is remembered (localStorage `gods_api_base`).
- **As the default (no typing):** set the default in `udoc-app/src/api.ts` (`getBase()` fallback) to your API URL and rebuild. _Give me the URL and I'll bake it in._

## 3) In-app updates (OTA) — three layers, all included
1. **Live WebView (instant):** run `udoc-mobile/use-render.sh https://<web>.onrender.com` (or use `capacitor.config.render.json`) to set `server.url`. The native app then loads the **live** Render web app, so a GitHub-main → Render deploy is live in-app on the next open. The bundled `www/` stays as an offline fallback.
2. **Service-worker auto-update:** the PWA is built with `registerType: "autoUpdate"` (vite-plugin-pwa) — a new build's service worker activates automatically.
3. **"New version deployed" banner:** the app polls `GET /version` every 60s; when the deployed commit changes it shows a gold **↻ tap to update** banner that reloads to the newest bundle.

## 4) Build the Android APK
```bash
cd udoc-mobile
./use-render.sh https://<web>.onrender.com   # optional: load the live site (OTA)
./build-apk.sh                               # needs Android SDK + JDK 17
```
(Without `use-render.sh`, the APK ships the bundled `www/` and you point it at the API via the Connect screen.)

## What I need from you to finish the wiring
- Your **Render web URL** and **API URL** (once deployed) — I'll set them as defaults and pre-fill `server.url`.
- If your service names differ from `gods-platform-core` / `gods-udoc-web`, tell me and I'll align `render.yaml` and the configs.

_Note: `render.yaml` uses the current Render blueprint schema (`runtime: python` / `runtime: static`). If Render flags a field on import, it will say which — ping me and I'll adjust._
