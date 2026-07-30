# UDOC Client — Desktop (Electron)

**Audience:** External / pilot tenants.  
**Functions:** Governance console · SaaS Portals · Sector · Citizen public link.  
**API:** All data via `gods-platform-core` (through the web hosts).  
**Not** staff kill-switch / global jobs — those are `udoc-desktop` (Internal).

| Env | Default |
|-----|---------|
| `UDOC_CLIENT_URL` | `https://gods-udoc-client.onrender.com` |
| `UDOC_SAAS_PORTALS_URL` | `https://gods-udoc-portals.onrender.com` |
| `UDOC_SECTOR_URL` | `https://gods-udoc-sector.onrender.com` |
| `UDOC_CITIZEN_URL` | Client `/citizen.html` |

```bash
cd udoc-desktop-client
npm install
npm start
npm run dist
```

Copy `icon.png` from `udoc-desktop/` if missing. Matrix: `udoc-mvp/UDOC_MVP_PACKAGE_MATRIX.md`.
