# v20 — Consolidated (v18 live ecosystem + GODS Admin UDOC operational platform)
_One mergeable unit for your waiting branch. Additive only — your live backend + frontends are unchanged._

## What v17/v18/v19 actually were (the diff you asked for)
- **v17 → v18:** v18 added the **user/access-management** router (`platform-core/app/routers/users_admin.py`)
  + the Access Control UI (`udoc-app` App.tsx 44KB→47KB). Additive feature on the LIVE ecosystem.
- **v19 (package_v38):** the fixes I implemented there — `_heal_schema`, `bootstrap_admin`, login `is_active`,
  user-mgmt — **v18 already had all of them** (`platform-core/app/main.py` runs heal + bootstrap;
  `auth.py` line 32 `if not u.active`; `users_admin` has list/roles/create/patch). So v19 added **no new
  fixes** to the live system; it duplicated them in an **incompatible monorepo** (`apps/api`, `/api/v1`,
  `tenant_code`, `udoc-*` services). v19's only genuinely new value = package_v38's **intelligence depth,
  mainframe, division routers** → donor material for stage **B**, NOT a wholesale merge.

## What v20 IS
- The **entire live v18 ecosystem, unchanged** (platform-core flat API, udoc-app, platform-internal,
  portals-web, divisions, governance-engines, infra, IP…).
- **+ `udoc-internal/index.html`** — the GODS Admin UDOC operational control plane (15 sections, brand-exact,
  wired to the live flat contract: Overview, AI Systems, Decisions·EVA, Policy·COB, Oversight, Audit,
  Constitution, Compliance, Sovereignty, Incidents, Intelligence, Clients/Tenants, Division Ops, Access
  Control, Roles & Profiles).
- **+ `render.yaml`** with one added static service `gods-udoc-admin` (your `gods-db` + 4 services unchanged).
- **+ continuity docs** at root (this file, UDOC_CONSOLIDATION_MASTER, V19_CORRECTION_AND_GODS_ADMIN,
  GODS_ADMIN_UDOC_OPERATIONAL, GODS_UDOC_MEMORY).

## Verified as a unit
`platform-core` boots; the admin console authenticates against it and renders with real data, **0 JS errors**
(overview 6 KPIs, decisions 14, audit 15 + merkle VERIFIED, access 10 operators, roles 12).

## Merge / deploy (safe, additive)
1. Merge your branch / drop these into the repo: it adds exactly **`udoc-internal/index.html`** and updates
   **`render.yaml`** (one new service). Nothing else in the live stack changes byte-for-byte.
2. Push to `main`. Render's Blueprint adds **`gods-udoc-admin`** as a new static site; existing services + DB
   untouched. CORS already allows it (`*`, no credentials — Bearer token in header).
3. Optional mobile OTA: point a Capacitor shell `server.url` at `gods-udoc-admin` (see GODS_ADMIN_UDOC_OPERATIONAL.md).

## Next, in your order: C → B → A → D
- **C — Client UDOC (external):** build the external client platform (v7 multi-persona) + client-private
  intelligence, on the flat contract.
- **B — Intelligence depth:** port package_v38's semantic/knowledge/provenance services INTO `platform-core`'s
  `/intel` (internal reporting + client KB).
- **A — Profile/user-roles depth:** the 24 Sovereign-Operator profiles + per-role access matrix, managed from admin.
- **D — COB actions in-admin:** approve/veto policy versions, resolve oversight, run bias scans from the console (role-gated).
