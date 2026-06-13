# v19 Correction + GODS Admin UDOC — delivery & deploy
_Supersedes the "package_v38 as base" assumption in UDOC_CONSOLIDATION_MASTER.md (Sections F/G)._

## What went wrong with v19 (root cause)
v19 was built by making the **`package_v38` monorepo the base** and shipping a `render.yaml` that defines
**new** services (`udoc-api` / `udoc-web` / `udoc-db`). Your live ecosystem is a different monorepo, so v19
did not merge — it tried to stand up a parallel/replacement stack. Concrete incompatibilities:

| | Live v18 (deployed) | v19 / package_v38 |
|---|---|---|
| Repo layout | ~35 top dirs (`platform-core`, `udoc-app`, `platform-internal`, `portals-web`, divisions…) | `apps/api`, `apps/web`, `apps/mainframe` |
| API contract | flat (`/auth/login`, `/access/profile`, `/users`, `/udoc/...`) | `/api/v1/...` |
| Render services | `gods-db`, `gods-platform-core`, `gods-udoc-web`, `gods-platform-internal`, `gods-portals` | `udoc-db`, `udoc-api`, `udoc-web` |
| DB schema | `tenant_id` / `tenant_pk` | `tenant_code` |
| CORS | `allow_credentials=False` | `True` |

Deploying it would have orphaned the `gods-*` services + `gods-db` and broken every frontend + the mobile
app that call the flat contract. **Correctly pulled back.**

## Corrected rule (now permanent)
- **The live v18 ecosystem is THE base and THE deploy target. It is never replaced.**
- `package_v38` is a **donor only** — we borrow specific features (e.g. the intelligence/knowledge layer)
  and port them INTO `platform-core` on the flat contract + `tenant_id` schema, when needed. We never swap
  the base or the `render.yaml` service definitions.
- Everything new is **additive** to the existing repo + Render blueprint.

## Delivered this session — GODS Admin UDOC (internal sovereign operations mainframe)
- File: **`udoc-internal/index.html`** (single-file, brand-exact: navy `#0A1628` / gold `#C9A84C` /
  cyan `#00C2D4`, Barlow + IBM Plex Mono, Shield&Compass mark, CONFIDENTIAL classification bar).
- Wired to the **live `gods-platform-core` flat API** (default base `https://gods-platform-core.onrender.com`,
  overridable on the login screen). Sections, all pulling real data:
  - **Overview** — cross-deployment KPIs (systems, audit events, pending oversight, incidents, personnel)
    from `/registry/models`, `/audit/records`, `/oversight/cases`, `/udoc/incidents`, `/users`,
    `/udoc/regulator/summary`.
  - **AI Systems** — `/registry/models`. **Oversight (HITL)** — `/oversight/cases`.
  - **Audit & Integrity** — `/audit/records` + `/audit/chain/merkle-root` + `/audit/chain/verify`.
  - **Constitution** — `/udoc/constitutional/pillars`. **Incidents** — `/udoc/incidents`.
  - **Access Control** — `/users` (+ `/users/roles`): grant operator, change role, revoke/restore.
- Verified against a locally-booted `platform-core` + seed: login OK; 6 KPI tiles; 2 systems; 1 oversight
  case; 15 audit records + merkle root + chain VERIFIED; 12 constitutional pillars; 10 operators + grant form.
- **Additive Render service** appended to `render.yaml`: `gods-udoc-admin` (static, `rootDir: udoc-internal`).
  The existing `gods-db` + 4 services are unchanged.

## Deploy (from your machine — additive, safe)
1. Drop **`udoc-internal/index.html`** into the repo at `udoc-internal/index.html`.
2. Replace the repo's **`render.yaml`** with the one in outputs (it is your existing file + ONE new service).
3. Commit + push to `main`. In Render, the Blueprint adds **`gods-udoc-admin`** as a new static site;
   nothing else changes. Open it, sign in as your admin, and it talks to the live core.
4. (Optional) Add the `gods-udoc-admin` URL to `platform-core` CORS — not required: CORS is `*` + no
   credentials (Bearer token in header), so the new origin already works.

## Known follow-ups (small, honest)
- `/udoc/regulator/summary` returns 403 for role `admin` → the "Decisions" KPI shows "—". Align that
  endpoint's role-gating to include the GODS admin (or read decisions from a decisions count endpoint).
- Client UDOC (external) + folding package_v38's intelligence layer into `platform-core` remain later stages.
- Mobile OTA: point the mobile WebView/`server.url` at `gods-udoc-admin` only if you want the admin on mobile
  (the existing `gods-udoc-web` remains the client app).
