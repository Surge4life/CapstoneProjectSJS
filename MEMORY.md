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
