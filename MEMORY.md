# MEMORY.md — UDOC live-build continuation anchor
_Read this + SKILLS.md on resume. Workstream: make UDOC a fully live, investment-grade system; divisions last._

## Entity / honesty (non-negotiable)
G.O.D.S Holdings (Pty) Ltd is **proposed / not registered**. No company, trust, trademark, or domain registered; IP vests in **Sashin J. Singh** as author. Demo email domain `@gods.local` (admin@gods.local/admin123; staff staff123). Brand: navy `#060E1C`, gold `#C9A84C`, UDOC purple `#7C5CBF`, hardware cyan `#00C2D4`.

## Regulatory ground truth (June 2026 — verified by web search; keep accurate in UI)
- **EU AI Act (Reg 2024/1689):** IN FORCE, phased. Prohibited practices (2 Feb 2025) + GPAI (2 Aug 2025) live; high-risk Annex III + transparency from **2 Aug 2026**; embedded-product high-risk to 2 Aug 2027. Digital Omnibus postponement provisionally agreed (May 2026) but **not yet law**. Fines up to €35M / 7%.
- **South Africa:** **No enacted AI-specific law.** Draft National AI Policy (Notice 3880 of 2026, **Gazette GG 54477**, 10 Apr 2026) **WITHDRAWN 26 Apr 2026** (≈10% fabricated citations). AI governed via **POPIA (Act 4 of 2013, s71)**, **Constitution (1996, ss 9/16/33)**, IP/procurement/sectoral law, King IV/V. ⚠ Older founder materials cite GG54477 as active — represent as **withdrawn**.

## System state (all build-verified this session)
- **Backend `platform-core`** (FastAPI + SQLite default). Runs only within ONE bash invocation here. Run: `cd platform-core && pip install -r requirements.txt && python3 seed.py && python3 -m uvicorn app.main:app --port 8077`. Login `POST /auth/login` form{username,password}→{access_token}; Bearer. `seed.py` creates admin + model-001 + genuine activity (14 EVA decisions, 15-record intact Merkle chain, 1 oversight case). Serves the live HTML cockpit at **`GET /admin`**.
- **HTML admin cockpit** `GODS_Admin_Live.html` (= `platform-core/static/admin.html`): demo + live bridge (connect/login + API client + poller; `neutraliseDemo()` kills mock loops). Command Centre, AI Registry, COB, Audit wired.
- **UDOC client `udoc-app`** (React+Vite+TS, PWA; runtime base in `src/api.ts`, default `https://gods-platform-core.onrender.com`). **= the mobile web build.** Login → **split**: **Software** (Dashboard · AI Registry+kill-switch · **EVA Engine** 6-D · **Policy-to-Code** · Audit · Compliance) | **Hardware** (HQ-OS · Sovereign Edge · Sovereignty · Kill-Switch).
- **UDOC mobile `udoc-mobile`** — Capacitor v6 (appId `za.gods.udoc`, webDir `www`). Built from `udoc-app/dist` → `udoc-mobile/www/`. APK via `udoc-mobile/build-apk.sh`.
- **Internal `platform-internal`** (React+Vite+TS, react-router; `/api` proxy). RBAC launcher/shell + UDOCGov + division ops + live Holdings Overview.

## Increment 4 (this session) — Policy-to-Code engine BUILT & OPERATIONAL
- Backend: models +PolicyPack/+PolicyRule; `app/services/policy_engine.py` (extract_text PDF/DOCX/TXT + extract_rules transparent heuristics + apply enforcement); `app/routers/policy.py` (`/policy/upload`,`/packs`,`/packs/{id}`,`PATCH /rules/{id}`,`/packs/{id}/activate|archive`,`/active`,`/test`); wired into `decisions.py` (after evaluate → pe.apply → BLOCK/REVIEW; response adds base_decision/policy_enforced/policy_findings; audited). Verified: sample AI Act DOCX → 6 rules → activate → social-scoring model BLOCKED (PR-001), benign chatbot APPROVED.
- Frontend (udoc-app→web+mobile): api +uploadPolicy/+patch; **Policy-to-Code tab** (upload→rules table→activate→Active/Enforced cards); **Compliance tab** = accurate regulatory landscape + active policy. Verified on mobile build.

