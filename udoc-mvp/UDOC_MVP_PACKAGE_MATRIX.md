# UDOC Capstone MVP · Package Matrix (March 2027 submission)

**Date:** 2026-07-31  
**Goal:** Split UDOC into role-specific packages (not one mega-demo).  
**API:** All packages connect to `gods-platform-core`.  
**Honesty:** Software MVP on free Render/Neon; not commercial SaaS; not hardware appliance.

---

## Package map

| Package | Audience | Channel | Repo / host |
|---------|----------|---------|-------------|
| **UDOC Internal Desktop** | Staff / admins | Electron | `udoc-desktop` → Admin |
| **UDOC Client Desktop** | Tenants | Electron | `udoc-desktop-client` → Client |
| **UDOC Web · Client** | Tenants | Static | `udoc-public` |
| **UDOC Web · Internal** | Staff | Static | `udoc-internal` |
| **UDOC App + Mobile** | Tenants only | PWA / APK | `udoc-app` · `udoc-mobile` |
| **Citizen** | Public | Browser | Client `/citizen.html` |
| **Gateway** | All | Static | `udoc-gateway` |
| **Sentinel / Portals** | Staff + ops | Core | `/Sentinel` · `/portals` |

---

## Implementation progress

| ID | Work | Status |
|----|------|--------|
| M1 | Internal Desktop → Admin | **Done** |
| M2 | Client Desktop package | **Done** |
| M3 | App/Mobile client gate (no hardware plane) | **Done** — CSS + auto-enter Software |
| M4 | Staff mobile = Admin PWA | Documented |
| M5 | Client Web Models/Reports/Policy labels | **Done** |
| M6 | Internal Desktop menu shortcuts | **Done** |
| M7 | Live P6 smoke green | **Operator** |

Details: `UDOC_CLIENT_PACKAGE_NOTES.md` · `UDOC_SAAS_READINESS_GAP.md`

---

## Capstone MVP bar

1. Internal path (Admin Desktop/Web + Sentinel)  
2. Client path (Web + optional Desktop + App)  
3. Citizen public path  
4. Gateway role routing  
5. Smoke: biased **BLOCK** on Client + Sentinel  
