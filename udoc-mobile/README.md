# UDOC Client — Android .apk (app id: za.gods.udoc)

**Package:** CLIENT (tenant SaaS only)  
**Audience:** External / pilot tenants.  
**Not** GODS staff admin. Staff mobile for Capstone = PWA install of Admin (`gods-udoc-admin`).

Capacitor wraps the **udoc-app** build (`UDOC_PACKAGE = "client"` in `packageMode.ts`).  
Hardware plane and kill-switch UI are gated out (CSS + CAPS `hw: []`).

| Doc | Path |
|-----|------|
| Package matrix | `udoc-mvp/UDOC_MVP_PACKAGE_MATRIX.md` |
| Package story | `udoc-mvp/CAPSTONE_PACKAGE_STORY.md` |
| Client notes | `udoc-mvp/UDOC_CLIENT_PACKAGE_NOTES.md` |

## Requirements (your desktop)
- Android Studio or Android command-line tools
- JDK 17+
- Node.js 18+

## Build (keep www in sync with udoc-app)
```bash
cd udoc-app && npm run build
# copy dist → udoc-mobile/www (or your existing sync script)
cd ../udoc-mobile
./build-apk.sh
npx cap open android    # signed APK via Android Studio
```

## First launch
Connect → Core API (`https://gods-platform-core.onrender.com`).  
Client functions only: own models · EVA · policy · tenancy — **no** staff kill-switch / global jobs / Access Control admin.