## Increment 5 (this session) — Render OTA scaffold + sector selection
- udoc-app: **Public/Private sector** picker on the selection screen (localStorage `udoc_sector`; defaults policy-upload sector; topbar chip). In-app **update banner** (polls `/version`) + PWA autoUpdate; `vite.config.ts` define `__BUILD_ID__`.
- Render artifacts: `render.yaml`, `/version`, `capacitor.config.render.json`, `use-render.sh`, `UDOC_RENDER_OTA.md`. Build-verified (sector toggle + /version smoke-tested on mobile build). 7-UI sector modeling still pending the founder's list of the 7 demos.

## PENDING (priority order)
1. **Render + GitHub OTA — SCAFFOLDED (only needs the real Render URL):** `render.yaml` (blueprint: gods-platform-core API + gods-udoc-web static PWA, autoDeploy main), backend `GET /version` (Render git env), udoc-app in-app "new version deployed" banner (polls /version) + PWA autoUpdate, `udoc-mobile/capacitor.config.render.json` + `use-render.sh` (sets server.url→live site), `UDOC_RENDER_OTA.md`. TODO once URL known: bake API URL into `udoc-app` getBase() default + internal `VITE_API_BASE`.
2. **Private/Public sector + 7 UDOC HTML UIs:** site blocks bots — ASK founder for the 7 demos; model the sector/UI split around them (backend already carries `sector`).
3. Mirror Policy-to-Code into the **HTML admin cockpit** (Policy-as-Code stub) + internal app.
4. Compliance depth: map UDOC controls → EU AI Act articles / POPIA sections; per-decision evidence export.
5. **Divisions LAST**, then hardening + deploy + UAT (`GODS_Live_Rollout_and_Test_Schedule.md`).

## OPEN QUESTIONS for the founder
- The **7 UDOC HTML demos**: names + what each shows (to model Private/Public sector).
- The **Render deployment URL** for platform-core (to wire mobile + OTA).

---
## SESSION ADD — White paper, 7 demos, admin tabs, GAP analysis, G.O.D.S Intelligence scaffold

### Uploads read (in /mnt/user-data/uploads)
- `UDOC_EVA_Whitepaper_v1.docx` (EVA = "Evaluating Valiant Algorithms"; the canonical EVA spec).
- `index.html` (the Netlify site, launches 25 Jun 2026) — the **7 UDOC demos** + AGI/Singularity paper + Intelligence framing.
- `GODS_Admin_Stack_Enhanced_v3_6_attached_package.html` — the **authoritative admin tab map** for the React console.
- (Also huge zips UDOC.zip 499M / SYSTEM_BUILD 205M / BRANDING 182M / SJSCAPSTONE 24M — the portfolio; NOT unzipped.)

### The 7 UDOC demos (a version lineage; target = v9.3)
mvp-1 International Standards Dashboard · mvp-2 Multi-Framework Compliance Engine · v5-sa SA-Aligned Architecture Lineage · v7-platform Full Platform (World Deterministic Governance) · v7-eva EVA Engine (Multi-Dimensional Evaluation) · **udoc-platform-ui Operational Control Platform v9.3** · **udoc-sovereign-console Sovereign AI Governance Platform v9.3**. v7/v9.3 contain sector consoles → **Public sector** = Welfare/SARS/Justice/Health; **Private sector** = Corporate.

### Authoritative admin tab map (mirror in React console + cockpit)
overview · users · config · logs · cob · **UDOC**: u-registry, u-policy, u-compliance, u-bias, u-constitutional, u-control, u-evidence, u-exchange, u-hardware, u-incident, u-lifecycle, u-api, u-regulator, u-replay, u-schema · **SETHS**: s-participants, s-employers, s-outcomes · **TS**: ts-projects · madiba.

