# UDOC Capstone MVP · Package Matrix (March 2027)

**Updated:** 2026-07-31  
**API:** `gods-platform-core` · Free Render/Neon · not commercial SaaS  
**Story:** `CAPSTONE_PACKAGE_STORY.md`  
**Intent / freeze / phases:** `ENGINEERING_ROADMAP_CAPSTONE.md`  
**Decision record:** `EDR-001-udoc-only-deploy-layer.md`

## Package map

| Package | Audience | Channel | Host / dir |
|---------|----------|---------|------------|
| **Internal Desktop** | Staff | Electron | `udoc-desktop` → Admin |
| **Internal Web** | Staff | Static PWA | `udoc-internal` · gods-udoc-admin |
| **Client Desktop** | Tenants | Electron | `udoc-desktop-client` → Client |
| **Client Web** | Tenants | Static | `udoc-public` · gods-udoc-client |
| **Client App/Mobile** | Tenants | PWA/APK | `udoc-app` · `udoc-mobile` |
| **Citizen** | Public | Browser | Client `/citizen.html` |
| **Gateway** | All | Static | `udoc-gateway` · role → package |
| **Sentinel / Portals** | Staff ops | Core | `/Sentinel` · `/portals` · `/admin` |

## Gateway role map

| Role | Routes to |
|------|-----------|
| admin · exec · auditor | Internal Admin |
| operator · viewer | Operator workspace |
| gov | Sector |
| client | Client SaaS |
| (none) | Citizen public |

## Progress

| ID | Work | Status |
|----|------|--------|
| M1 | Internal Desktop → Admin | **Done** |
| M2 | Client Desktop | **Done** |
| M3 | App client gate (`packageMode` + CSS + plane) | **Done** |
| M4 | Staff mobile = Admin PWA | **Documented** |
| M5 | Client Web labels | **Done** |
| M6 | Internal package identity | **Done** |
| M7 | Live P6 smoke green | **Operator** |
| M8 | Gateway package routing | **Done** |
| M9 | Capstone package story (demos → packages) | **Done** |
| M10 | Engineering roadmap + EDR-001 (intent first) | **Done** |

## Notes

- Client: `UDOC_CLIENT_PACKAGE_NOTES.md`  
- Internal: `UDOC_INTERNAL_PACKAGE_NOTES.md`  
- Package story: `CAPSTONE_PACKAGE_STORY.md`  
- Roadmap (freeze, phases, constraints): `ENGINEERING_ROADMAP_CAPSTONE.md`  
- Gateway: `udoc-gateway/README.md`  
- SaaS gap (honest non-claim): `UDOC_SAAS_READINESS_GAP.md`

## Capstone bar

1. Internal path · 2. Client path · 3. Citizen · 4. Gateway · 5. biased **BLOCK** on Client + Sentinel

**Intent rule:** Well-documented limits and decisions are Capstone assets. Commercial certainty is not required and is not claimed.
