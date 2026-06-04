> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# Building the G.O.D.S .apk Applications

Five installable apps. Each has a complete Capacitor project ready to compile to a signed
`.apk`. The web app inside each is **also installable as a PWA today** with zero toolchain.

| App | Build dir | App ID | Who uses it |
|---|---|---|---|
| UDOC Control | udoc-mobile | za.gods.udoc | SaaS clients governing their AIs |
| SETHS | seths-mobile | za.gods.seths | students/employers/employees + documents |
| MADIBA | madiba-mobile | za.gods.madiba | investors: engagement + project updates |
| TS Industries | ts-mobile | za.gods.ts | SPV/gov/private project submission + partners |
| GODS Portals | portals-mobile | za.gods.portals | combined Student/Employer/Employee portals |

## Prerequisites (install on your desktop once)
1. **Android Studio** — https://developer.android.com/studio (bundles the Android SDK + emulator)
2. **JDK 17+** — Android Studio includes one, or install Temurin 17
3. **Node.js 18+** — https://nodejs.org

## Build any app (one command)
```bash
cd udoc-mobile          # or seths-/madiba-/ts-/portals-mobile
./build-apk.sh
```
This builds the web app, generates the native `android/` project, applies the G.O.D.S Android
resources, and assembles an unsigned release APK at
`android/app/build/outputs/apk/release/app-release-unsigned.apk`.

## Produce a SIGNED apk (for sideload / Play Store)
```bash
cd udoc-mobile
npx cap open android
```
In Android Studio: **Build → Generate Signed Bundle / APK → APK →** create a keystore (keep it
safe — you reuse it for updates) **→ release**. That `.apk` installs on any Android device.

## Quick test on an emulator (no signing needed)
```bash
cd udoc-mobile && npx cap open android      # then press Run ▶ in Android Studio
```

## Why these aren't pre-built in the package
A signed `.apk` requires the Android SDK + Android Gradle Plugin + a keystore. The environment
that generated this package has no SDK and is firewall-blocked from fetching it, so the SDK
compile is the single step that runs on your machine. Everything else — web apps, Capacitor
config, native resources, network-security for the connect-screen, build scripts — is done and
validated.

## First launch (all apps)
Each app opens a **connect screen**: enter your deployed backend URL — your Render URL
(`https://gods-platform-core.onrender.com`), a LAN IP (`http://192.168.x.x:8000`), or an
ngrok/cloudflared tunnel — and the app runs live against your G.O.D.S deployment.