### EVA canonical (white paper) — alignment gaps vs current build
White paper: 6 dims **Validity, Reliability, Risk, Compliance, Stability, Impact** (0–10), Composite EVA Score (Risk+Impact inverted), outcomes **APPROVE/REVIEW/ESCALATE/BLOCK**, **EVA Certificate** on APPROVE (signed, WORM, publicly verifiable), <50ms sync for HIGH (async for MED/LOW), CRYSTALS-Dilithium signing + 10-yr retention, Policy-as-Code (OPA/Rego-style, versioned, COB-approved, signed, hot-reload <5ms). Current build uses SVS + APPROVE/REVIEW/**RESTRICT**/BLOCK + HMAC seal + Merkle; policy engine has upload/activate/edit. ⚠ White paper cites GG54477 as active (April 2026, pre-withdrawal) — UPDATE to reflect **withdrawn 26 Apr 2026**.

### UDOC enterprise-SaaS readiness GAP list (priority)
1. **Multi-tenancy / client isolation** (per-tenant data on models/decisions/policy/audit) — biggest gap; currently single-tenant.
2. **EVA alignment**: rename/Add the 6 named dims + 0–10 + Composite score + **ESCALATE** outcome + per-dim thresholds.
3. **EVA Certificate** issuance + public verify endpoint (per APPROVE).
4. **Policy engine maturity**: rule versioning + COB approval state + signing + hot-reload + test harness.
5. **HITL routing + COB workflow** (ESCALATE→COB queue; rule veto).
6. **SaaS commercial**: 6-tier product plans, API keys/service accounts, usage metering, rate limits, per-tenant quotas (check `saas.py`).
7. **Enterprise auth**: SSO/OIDC + API keys.
8. **Observability/SLA**: <50ms tracking + async tiers + metrics + incident.
9. **Data lifecycle**: 10-yr retention, classification tiers, evidence export (FRIA/DPIA), POPIA deletion.
10. **Admin completion** (build the React console to the v9.3 tab map) + **regulator/replay/schema/exchange/lifecycle/evidence/control** pages.

