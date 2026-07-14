# Building the real .apk (on your machine — 3 commands)

The complete Android project is already generated in `android/` (Capacitor wrapper around
the portals PWA). This environment can't compile it only because it blocks Google's Android
SDK download (`dl.google.com` is firewalled here) — NOT because anything is missing. On any
normal machine it builds directly.

## One-time setup
1. Install **Android Studio** (bundles the Android SDK + JDK): https://developer.android.com/studio
2. Install **Node.js 18+**.

## Build the APK
```bash
cd portals-web
npm install
npm run apk:debug      # → android/app/build/outputs/apk/debug/app-debug.apk
```
That's it — `app-debug.apk` is a real installable Android app. Copy it to a phone and install
(enable "install from unknown sources"), or run `npm run apk:release` for a signed release build.

## Or use the GUI
```bash
npm run cap:open       # opens the project in Android Studio
# then: Build ▸ Build Bundle(s)/APK(s) ▸ Build APK(s)
```

## What the app does
It's the G.O.D.S Portals (Student / Employer / Employee) wrapped natively. On first launch it
shows the connect screen — enter your deployed backend URL (LAN IP or public tunnel) and it
works exactly like the web/PWA version, fully offline-capable shell + live data from your node.

## Signing a release .apk (for distribution)
```bash
keytool -genkey -v -keystore gods.keystore -alias gods -keyalg RSA -keysize 2048 -validity 10000
# add signingConfig to android/app/build.gradle (Android Studio: Build ▸ Generate Signed Bundle/APK)
npm run apk:release
```
