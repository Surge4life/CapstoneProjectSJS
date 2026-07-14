# UDOC Mobile Gateways — build & OTA

Mobile access and control of the entire G.O.D.S UDOC ecosystem from your phone. Each gateway is a thin
**Capacitor** Android shell whose `server.url` points at a live Render static service — an **OTA** model:
redeploy the web console and the change reaches the device on next open, **no APK rebuild needed**.

> Pre-registration forecast · G.O.D.S Holdings (Pty) Ltd (PROPOSED) · not yet registered. IP vests in Sashin J. Singh.

## What's here
- **`gods-mobile/`** — the **primary unified app** ("G.O.D.S UDOC"). `server.url = gods-udoc-gateway`.
  Sign in once → routed to your console (admin / client / operator) by role, in-app. `allowNavigation`
  whitelists all four console origins + the API so cross-console routing stays inside the webview.
  Full buildable project: `capacitor.config.json`, `package.json`, `www/` (offline splash), `android-resources/`, `build-apk.sh`.
- **`mobile-gateways/`** — per-surface **OTA config variants** for dedicated single-console apps:
  - `capacitor.config.admin.json`    → `gods-udoc-admin`    (appId `za.gods.udoc.admin`)
  - `capacitor.config.client.json`   → `gods-udoc-client`   (appId `za.gods.udoc.client`)
  - `capacitor.config.operator.json` → `gods-udoc-operator` (appId `za.gods.udoc.operator`)
- **`udoc-mobile/`** (existing) — bundles the `udoc-app` React build locally. To switch it to OTA, set
  `server.url = https://gods-udoc-web.onrender.com` in its `capacitor.config.json` (then it behaves like the others).

## Surface → live service map
| Mobile app | server.url |
|---|---|
| G.O.D.S UDOC (unified) | https://gods-udoc-gateway.onrender.com |
| UDOC Admin | https://gods-udoc-admin.onrender.com |
| UDOC Client | https://gods-udoc-client.onrender.com |
| UDOC Operator | https://gods-udoc-operator.onrender.com |
| UDOC (existing udoc-mobile, optional OTA) | https://gods-udoc-web.onrender.com |

API for all: `https://gods-platform-core.onrender.com` (consoles store it from the SSO hand-off / their own settings).

## Build the unified app (recommended) — on your machine
Requires Android Studio (or cmdline-tools), JDK 17+, Node 18+. The sandbox cannot build APKs (Android SDK is firewall-blocked) — these steps run on your Windows desktop.

```bash
cd gods-mobile
npm install
npx cap add android      # generates android/ via the Android SDK
npx cap sync
# apply resources:
#   cp android-resources/xml/network_security_config.xml android/app/src/main/res/xml/
#   cp android-resources/values/strings.xml             android/app/src/main/res/values/
#   merge android-resources/AndroidManifest.permissions.xml into android/app/src/main/AndroidManifest.xml
#   (INTERNET + ACCESS_NETWORK_STATE; add android:networkSecurityConfig="@xml/network_security_config")
npx cap open android     # Android Studio -> Build > Generate Signed Bundle/APK > APK > release (create keystore once)
```
`build-apk.sh` automates steps up to an **unsigned** release APK; sign in Android Studio for distribution.

## Build a per-surface app
Scaffold like `gods-mobile`, then drop in one of the `mobile-gateways/capacitor.config.*.json` files as
`capacitor.config.json` (it sets that app's `appId`, `appName`, and `server.url`). Update `strings.xml`
(`app_name`, `package_name`) to match the chosen appId. Build as above.

## OTA update flow
1. Edit the web console (e.g. `udoc-operator/index.html`) and push — Render redeploys the static service.
2. Users get the change next time they open the app. No Play Store / APK round-trip.
Because the shell only hosts `server.url`, app updates are needed only for native changes (permissions, icons, Capacitor version).

## Notes
- All surfaces are HTTPS; `network_security_config.xml` sets `cleartextTrafficPermitted="false"` (system trust only).
- SSO works on mobile exactly as on web: the unified app loads the gateway, you sign in once, and the
  in-app navigation to your console carries the token via URL fragment (whitelisted origins keep it in-webview).
- iOS: the same configs work with `npx cap add ios` (build in Xcode); Android is the documented path here.