### ✅ G.O.D.S Intelligence — BUILT (backend scaffold, internal-only) this session
- Models: `KnowledgeDoc` (archive/data-room: title/source/category/content_text/active…), `IntelState` (stage 1–5, corpus stats).
- Service `app/services/gods_intelligence.py`: ingest/set_active/remove (add-remove data updates corpus), `ask()` = **retrieval-grounded, citeable** answer over ACTIVE corpus (no hallucination; "not in corpus" otherwise), `guardrail_check()` = **Pillar VIII Human Primacy**, non-overridable (regex blocks override/disable-safety/subordinate-human), `MATURITY` ladder (Stage 1 ACTIVE Automated·Assistive → 2 Generative → 3 Agentic → 4 Recursive → 5 Singularity-Governance, 2–5 ROADMAP/gated), `MANDATE` (250-yr phases), `overview()`.
- Router `app/routers/intel.py` (prefix `/intel`, **INTERNAL ONLY**: write=admin/operator/gov, read also auditor; client/viewer → 403): `/state`, `/docs`, `/ingest` (multipart PDF/DOCX/TXT, reuses policy_engine.extract_text), `/ingest-text`, `PATCH /docs/{id}` (active), `DELETE /docs/{id}`, `/ask`. Audited INTEL_INGEST/REMOVE/QUERY. Registered in main.py.
- Verified: ingest 2 docs → stage 1, grounded EVA answer w/ citation; "override human oversight" BLOCKED (Pillar VIII); out-of-corpus handled.
- Honest framing: corpus-grounded internal brain; "training" = curating the indexed corpus; AGI/Singularity = ROADMAP (per G.O.D.S's own position paper, subsumed by Constitutional Doctrine). NOT client-exposed. Does NOT replace EVA yet (parallel; future successor per roadmap).

### PENDING after this session (sequenced per founder priority)
A. **UDOC completion** → align EVA to white-paper canon (6 named dims/0–10/Composite/ESCALATE) + EVA Certificate; build the v9.3 tab pages (control/evidence/exchange/incident/lifecycle/api/regulator/replay/schema/constitutional). Map Public/Private sector → demo domains.
B. **Admin completion** → React console mirroring the admin tab map, wired to platform-core across the eco-system (the static admin HTML is the UI/UX framework).
C. **Intelligence maturation + UI** → embed an Intelligence panel in the ADMIN (platform-internal / cockpit, NOT client udoc-app); personalized desktop/app sync; Drive/zip corpus ingestion at scale; Stage-2 generative synthesis layer (pluggable LLM) behind COB gate.
D. Multi-tenancy + SaaS commercial (tiers/API keys/metering) + EVA Certificate + policy versioning/COB workflow.

---
## Increment A DONE — EVA aligned to white paper + EVA Certificates
- `governance_bridge.py`: six named dimensions on 0–10 (**Validity, Reliability, Risk, Compliance, Stability, Impact**; Impact severity from di+spd+risk), **Composite EVA Score** (0–10), outcome **RESTRICT→ESCALATE** (gating: risk≥.6 | compliance<.80 | impact_sev≥.55 | composite<.60 → ESCALATE; risk≥.5 | composite<.75 → REVIEW). Verdict gained validity/reliability/impact/composite_eva/dimensions. `seal_payload()` helper added.
- `EvaCertificate` model + issuance on APPROVE in `decisions.py` (cert_id EVA-<hash12>, dims_json, HMAC seal; **issued_at bound to the signed payload** so verify matches). Endpoints `GET /decisions/certificates` + `GET /decisions/certificates/{cid}/verify`.
- udoc-app EVA view: Composite EVA Score + six dims (from `verdict.dimensions`, Risk/Impact inverted) + ESCALATE colours + inline certificate + "EVA Certificates" panel; api fetches `/decisions/certificates`. Built + pushed to mobile www.
- Verified: APPROVE composite 8.68 → cert issued → verify **valid:True**; ESCALATE (compliance .75); REVIEW (MEDIUM); BLOCK (biased, no cert). UI shows all six dims + composite + cert.

## Increment C START DONE — G.O.D.S Intelligence console embedded in platform-internal (admin)
- `platform-internal/src/consoles/Intelligence.tsx` + route `/intelligence` + launcher card + nav, gated `isInternal = is_admin || role∈{admin,operator,gov}` (backend `/intel/*` also enforces). api +`del`. Shows maturity ladder, corpus stats, **grounded ask + citations**, 250-yr mandate, Pillar VIII guardrails, archive **add (ingest-text) / remove (DELETE)**. Build (195KB) + runtime verified (login→Intelligence→state+ladder+grounded answer).

## PENDING (next increments)
- **UDOC v9.3 tab completion** in the admin console: u-control, u-evidence, u-exchange, u-incident, u-lifecycle, u-api, u-regulator, u-replay, u-schema, u-constitutional (per the admin tab map).
- **Multi-tenancy / client isolation** (per-tenant scoping on models/decisions/policy/audit) — top SaaS gap.
- **SaaS commercial**: 6-tier plans, API keys/service accounts, usage metering, rate limits (extend `saas.py`).
- **Policy engine maturity**: rule versioning + COB approval workflow + signing + hot-reload.
- **Intelligence Stage-2**: pluggable LLM synthesis layer behind COB gate; ingest the data-room (Drive/zips) at scale; embed an Intelligence assistant in the HTML cockpit too.
- **Sector → 7-demo mapping** (Public: Welfare/SARS/Justice/Health; Private: Corporate).
- Update the EVA white paper to reflect **GG54477 withdrawn 26 Apr 2026**.

---
## SESSION ADD — v2 whitepapers/patent alignment + UDOC client-station + corpus loader
- Read UDOC_Full_Technical_Whitepaper_v2.docx (393 paras: 4 deployment models, five-plane HW stack, BOM/budget, edge appliance classes, perf SLAs, GG54477 §17 [pre-withdrawal], 12 pillars) + UDOC_EVA_Technical_Whitepaper_v9_1.docx (CGS advisory; six dims incl **Confidence**; FPGA coprocessor claims 24/25; TPM mesh claim 37; FIPS 140-3 L3 HSM; HQ-OS claims 31-35; 5-phase deployment sequence; 5-tier licensing). Blueprint images = the 5-plane cutaway + 4 patent diagrams.
- **EVA alignment applied:** dim Reliability→**Confidence**; EvaCertificate += content_sha3 (SHA-3-256 of inputs) + policy_version + merkle_leaf; certificate now issued for **every** decision; verify uses SHA-3 payload; signature_alg "HMAC-SHA256 (PQC/Dilithium-ref)". CGS already advisory (BLOCK dimensional) — confirmed.
- **udoc-station/** (NEW): `bringup_selftest.py` (stdlib, 5-plane readiness → signed readiness_report.json; PASS/PARTIAL/DEPENDENCY/FAIL; verdict READY*/NOT-READY), `station.config.json`, `run_test_env.sh` (boots platform-core + runs self-test — VERIFIED **READY-WITH-DEPENDENCIES**), `install.sh` (venv + systemd, `--offline` air-gap), `Dockerfile.station` + `docker-compose.yml`, `README.md`. Honest: HSM/PQC/WORM/QPU = DEPENDENCY with software fallbacks.
- **tools/ingest_corpus.py** (NEW): ingest a folder OR .zip (the Drive export) into the Intelligence archive via gods_intelligence + extract_text. VERIFIED on the two whitepapers (157,872 chars → grounded ask cites them). User will PR/merge their full Drive zip; loader handles it; DB not shipped (user loads own corpus).
- **ALIGNMENT_AUDIT.md** (NEW) at repo root — full metric-by-metric table.
- Intelligence: public **offline** standalone app (their GODS_Intelligence_AI_Offline.html, 32KB, service-worker/corpus/offline) is the PUBLIC variant; our internal server-backed console stays PRIVATE/internal-only. Keep them distinct.

