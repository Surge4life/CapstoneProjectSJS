# UDOC — Consolidation & Integration Master (facts vs hard truth)
_Authoritative. Supersedes mockup-based assumptions. Grounded in the actual uploaded code._
_Resume order on any new session: this file → MEMORY.md → SKILLS.md. Keep these THREE in the project
resources (they persist); the sandbox `/tmp` workspace does NOT survive between sessions._

## A. Verified facts (run in sandbox this session)
- **`package_v38` (your detailed build) is real and runs:** API imports OK, **72 routes**, and after a fix
  **ALL 9 tests pass**. Fix applied: the KB ingest default path missed the repo-root `docs/source-material`,
  so the knowledge stores shipped empty; added the repo-root path + regenerated → 204 chunks / 14 sources,
  knowledge store populated (424KB). Foundation is sound and green.
- **Live system = the lean v18** (deployed on Render; working) — a SUBSET of package_v38's API surface plus
  deployment + operational hardening that package_v38 lacks.

## B. What is DONE (by SJS) — `package_v38` monorepo
- **Backend `apps/api`** (FastAPI 0.115, SQLAlchemy 2.0, psycopg3, JWT, bcrypt, redis, pypdf). 17 routers:
  registry, decisions, audit, bias, compliance, oversight, lineage, sovereignty, workforce, intelligence,
  admin, auth, health, **seths, madiba, ts** (division routers).
- **Intelligence layer (deep):** services for ingest, knowledge, memory, semantic, workflows, gap, provenance;
  JSON stores (`knowledge_store`, `sources_manifest`, `memory_packs`, `workflow_state`, `provenance_registry`).
  → This is the engine for BOTH internal (data-sharing + reporting) and client-private (company knowledge).
- **Crypto:** `pqc.py` (hybrid post-quantum placeholder + signed-hash). Risk engine, explainability, event bus.
- **Frontend `apps/web`** — React+TS+Vite but THIN (single App.tsx). This is where the v7 multi-persona UX goes.
- **Mainframe `apps/mainframe`** — rich HTML admin consoles (GODS_Admin_Mainframe_v3_8 110K, GODS_Admin_Stack
  139K/182K, Access_Gateway, GODS_Intelligence_AI, Technical_Whitepaper_System). Needs API wiring.
- **Infra:** docker-compose (Postgres16/Redis7/Redpanda/OpenSearch), k8s starters, Prometheus, CI/CD;
  production pack (`work_fusion`) adds `infra/production`. `udoc-demo` + `legacy-node-mvp` preserved.
- **README "not production-complete" list:** real Kyber/Dilithium, Cassandra audit store, Kafka-under-load,
  GraphQL, SOC2/ISO27001 evidence, real HSM, air-gapped updates. (These are the hardware-ready-later items.)

## C. What is LIVE (v18) — deployed gains to FOLD IN
- `_heal_schema()` idempotent ALTER (heals old live DBs), DB backup/restore endpoints + CLI, bootstrap admin,
  CORS fix (`allow_credentials=False`), `render.yaml`, **role-scoped UDOC UI**, **runtime user/access
  management (`/users`)**, login `active`-revoke, Capacitor APK (OTA). 126 routes (more API surface in
  user-mgmt / backup / policy-versioning / tenant self-service than package_v38).

