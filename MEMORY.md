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
