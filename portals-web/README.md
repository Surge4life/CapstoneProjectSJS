# G.O.D.S Ecosystem Portals (installable PWA)
Student · Employer · Employee portals in one installable app, connecting LIVE to your
deployed G.O.D.S backend — including from your public web page.

## Run / build
```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # dist/ — includes service worker (sw.js) + manifest → installable
```

## How the live connection works (the part you asked for)
The portal's backend URL is **set at runtime on the connect screen**, so the SAME built app
works whether it's served locally or from capstoneprojectsjs.netlify.app:

1. **Deploy the backend** on your machine: `cd platform-core && python seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. **Make it reachable from the device**, choose one:
   - **Same Wi-Fi / LAN:** use `http://<your-machine-ip>:8000` (find IP with `ip addr` / `ipconfig`).
   - **Public tunnel (works anywhere):** `ngrok http 8000` or `cloudflared tunnel --url http://localhost:8000`,
     then use the `https://…` URL it prints. (Tunnel = your Netlify page can reach your laptop.)
3. **Open the portal** (locally or on Netlify), paste that URL on the connect screen, press Connect.
   Green ✓ = live. Pick Student / Employer / Employee and use it for real.

CORS on the backend already allows `https://capstoneprojectsjs.netlify.app`.

## Connecting it to your Netlify capstone site
Two options:
- **Embed:** add a link/iframe on capstoneprojectsjs.netlify.app pointing to the deployed portal, or
- **Host the portal there:** drop this `dist/` into the Netlify site (e.g. `/portals/`) and link it
  from your homepage. Either way the connect screen wires it to your live backend.

## Installable to phone/desktop (PWA — real today, no store needed)
Open the portal in Chrome/Edge/Safari → browser shows **Install** (or Share → Add to Home Screen).
It installs as a standalone app with the G.O.D.S icon, launches full-screen, and connects to your
backend over the network. This is the genuine, working "download & install" path.

## True compiled .apk (optional native wrapper)
A signed `.apk` needs a native build toolchain. The honest path:
```bash
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init "GODS Portals" za.gods.portals --web-dir=dist
npx cap add android
npx cap copy
npx cap open android        # opens Android Studio → Build > Generate Signed APK
```
This produces a real installable `.apk`. It requires Android Studio + JDK on your machine
(can't be built in this environment), but the web app it wraps is exactly what's here and
already works as an installable PWA in the meantime.