## D. The TWO distinct offerings (SJS architecture — drives everything)
1. **GODS Admin UDOC — INTERNAL (priority #1).** A *dedicated overarching admin* for G.O.D.S (the holding co.)
   with control over **all UDOC systems deployed across all divisions**. Internal UDOC = intelligence +
   data-sharing + recording → report generation. Surface: `apps/mainframe` (GODS Admin Mainframe) wired to API.
   Roles: a dedicated **GODS UDOC Admin** (super/overarching) distinct from a client's UDOC admin.
2. **Client UDOC — EXTERNAL.** What a client organisation runs: the **dedicated EVA-engine AI-policy-regulation
   UDOC** (register systems, decisions, oversight, audit, compliance for THEIR AI). Plus **client-private
   Intelligence**: a client uploads/stores company data their workers use as an automated operational
   reference (kept in line with company objectives). Surface: `apps/web` (the v7 multi-persona platform).
- G.O.D.S = holdings company. **UDOC = the product/task to complete first.** Ecosystem (seths/madiba/ts)
  comes only after GODS Admin UDOC is done.

## E. GAP (to production-ready, public release)
1. ONE consolidated codebase = `package_v38` hardened + v18 gains folded in.
2. Fix the 2 intelligence tests; make the knowledge/provenance stores load deterministically.
3. **GODS Admin mainframe wired to the API** (internal admin, cross-division control, intelligence/reporting).
4. **Client web platform** built to the v7 multi-persona, sector/role-differentiated UX + client-private intel.
5. Production auth hardening (README says auth is a *scaffold*) → v18 user/access-mgmt + instant-revoke.
6. Durable data (off free Render Postgres before 3 Jul 2026) + production infra + suitable host migration.
7. Multi-surface: one web app wrapped for web + mobile (Capacitor) + desktop (Electron).
8. Hardware-ready-later items tracked (PQC/HSM/Cassandra/Kafka) — surfaced, not blocking v1.

## F. Merge approach
- **Base = `package_v38`** (super build) for architecture + intelligence + divisions + infra;
  take production infra from `work_fusion`.
- **Fold v18 into `apps/api`:** schema-heal, backup/restore + CLI, bootstrap admin, CORS, render.yaml;
  merge auth → add `/users` user/access-mgmt + role-scoping + `active`-revoke + instant-revoke (token-version).
- **Reconcile models** (package_v38 `tenant_code` vs v18 `tenant_id/tenant_pk`) into one schema; heal handles drift.
- Keep package_v38 tests + add v18 governance tests; everything must stay green.

## G. Staged plan (GODS Admin UDOC first; ecosystem last)
- **Stage A — Foundation lock:** ✅ DONE — `package_v38` adopted as canonical base; KB ingest path fixed;
  knowledge regenerated (204 chunks/14 sources); **all 9 tests green**; API imports (72 routes).
  _Next within A:_ boot + smoke the live API server, then proceed to Stage B.
- **Stage B — Fold in v18 gains:** ✅ DONE (v19) — added schema-heal (`app/db/heal.py`), bootstrap-admin
  (`app/db/bootstrap.py`), login `is_active` block, and admin user-management (create + full PATCH update +
  password reset + roles catalog, with self-lockout guards) into `apps/api`; added root `render.yaml`.
  VERIFIED: tests 9/9; heal adds 6 missing columns to an old `users` table; a fresh empty DB self-bootstraps
  and is loginable (admin@gods.local); create→login→revoke(403)→restore→password-reset loop passes;
  self-deactivate/demote blocked (400). 75 routes. _Deferred to a later pass:_ signed backup/restore
  endpoints + token-version instant-revoke (note: `get_current_user` already rejects inactive users, so a
  revoke already bites protected calls immediately; login now also blocks).
- **Stage C — GODS Admin UDOC (internal):** wire `apps/mainframe` to the API; dedicated GODS UDOC Admin role;
  cross-division oversight of all UDOC deployments; internal intelligence + report generation. _Verify:_ live.
- **Stage D — Client UDOC (external web):** build `apps/web` into the v7 multi-persona, sector/role-scoped
  client platform + client-private intelligence (company data upload/reference). _Verify:_ live per mockup.
- **Stage E — Production hardening + host + multi-surface:** durable DB, production infra, security,
  Capacitor + Electron, perf/error states. _Verify:_ clean end-to-end deploy.
- **Stage F — Rest of GODS ecosystem:** seths/madiba/ts division UDOCs. _After Stage C–E sign-off._

## H. Continuation protocol (so sessions resume cleanly)
- Durable across sessions: **project resources (`/mnt/project`)** + files SJS re-uploads. NOT `/tmp`.
- Each session: rebuild base from the uploaded `udoc_platform_detailed_v3_8_super_build` tarball (or the latest
  consolidated zip in outputs). Read this file + MEMORY.md + SKILLS.md first.
- Never mark a stage done without a live/verified check. Update Section G checkboxes as stages pass.
