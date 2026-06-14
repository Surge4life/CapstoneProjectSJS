# GODS Admin UDOC — Operational Control Plane (Stage 1 of the detailed operational build)
_Additive to the live v18 ecosystem · wired to the `gods-platform-core` flat contract · package_v38 = donor._

## Delivered + verified this session
The GODS Admin UDOC (`udoc-internal/index.html`) is now a full operational control plane — **15 sections,
all wired to live endpoints, 0 JS errors**, verified against a booted `platform-core` + seed:

| Section | Live endpoint(s) | Verified |
|---|---|---|
| Overview | registry/models, audit/records, oversight/cases, udoc/incidents, users, udoc/regulator/summary | 6 KPIs |
| AI Systems | /registry/models | 2 rows |
| Decisions · EVA | /decisions, /decisions/certificates | 14 rows |
| Policy & COB | /policy/packs, /policy/versions, /policy/active | renders (0 seeded) |
| Oversight (HITL) | /oversight/cases | 1 row |
| Audit & Integrity | /audit/records, /audit/chain/merkle-root, /audit/chain/verify | 15 + VERIFIED |
| Constitution | /udoc/constitutional/pillars | 12 pillars |
| Compliance | /compliance/frameworks (+ /compliance/sweep action) | renders |
| Sovereignty | /sovereignty/posture | 3 rows |
| Incidents | /udoc/incidents | renders |
| Intelligence | /intel/state, /intel/docs, /intel/ask (ask box) | 2 KPIs + ask |
| Clients / Tenants | /tenants, /tenants/tiers | 2 rows |
| Division Ops | /analytics/{SETHS,MADIBA,TS,UDOC}/kpis | 4 panels |
| Access Control | /users, /users/roles (grant/role/revoke) | 10 operators |
| Roles & Profiles | /users/roles, /access/profile | 12 roles |

## Deploy (additive — unchanged from before)
- Replace `udoc-internal/index.html` in the repo with the file in outputs.
- `render.yaml` already declares `gods-udoc-admin` (added last session) — no further change. Push to `main`.
- CORS already permits it (`*` + no credentials; Bearer token in header).

## Mobile app — OTA gateway to the admin
The admin is the static site `gods-udoc-admin`. To put it on mobile with OTA (UI updates on next launch,
no rebuild), point a Capacitor shell's `server.url` at it — same pattern as `udoc-mobile` → `gods-udoc-web`:
```json
// capacitor.config.json
{ "appId": "za.gods.udoc.admin", "appName": "GODS UDOC Admin", "webDir": "www",
  "server": { "url": "https://gods-udoc-admin.onrender.com", "cleartext": false } }
```
Build once (`npx cap sync android && ./gradlew assembleDebug`); thereafter every `gods-udoc-admin` redeploy
reaches the device on next open. (Your existing `udoc-mobile` → `gods-udoc-web` remains the client app.)

## Next stages (same additive method, on the live contract)
1. **Profile/user-roles depth** — surface the 24 Sovereign Operator profiles + per-role access matrix as a
   managed model in `platform-core` (extends `/users/roles` + `/access/profile`), editable from the admin.
2. **Port package_v38's intelligence depth** (semantic/knowledge/provenance) INTO `platform-core`'s
   `/intel` so the admin's Intelligence + reporting is the full engine (internal reporting; client-private KB).
3. **Client UDOC (external)** — build `udoc-public`/`udoc-app` into the v7 multi-persona client platform +
   client-private intelligence, on the same flat contract.
4. **Decision/COB actions in-admin** — approve/veto policy versions, resolve oversight cases, run bias scans
   directly from the control plane (role-gated).
