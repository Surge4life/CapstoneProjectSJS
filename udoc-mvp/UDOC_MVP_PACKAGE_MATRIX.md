# UDOC Capstone MVP · Package Matrix (March 2027)

**Updated:** 2026-07-31  
**API:** `gods-platform-core` · Free Render/Neon · not commercial SaaS

## Package map

| Package | Audience | Channel | Host / dir |
|---------|----------|---------|------------|
| **Internal Desktop** | Staff | Electron | `udoc-desktop` → Admin |
| **Internal Web** | Staff | Static PWA | `udoc-internal` · gods-udoc-admin |
| **Client Desktop** | Tenants | Electron | `udoc-desktop-client` → Client |
| **Client Web** | Tenants | Static | `udoc-public` · gods-udoc-client |
| **Client App/Mobile** | Tenants | PWA/APK | `udoc-app` · `udoc-mobile` |
| **Citizen** | Public | Browser | Client `/citizen.html` |
| **Gateway** | All | Static | `udoc-gateway` |
| **Sentinel / Portals** | Staff ops | Core | `/Sentinel` · `/portals` · `/admin` |

## Progress

| ID | Work | Status |
|----|------|--------|
| M1 | Internal Desktop → Admin | **Done** |
| M2 | Client Desktop | **Done** |
| M3 | App client gate (no hardware plane) | **Done** |
| M4 | Staff mobile = Admin PWA | Documented |
| M5 | Client Web Models/Reports/Policy | **Done** |
| M6 | Internal package identity + infra nav | **Done** (banner, Core/admin, SW v5) |
| M7 | Live P6 smoke green | **Operator** |

## Notes

- Client: `UDOC_CLIENT_PACKAGE_NOTES.md`  
- Internal: `UDOC_INTERNAL_PACKAGE_NOTES.md`  
- SaaS gap: `UDOC_SAAS_READINESS_GAP.md`

## Capstone bar

1. Internal path · 2. Client path · 3. Citizen · 4. Gateway · 5. biased **BLOCK** on Client + Sentinel
