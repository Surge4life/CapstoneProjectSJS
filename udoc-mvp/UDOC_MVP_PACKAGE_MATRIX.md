# UDOC Capstone MVP · Package Matrix (March 2027 submission)

**Date:** 2026-07-31 (updated)  
**Goal:** Split UDOC into role-specific packages (not one mega-demo).  
**API:** All packages connect to `gods-platform-core` (G.O.D.S API).  
**Honesty:** Software MVP on free Render/Neon; not commercial SaaS; not hardware appliance.

---

## 1. Package map (who uses what)

| Package | Audience | Channel | Repo / live host | Primary functions |
|---------|----------|---------|------------------|-------------------|
| **UDOC Internal Desktop** | GODS staff · UDOC admins · internal operators | Electron `.exe` | `udoc-desktop` → **Admin** host | Control plane, HITL, kill-switch, lifecycle, evidence, jobs, Sentinel link, Core `/portals` dual-path |
| **UDOC Client Desktop** | Paying / pilot tenants | Electron `.exe` | `udoc-desktop-client` → **Client** host | Registry, Govern/EVA, reports, policy view, models under **tenant** SaaS only |
| **UDOC Web · Client** | External clients (browser) | Static PWA | `udoc-public` · `gods-udoc-client` | Models · Reports · Policy/Compliance · EVA · Audit · Bias · Sovereignty |
| **UDOC Web · Sector** | Public / Private sector ops | Static | `udoc-sector` | Sector profile · frameworks · EVA · PUBLIC/PRIVATE terminology |
| **UDOC Web · SaaS Portals** | Client roles admin/controller/cob/auditor/viewer | Static | `udoc-portals` | Role+sector filtered portal controls → Core dual-path |
| **UDOC Web · Internal** | Staff browser | Static | `udoc-internal` · `gods-udoc-admin` | Same capability class as Internal Desktop (browser) |
| **UDOC Web · Operator** | Profile operators | Static | `udoc-operator` | Workspace for sovereign-operator profiles |
| **UDOC Gateway** | All signed-in users | Static | `udoc-gateway` | SSO → correct console by role |
| **UDOC App (PWA)** | Clients on installable web | Vite PWA · `gods-udoc-web` | `udoc-app` | Client Control: models · EVA · policy · tenancy · connect to Core |
| **UDOC Mobile** | Clients on Android | Capacitor · `udoc-mobile` | wraps `udoc-app` / client | Same **client** surface as UDOC App; not staff admin |
| **Citizen (public)** | Affected persons | Browser · no login | Client `/citizen.html` | Challenge · case status · rights · help |
| **Sentinel / Core shells** | Staff + advanced ops | Core static routes | `/Sentinel` · `/portals` · `/admin` | EVA runtime · 24 dual-path · constitutional admin |

**Hard rule:** Client packages never expose kill-switch, global jobs, or cross-tenant admin. Internal packages never pretend to be the sales SaaS product UI.

---

## 2. Seven demos → package assignment

| # | Demo slug | Goes into |
|---|-----------|-----------|
| 1 | `udoc-mvp-1` International Standards | **Client Web** · Client Desktop · UDOC App/Mobile |
| 2 | `udoc-mvp-2` Multi-Framework Compliance | **Client Web** · Sector Web |
| 3 | `udoc-v7-platform` Full platform | **Split:** Client tabs + Internal Admin + Citizen + Portals — not one app |
| 4 | `udoc-v7-eva` EVA engine | **Sentinel** + Client Govern + Internal EVA Command |
| 5 | `udoc-v5-sa` SA lineage / pillars | **Sentinel** Pillars + Client Sovereignty |
| 6 | `udoc-platform-ui` Operational control v9.3 | **Internal Desktop + Internal Web** |
| 7 | `udoc-sovereign-console` Sovereign console v9.3 | **Internal Desktop + Internal Web** · partial StayChain on Core |

---

## 3. Implementation progress (2026-07-31)

| ID | Work | Status |
|----|------|--------|
| M1 | Internal Desktop → Admin host + staff menu | **Done** |
| M2 | Client Desktop package `udoc-desktop-client` | **Done** |
| M3 | App/Mobile client branding + packageMode helper | **In progress** (branding landed; rebuild App CAPS wiring on next App.tsx edit) |
| M4 | Staff mobile = Admin PWA | Documented |
| M5 | Client Web nav: Models · Reports · Policy labels | **Done** (index.html) |
| M6 | Internal Desktop shortcuts | **Done** |
| M7 | Canon freeze / implement from matrix | Ongoing |

See also: `UDOC_CLIENT_PACKAGE_NOTES.md`.

---

## 4. Capstone MVP acceptance (package-level)

1. **One Internal path** — Desktop or Web Admin (demo 6/7 class) + Sentinel + Portals.  
2. **One Client path** — Web Client + optional Desktop Client + App/Mobile.  
3. **Citizen path** — public challenge/status.  
4. **Gateway** routes by role.  
5. **Smoke** — biased BLOCK on Client + Sentinel.  
6. **Docs** — this matrix + live environments + smoke/P6.

Not required for Capstone MVP: MFA, paid multi-tenant proof, hardware node, GIS product, full StayChain UI.