## PENDING (priority order, updated)
1. **Policy versioning + COB approval workflow + <5ms hot-reload** (the originally-next task; still pending).
2. Production crypto/hardware integration (liboqs PQC signing; HSM split-custody; Cassandra WORM 10-yr) — hardware-dependent; interfaces + posture checks already in place.
3. Remaining UDOC **v9.3 admin tab pages** (control/evidence/exchange/incident/lifecycle/api/regulator/replay/schema/constitutional).
4. Full **Drive corpus** ingest once the user provides the merged zip; test corpus add/remove/update at scale.
5. Tenancy UI (tenant switcher + tier/usage) in admin + client app; sector→7-demo mapping.

---
## SESSION ADD — Policy versioning + COB approval workflow + hot-reload (COMPLETE / verified)
**New model** `PolicyVersion` (pack_id, version, content_hash=SHA-3-256 of frozen rules, rules_json snapshot, rule_count, state PROPOSED|APPROVED|ACTIVE|VETOED|SUPERSEDED, proposed_by, reviewed_by, review_note, signature=HMAC seal, created_at, decided_at) + `PolicyPack.current_version`.
**policy_engine** hot-reload cache: module `_EPOCH`/`_MEMO`/`_LAST_RELOAD_MS`; `invalidate()` bumps epoch+clears memo; `active_rules()` memoised by (epoch,jurisdiction,sector,tenant_pk) and times the rebuild; `hot_reload_stats()`.
**policy.py** endpoints: `POST /packs/{id}/submit` (freeze enabled rules → PROPOSED version, pack PENDING_APPROVAL), `POST /versions/{vid}/approve` (COB gov/admin only; separation-of-duties: proposer≠approver when tier requires COB; supersedes prior ACTIVE; pack ACTIVE; `pe.invalidate()` hot-reload), `POST /versions/{vid}/veto` (reason → VETOED, pack DRAFT), `GET /versions?pack_id=`, `GET /versions/{vid}` (rules + signature_valid + content_hash_valid), `GET /hotreload`. `/packs/{id}/activate` is now the **fast-path**: auto-approves (proposer=approver) for non-COB tiers, else returns 409 directing to submit→COB-approve. `invalidate()` also called on rule PATCH + archive.
**COB requirement** by tier entitlement `cob` (Enterprise/Institutional/Sovereign = true) OR platform packs (tenant_pk NULL) always require COB.
**Verified (port 8104, fresh seed):** ACME(GROWTH) fast-path → version ACTIVE; DSD(ENTERPRISE) fast-path → 409; submit → PROPOSED; client self-approve → 403; COB(gov) approve → ACTIVE; decision on model-001 (credit scoring) → **BLOCK via PR-001 PROHIBIT** (matched credit, scoring); veto → VETOED; versions trail [(1,ACTIVE)]; version integrity sig_valid=True hash_valid=True; **hot-reload last_reload_ms 1.83ms (sub-5ms ✓)**. Smoke suite tests/test_governance.py = 8 passed.
**NOTE:** `/auth/register` returns 422 in this stack — DO NOT rely on it in tests; seed the user instead. Added gov COB officer **cob@gods.local / staff123** to seed.

