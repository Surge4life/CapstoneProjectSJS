# MADIBA — Android .apk build (app id: za.gods.madiba)

Capacitor project that compiles the **madiba-app** web app into a native Android `.apk`.

## Why it isn't pre-compiled in the package
A signed `.apk` needs the Android SDK + Android Gradle Plugin + a keystore. The build sandbox
that produced this package has no SDK and is firewall-blocked from downloading it. Everything
else is done; the SDK build is the one step that must run on your machine.

## Requirements (on your desktop)
- Android Studio (gives you the SDK + an emulator) **or** Android command-line tools
- JDK 17+
- Node.js 18+

## Build (one script)
```bash
cd madiba-mobile
./build-apk.sh          # builds web app → generates android/ → applies resources → assembles APK
```
Then to produce a **signed** apk for sideload/Play Store:
```bash
npx cap open android    # opens Android Studio → Build > Generate Signed Bundle / APK > APK
```
Output (unsigned): `android/app/build/outputs/apk/release/app-release-unsigned.apk`

## What's already prepared for you
- `www/` — the built web app (works as an installable PWA right now, no toolchain)
- `capacitor.config.json` — app id za.gods.madiba, cleartext enabled for the connect-screen
- `android-resources/` — network-security config (lets the app reach your LAN/tunnel backend),
  strings.xml, and the manifest permissions to merge
- `build-apk.sh` — the exact end-to-end build

## First launch
The app shows a connect screen — enter your deployed backend URL (e.g. your Render URL
`https://gods-platform-core.onrender.com`, or a LAN IP / ngrok tunnel) and it runs live.
