# UDOC Internal Package · Staff Admin

**Audience:** GODS staff · UDOC administrators · internal operators  
**Not:** Tenant SaaS sales product (that is Client package)  
**API:** `gods-platform-core`  
**Matrix:** `UDOC_MVP_PACKAGE_MATRIX.md`

## Channels

| Channel | Source / host |
|---------|----------------|
| Web Internal | `udoc-internal` → **gods-udoc-admin** |
| Desktop Internal | `udoc-desktop` → Admin host + menu to Sentinel / Portals / Core `/admin` |
| Sentinel | Core `/Sentinel` |
| 24 Portals dual-path | Core `/portals` |
| Constitutional Admin | Core `/admin` |
| Operator | `udoc-operator` |
| Staff mobile (Capstone) | PWA install of Admin (no separate staff APK) |

## Staff functions (demo 6–7 class)

- Command Centre · AI Registry · **Kill-switch** · EVA Command · Lifecycle · Evidence/Replay  
- Policy Engine · HITL Queue · Audit · Constitution · Compliance · Sovereignty  
- Intelligence · Clients/Tenants · Division Ops · Sectors · User Management  
- Infra: API Health · Scheduled Jobs · Portals · Citizen (view public surface)

## Hard rules

- Internal package **may** expose kill-switch, global jobs, cross-tenant views.  
- Client package **must not**.  
- Backend JWT role remains authoritative.

## Live hosts

- Admin: `https://gods-udoc-admin.onrender.com`  
- Core: `https://gods-platform-core.onrender.com`  
- Client (separate): `https://gods-udoc-client.onrender.com`

## Density

`admin-v7-enhance.js` injected via `sw.js` (network-first) — scenario chips, Full EVA batch, HITL portal link, infra nav.
