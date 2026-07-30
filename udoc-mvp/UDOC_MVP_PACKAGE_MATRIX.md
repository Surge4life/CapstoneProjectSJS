# UDOC Capstone MVP · Package Matrix (March 2027 submission)

**Date:** 2026-07-30  
**Goal:** Split UDOC into role-specific packages (not one mega-demo).  
**API:** All packages connect to `gods-platform-core` (G.O.D.S API).  
**Honesty:** Software MVP on free Render/Neon; not commercial SaaS; not hardware appliance.

---

## 1. Package map (who uses what)

| Package | Audience | Channel | Repo / live host | Primary functions |
|---------|----------|---------|------------------|-------------------|
| **UDOC Internal Desktop** | GODS staff · UDOC admins · internal operators | Electron `.exe` | `udoc-desktop` → **Admin** host | Control plane, HITL, kill-switch, lifecycle, evidence, jobs, Sentinel link, Core `/portals` dual-path |
| **UDOC Client Desktop** | Paying / pilot tenants | Electron `.exe` | `udoc-desktop-client` → **Client** host | Registry, Govern/EVA, reports, policy view, models under **tenant** SaaS only |
| **UDOC Web · Client** | External clients (browser) | Static PWA | `udoc-public` · `gods-udoc-client` | Dashboard · Registry · Compliance · Audit · Bias · Sovereignty · Govern |
| **UDOC Web · Sector** | Public / Private sector ops | Static | `udoc-sector` | Sector profile · frameworks · EVA · PUBLIC/PRIVATE terminology |
| **UDOC Web · SaaS Portals** | Client roles admin/controller/cob/auditor/viewer | Static | `udoc-portals` | Role+sector filtered portal controls → Core dual-path |
| **UDOC Web · Internal** | Staff browser | Static | `udoc-internal` · `gods-udoc-admin` | Same capability class as Internal Desktop (browser) |
| **UDOC Web · Operator** | Profile operators | Static | `udoc-operator` | Workspace for sovereign-operator profiles |
| **UDOC Gateway** | All signed-in users | Static | `udoc-gateway` | SSO → correct console by role |
| **UDOC App (PWA)** | Clients on installable web | Vite PWA · `gods-udoc-web` | `udoc-app` | Client Control: register/govern own AIs · dashboard · connect to Core |
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

## 3. Role → entry

| Role | Entry package |
|------|----------------|
| `admin` / `exec` (GODS) | Gateway → Internal Web **or** Internal Desktop |
| `operator` (UDOC staff) | Internal Web / Operator / Core `/portals` |
| `gov` / sector | Sector Web |
| `client` | Client Web · Client Desktop · UDOC App · Mobile |
| `auditor` | Client (read-heavy) or Internal audit views |
| public citizen | Citizen only |

Server remains authoritative (`/access/*`, JWT role). UI gating is not security.

---

## 4. Capstone MVP acceptance (package-level)

For March 2027 submission, **minimum package story**:

1. **One Internal path** — Desktop or Web Admin shows staff controls (demo 6/7 class) + link to Sentinel + Portals.  
2. **One Client path** — Web Client + optional Desktop Client + App/Mobile show tenant governance (demo 1/2/4 class).  
3. **Citizen path** — public challenge/status.  
4. **Gateway** routes by role.  
5. **Smoke** — biased BLOCK on Client + Sentinel.  
6. **Docs** — this matrix + `UDOC_LIVE_ENVIRONMENTS.md` + smoke/P6.

Not required for Capstone MVP: MFA, paid multi-tenant proof, hardware node, GIS product, full StayChain UI.

---

## 5. Outstanding package work (implementation queue)

| ID | Work | Priority |
|----|------|----------|
| M1 | `udoc-desktop` default URL = **Admin** (internal), not Core API root | P0 |
| M2 | `udoc-desktop-client` Electron shell → Client host | P0 |
| M3 | Align `udoc-app` / `udoc-mobile` copy & nav to **client-only** (no staff chrome) | P1 |
| M4 | Document mobile staff path = PWA install of Admin (no second staff APK required for Capstone) | P1 |
| M5 | Client Desktop functions: models list, EVA/Govern, reports/decisions table, policy active view | P1 |
| M6 | Internal Desktop shortcuts: Admin · Sentinel · Portals · Operator | P1 |
| M7 | Freeze Canon; implement from matrix | ongoing |

---

## 6. What not to do

- Do not point one desktop at Core root and call it both client and staff.  
- Do not add new Render services per package.  
- Do not build GIS/GBS packages until UDOC package matrix is stable.  
- Do not claim commercial SaaS readiness (see `UDOC_SAAS_READINESS_GAP.md`).