## PENDING (priority order, updated)
1. **Production crypto/hardware seam** — unify EVA-cert + audit + policy-version signing behind a `crypto_provider` that uses liboqs (CRYSTALS-Dilithium) when installed, else HMAC fallback (honest "PQC/Dilithium-ref"); HSM-custody seam; report active backend in station self-test. (Software seam now; real PQC/HSM/Cassandra-WORM remain hardware-dependent.)
2. Remaining UDOC **v9.3 admin tab pages** in platform-internal (control/evidence/exchange/incident/lifecycle/api/regulator/replay/schema/constitutional).
3. Full **Drive corpus** ingest once the user provides the merged zip (loader ready: tools/ingest_corpus.py).
4. Tenancy UI (tenant switcher + tier/usage) in admin + client app; sector→7-demo mapping; update whitepapers to reflect GG54477 withdrawal.

---
## SESSION ADD — Unified PQC-ready crypto provider + HSM-custody seam (COMPLETE / verified)
**New** `app/services/crypto_provider.py`: single signing seam. `sign(payload)` → CRYSTALS-Dilithium via liboqs (`oqs`) when installed (prefix `dil:`), else HMAC-SHA256 (same `GODS_SOV_KEY` as the sovereign seal, so existing seals stay consistent). `verify(payload, sig)` is PQC- and HMAC-aware. `provider_info()` → {pqc_available, algorithm, label, hsm_mode software|pkcs11, custody}. HSM custody seam via `UDOC_HSM_MODE`. Software mode never claims certified hardware.
**Threaded:** `governance_bridge.seal_payload` now delegates to `crypto_provider.sign`; added `verify_payload(payload, sig)` → `crypto_provider.verify`. EVA-certificate verify (decisions.py) and policy-version signature verify (policy.py) switched from equality to `verify_payload` (so non-deterministic PQC sigs verify correctly). The internal per-decision sovereign seal + specialized `verify_seal(model_id,decision,svs,risk,seal)` left as deterministic HMAC (smoke tests depend on it).
**New endpoint** `GET /system/crypto` → provider_info. Station self-test L2 PQC check now queries it (PASS when liboqs present, else DEPENDENCY with honest label).
**Verified (port 8105 + station):** smoke 8 passed; `/system/crypto` = HMAC fallback/software custody (dev); decision cert verify valid=True; policy version signature_valid=True & content_hash_valid=True; station verdict READY-WITH-DEPENDENCIES with PQC check reflecting the live provider. On a station with liboqs installed, sign() uses Dilithium and the PQC check flips to PASS — no code change.

