# TS Industries — Native Android (.apk) build
Capacitor wrapper for the ts-app PWA. App ID: `za.gods.ts`.

## Build the signed .apk (machine with Android Studio + JDK 17+)
```bash
cd ts-mobile
npm install
npm run build:web        # bundle latest ts-app build into www/
npx cap add android      # generate native android/ project (needs Android SDK)
npx cap sync
npx cap open android     # Android Studio → Build → Generate Signed APK
```
On first launch the app asks for your G.O.D.S backend URL (LAN IP or tunnel) and connects live.
The PWA (`ts-app`) is installable today with no toolchain.
