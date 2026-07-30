# UDOC Client — Android .apk (app id: za.gods.udoc)

**Audience:** Tenant / SaaS clients only.  
**Not** GODS staff admin. Staff mobile path for Capstone = PWA install of Admin (`gods-udoc-admin`).

Capacitor project that packages the **udoc-app** (client Control) web UI.

Package matrix: `udoc-mvp/UDOC_MVP_PACKAGE_MATRIX.md`.

## Requirements (your desktop)
- Android Studio or Android command-line tools
- JDK 17+
- Node.js 18+

## Build
```bash
cd udoc-mobile
./build-apk.sh
npx cap open android    # signed APK via Android Studio
```

## First launch
Connect screen → Core API base (`https://gods-platform-core.onrender.com`).  
Client functions only: register/govern **own** models, dashboard, tenant flows — no kill-switch / global jobs.
