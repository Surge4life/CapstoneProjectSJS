# G.O.D.S Portals — Native Android (.apk) build project

This is a complete Capacitor project that wraps the portals PWA (`portals-web`) into a
real, installable, signed Android `.apk`. The web app inside is identical to the PWA and
already works; this produces the native binary for Play Store / sideload distribution.

## Why it isn't pre-compiled here
A signed `.apk` requires the Android SDK + Android Gradle Plugin + a signing keystore.
Those can't be installed in the build sandbox (no SDK; Google's Maven is firewall-blocked).
Everything *except* the final compile is done for you below — it's three commands on any
machine with Android Studio.

## Build the .apk (on a machine with Android Studio + JDK 17+)
```bash
cd portals-mobile
npm install
npm run build:web        # copies the latest portals build into www/
npx cap add android      # generates the native android/ project (needs SDK)
npx cap sync
npx cap open android      # opens Android Studio
# In Android Studio:  Build → Generate Signed Bundle / APK → APK → create/keystore → release
# Output: android/app/build/outputs/apk/release/app-release.apk
```

## Command-line alternative (no IDE), once android/ exists and SDK is on PATH
```bash
cd android
./gradlew assembleRelease         # unsigned
# or configure signing in android/app/build.gradle then:
./gradlew assembleRelease         # signed release .apk
```

## What the app does
On first launch it shows the same connect screen as the PWA: enter your deployed backend
URL (LAN IP or ngrok/cloudflared tunnel), and the three portals (Student/Employer/Employee)
work live against your G.O.D.S deployment. Network-state aware via @capacitor/network.

## Distribution
- **Sideload:** share the `.apk`; users enable "install unknown apps" and tap it.
- **Play Store:** upload the signed `.aab` (Build → Generate Signed Bundle).
- **Meanwhile:** the PWA in `portals-web` is installable today with zero toolchain.