## PENDING (priority order, updated)
1. Remaining UDOC **v9.3 admin tab pages** in platform-internal (control/evidence/exchange/incident/lifecycle/api/regulator/replay/schema/constitutional).
2. Tenancy UI (tenant switcher + tier/usage) in admin + client app; sector→7-demo mapping.
3. Full **Drive corpus** ingest once the user provides the merged zip (tools/ingest_corpus.py ready).
4. Real hardware integration when in hand: install liboqs (PQC flips to PASS automatically), FIPS 140-3 L3 HSM (set UDOC_HSM_MODE=pkcs11 + PKCS#11 wiring), Cassandra WORM 10-yr; update whitepapers to reflect GG54477 withdrawal.

---
## SESSION ADD — UDOC v9.3 admin layer + self-contained admin console (COMPLETE / verified)
**Decision model** += `inputs_json` (governed inputs captured for replay) + `certificate_id` (links the decision to its EVA cert); decide() populates both. list_decisions now returns `id`.
**New router** `app/routers/admin_udoc.py` (prefix /udoc, tenant-isolated via principal+scope_pk):
- `GET /udoc/regulator/summary` — systems by status/risk, decisions by outcome, blocked/escalated, oversight open/total, active policy packs+rules+hot_reload, crypto provider, compliance basis (POPIA s71; GG54477 withdrawn).
- `GET /udoc/constitutional/pillars` — 12 G.O.D.S pillars with enforcement point + live status (PQC pillar reflects crypto_provider: ENFORCED if liboqs else PARTIAL). Status summary {ENFORCED:10, DECLARED:1, PARTIAL:1} in software mode.
- `GET /udoc/models/{model_id}/lifecycle` — status, stage (REGISTERED/OPERATING/BLOCKED), decision counts + last outcome.
- `GET /udoc/decisions/{id}/evidence` — decision + linked EVA cert (content_sha3, policy_version, merkle_leaf, dimensions) + audit chain head + inputs.
- `GET /udoc/decisions/{id}/replay` — re-evaluates stored inputs through the current EVA + active policy; returns original vs replayed + drift flag (reproducible when stable).
**Console** `platform-core/static/udoc_admin_v93.html` (self-contained, navy/gold/UDOC-purple, honest pre-registration labels) served at **`GET /udoc-admin`**; tabs Regulator/Constitutional/Lifecycle/Evidence/Replay wired live to the above. **Verified headless (Playwright):** all 5 tabs render — regulator ✓, constitutional 12 rows ✓, lifecycle OPERATING ✓, evidence cert+sha3 ✓, replay REPRODUCIBLE ✓. Smoke suite still 8/8.
**UI bug fixed (lesson):** the Load button must NOT call render() (which rebuilds the input bar and resets the id to its default before fetching). Split into loadLifecycle/loadEvidence/loadReplay that only refresh the result div and read a persisted lastMid/lastDid.

## PENDING (priority order, updated)
1. Extend the admin console / v9.3 tabs: remaining UDOC tabs as pages (control/kill-switch surface, data-exchange, incident, schema, api-keys, regulator evidence export/download).
2. Tenancy UI (tenant switcher + tier/usage + API-key issue) in admin + client app; sector→7-demo mapping.
3. Full **Drive corpus** ingest once the user provides the merged zip (tools/ingest_corpus.py ready).
4. Hardware integration when in hand: liboqs (PQC→PASS auto), FIPS 140-3 L3 HSM (UDOC_HSM_MODE=pkcs11), Cassandra WORM 10-yr; update whitepapers to reflect GG54477 withdrawal.

---
## SESSION ADD — v12: UDOC v9.3 admin tabs completed (COMPLETE / verified)
**admin_udoc.py +=** `GET /udoc/incidents` (BLOCK/ESCALATE feed + open oversight, tenant-scoped), `GET /udoc/exchange` (data-sovereignty/cross-border posture + DATA_LOCALISATION/MIN_SOVEREIGNTY active rules), `GET /udoc/schema` (self-describing governance schema for integrators), `GET /udoc/regulator/export` (signed evidence bundle: summary + recent decisions + audit head, sealed via crypto_provider).
**tenants.py +=** `GET/POST /tenants/me/apikeys` (tenant self-service keys). **BUG FIXED:** literal `/me/apikeys` was shadowed by `/{tid:int}/apikeys` (typed route 422'd on "me"); FastAPI matches in declaration order, so literal-segment routes MUST be declared before typed-param routes — moved /me routes (and KeyReq) above the /{tid} routes.
**Console (`/udoc-admin`) +=** tabs **Control** (kill-switch: list models + status dropdown → POST /registry/models/{id}/status?new_status=), **Incidents**, **Exchange**, **Schema**, plus a **Download signed evidence (JSON)** button on Regulator. Now 9 tabs.
**Verified (port 8111/8112):** schema 6 dims/8 rule-kinds; exchange ZA cross-border denied; biased decision → BLOCK shows in incidents; regulator export sealed (15 recent); self-service key POST 200 → prefix+api_key, lists 1, and the key authorizes (X-API-Key → model-001 only); kill-switch flips model-001 → SUSPENDED. Headless: control(2 rows)/incidents/schema/exchange render ✓. Smoke 8/8.

## PENDING (priority order, updated)
1. **v13** — Tenancy & commercial console tab (platform: list tenants + tier/status/usage + issue keys; client: own plan + usage + self-service keys; six-tier reference).
2. **v14** — Client self-service governance loop (console "Submit" tab: register a system + run a governed decision + view/verify the certificate).
3. Full Drive corpus ingest — USER is doing the zip + PR/merge (tools/ingest_corpus.py ready).
4. Hardware integration when in hand: liboqs (PQC→PASS), FIPS 140-3 L3 HSM (UDOC_HSM_MODE=pkcs11), Cassandra WORM 10-yr; whitepaper GG54477-withdrawal update.

---
## SESSION ADD — v13: Tenancy & commercial console tab (COMPLETE / verified)
**Console (`/udoc-admin`) += "Tenancy" tab** (reuses existing tenant endpoints; no backend change):
- Platform staff (no tenant): table of all tenants with tier_name + status pill + usage/quota bar; per-row controls — tier select→`POST /tenants/{id}/tier?tier=`, status select→`POST /tenants/{id}/status?status_value=`, `+Key`→`POST /tenants/{id}/apikeys`; plus a six-tier commercial reference table from `GET /tenants/tiers`.
- Tenant client: own Plan card (tier/sector/status + usage bar), Entitlements card, and self-service API keys (`GET/POST /tenants/me/apikeys`) with `+ Issue` (raw key shown once via alert).
- Helpers: usageBar(u,q); tnSetTier/tnSetStatus/tnIssueKey/tnIssueMyKey. POST-with-body via api(path,{method,headers,body}).
**Verified headless (port 8113):** platform tenancy renders 2 tenants + 6-tier reference (10 table rows); client plan view renders + **self-service key issued (gods_gov-dsd prefix shown)**. /tenants/me confirmed tier_name + entitlements present.

## PENDING (priority order, updated)
1. **v14** — Client self-service governance loop (console "Submit" tab: register a system + run a governed decision + view/verify the certificate).
2. Full Drive corpus ingest — USER doing zip + PR/merge.
3. Hardware integration when in hand (liboqs / FIPS HSM / Cassandra WORM); whitepaper GG54477-withdrawal update; sector→7-demo mapping.

---
## SESSION ADD — v14: Client self-service governance loop (COMPLETE / verified)
**Console (`/udoc-admin`) += "Submit" tab** (reuses registry + decisions + cert-verify; no backend change):
- Register a system: model_id/name/risk_tier/use_case → `POST /registry/models` (operator_id "self"; attaches to caller's tenant).
- Run a governed evaluation: model_id + raw_confidence + compliance + fair/biased sample → `POST /decisions`; renders outcome pill, composite EVA, six dimensions, certificate (id + content_sha3 + policy_version).
- Verify certificate → `GET /decisions/certificates/{id}/verify` → VALID/INVALID + signature_alg.
- Functions doRegister/doEvaluate/verifyCert. block_reasons is a LIST → join in UI.
**Verified headless (port 8116/8117 as client.dsd):** register "dsd-test-1" → status ACTIVE; fair evaluate → APPROVE, composite 8.7, dims (Validity 9.5/Confidence/Risk/Compliance 10/Stability 10/Impact); certificate EVA-… issued; Verify → VALID; biased sample → BLOCK. No console errors. Console now 11 tabs.
**Note:** Playwright `#sel >> text=` chained text-locator can falsely time out; use `button:has-text('…')` and read inner_text.

## PENDING (priority order, updated)
1. Full Drive corpus ingest — USER doing zip + PR/merge (tools/ingest_corpus.py ready).
2. Hardware integration when in hand: liboqs (PQC→PASS), FIPS 140-3 L3 HSM (UDOC_HSM_MODE=pkcs11), Cassandra WORM 10-yr.
3. Optional polish: whitepaper GG54477-withdrawal update; sector→7-demo mapping; revoke-API-key endpoint; client decision history view.
