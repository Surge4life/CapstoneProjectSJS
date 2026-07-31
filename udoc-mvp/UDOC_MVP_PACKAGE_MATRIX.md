# UDOC Capstone MVP · Package Matrix (March 2027)

**Updated:** 2026-07-31  
**API:** `gods-platform-core` · Free Render/Neon · not commercial SaaS  
**Cover:** `CAPSTONE_COVER_NOTE.md`  
**Glossary:** `GLOSSARY.md`  
**EDRs:** 001–004  
**Assessor:** `ASSESSOR_READING_ORDER.md` · `CAPSTONE_EVIDENCE_PACK.md` · `ARCHITECTURE_MAP.md`

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
| M1–M6, M8–M12 | Package channels + intent docs | **Done** |
| M7 | Live P6 smoke green | **Operator** |
| M13 | Glossary · cover note · EDR-004 | **Done** |

## Capstone bar

1. Internal path · 2. Client path · 3. Citizen · 4. Gateway · 5. biased **BLOCK** on Client + Sentinel

**Intent rule:** Well-documented limits and decisions are Capstone assets. Commercial certainty is not required and is not claimed.
