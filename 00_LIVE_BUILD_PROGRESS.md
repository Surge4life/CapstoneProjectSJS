# 00_LIVE_BUILD_PROGRESS.md — Wiring the HTML admin to the live backend
> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity. See `BRAND_AND_ENTITY_CONSTANTS.md`.

**Approach (confirmed):** the **HTML admin cockpit is the live admin**, wired to `platform-core`; the thin React apps are **migrated** toward this design over time rather than rebuilt. **Order:** G.O.D.S Admin cockpit + UDOC governance (all governance pages) **first**; divisions **last**.

## How to run it live (local)
```bash
cd platform-core
pip install -r requirements.txt            # first time
python3 seed.py                            # seeds admin + model-001 + starter governance activity
python3 -m uvicorn app.main:app --port 8077
# open  http://127.0.0.1:8077/admin  → click the ● control (bottom-right) → password: admin123 → Connect
```
The cockpit is served **same-origin at `/admin`**, so the backend URL auto-fills and there is no CORS step. Login: `admin@gods.local` / `admin123` (staff roles use `staff123`). To point the cockpit at a remote deployment instead, open `GODS_Admin_Live.html` and set the Backend URL field.

## What is LIVE now (this increment — P1 partial)
The cockpit (`platform-core/static/admin.html`, source `GODS_Admin_Live.html`) keeps the full approved demo design and binds to real API data via a **live bridge** (a connect/login + typed API client + binding/poller injected before `</body>`):
- **Command Centre** — KPIs (AI Systems, Decisions Today, Non-Compliant, Sovereignty, Bias Flags, Open Oversight) bound to `/admin/status`, `/sovereignty/posture`, `/bias/scan`, `/compliance/sweep`; **Live Audit Stream** bound to `/audit/records` (real Merkle-chain events); 7s polling.
- **AI Registry** — `#full-reg-body` bound to `/registry/models`.
- **COB** — live oversight-case panel bound to `/oversight/cases`.
- **Audit Trail / UDOC Audit** — streams bound to `/audit/records`.
- The demo's mock loops (fake 1.41M counter, mock stream) are **neutralised on connect**; the clock is preserved. Verified end-to-end with Playwright against the running backend.
- **Backend:** `seed.py` now creates genuine EVA decisions + Merkle audit chain + an oversight case (chain verify = intact); `GET /admin` serves the cockpit.

## What remains (next increments, in order)
1. **Finish G.O.D.S Admin + UDOC governance pages → full parity & live:**
   - Compliance Engine + SA AI Policy GG54477 pillars ← `/compliance/frameworks` + `/compliance/sweep` (per-framework %).
   - Bias Monitor ← `/bias/scan` (+ per-decision detail); Sovereignty page ← `/sovereignty/posture`.
   - System Health ← `/health` + `/health/ready`; Model Lifecycle ← `/registry/models` + `/registry/models/{id}/status` (promote/suspend actions).
   - Evidence Bundles ← `/documents/*` + audit export; Constitutional Pillars/Risk ← derive from compliance+oversight; Incident/Breach ← oversight.
   - Wire **write actions** behind the demo buttons (Register System → `POST /registry/models`; Recruit/Resolve → `POST /oversight/cases[/resolve]`; Submit decision → `POST /decisions`) with toasts + refresh.
   - RBAC: respect `/access/profile` (`is_admin`, role) to show/hide actions.
2. **UDOC specifics** (udoc-app / udoc-* services) to the same standard.
3. **Divisions last** — S.E.T.H.S, T.S, M.A.D.I.B.A consoles ← `/seths/*`, `/ts/*`, `/madiba/*`, `/analytics/{div}/*`; portals UI on the working lifecycle API.
4. **React migration** — port the live bridge's design tokens/components into `platform-internal` / `platform-web` so the React shells match the cockpit (reuse, don't rebuild).
5. **Hardening + deploy** — visual-regression baselines, load/chaos, observability wiring, deploy, UAT (per `GODS_Live_Rollout_and_Test_Schedule.md`).

## Continuation method (for usage-limit resets)
- The live bridge lives in `GODS_Admin_Live.html` (and `platform-core/static/admin.html`). To wire another page: add a `render*()` that fetches the endpoint and fills the page's table/KPIs, then call it from `refreshAll()`. Bind KPIs by label via `setKpi(label,value)`; bind tables by their existing `tbody` id; inject a live panel where the demo has none.
- Test pattern (one shell): `seed.py` → background uvicorn → seed activity via httpx → Playwright `goto /admin` → click `.gl-hd`, fill `#gl-pass`, click `#gl-connect` → assert via `page.evaluate`.
- The backend only persists within a single bash invocation here, so always start it and test in the **same** command.
