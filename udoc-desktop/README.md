# UDOC Internal — Desktop (Electron)

**Audience:** GODS staff · UDOC administrators · internal operators.  
**Not** the client SaaS product. Client desktop lives in `udoc-desktop-client/`.

Loads the **Admin** host by default and menu-jumps to Sentinel, 24 Portals, Core `/admin`.

| Env | Default |
|-----|---------|
| `UDOC_ADMIN_URL` | `https://gods-udoc-admin.onrender.com` |
| `UDOC_SENTINEL_URL` | `https://gods-platform-core.onrender.com/Sentinel` |
| `UDOC_PORTALS_URL` | `https://gods-platform-core.onrender.com/portals` |
| `UDOC_CORE_ADMIN_URL` | `https://gods-platform-core.onrender.com/admin` |

## Build / run (Windows · Node 18+)

```bash
cd udoc-desktop
npm install
npm start          # test window
npm run dist      # installer + portable → release/
```

Package matrix: `udoc-mvp/UDOC_MVP_PACKAGE_MATRIX.md`.
