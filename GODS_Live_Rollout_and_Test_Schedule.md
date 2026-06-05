# G.O.D.S ECOSYSTEM — LIVE ROLLOUT & TEST SCHEDULE
**Bringing the live systems up to the demo UI (look, feel, function & control)**
Sashin J. Singh · G.O.D.S Holdings (Pty) Ltd *(proposed)* · June 2026 · pre-registration forecast

---

## 0 · Purpose
The HTML demos (chiefly `GODS_Admin_Mainframe_Branded_v6.html` — ~18 governance pages, EVA Command Centre, live counters, audit stream, GG54477 + Bill-of-Rights dashboards) show what the finished product *looks and behaves* like. The live ecosystem has a **strong backend but thin frontends**. This schedule closes that gap in controlled phases, each with explicit **test gates**, so the live apps end up matching the demo while being genuinely wired to the real API.

## 1 · Honest baseline (what exists today)
| Layer | State |
|---|---|
| **Backend** (`platform-core`) | **Strong.** FastAPI, ~25 routers / 53 routes: auth, audit (Merkle chain), decisions, bias, compliance, oversight (COB), registry, analytics, sovereignty, documents, intelligence, division endpoints (seths/ts/madiba), portal lifecycle. Smoke 22/22; e2e green. |
| **Admin/staff UI** (`platform-internal`) | **Thin.** 259 lines — 5 console stubs + shell. |
| **Public platform** (`platform-web`) | **Thin.** 263 lines — 7 short page stubs. |
| **UDOC app** (`udoc-app`) | **Thin.** 85 lines — single view. |
| **Division platforms** (`seths/ts/madiba-platform`) | Basic React + charts. |
| **Demo** (`GODS_Admin_Mainframe_Branded_v6.html`) | **Rich, static.** ~18 pages, full design, mock data, live-looking counters. **This is the parity target.** |

**Conclusion:** the work is overwhelmingly **front-end + wiring**, not new backend. Where a demo page has no endpoint yet, we add a thin endpoint or a clearly-labelled stub.

## 2 · Target ("done") state
Every demo page exists as a live page with the same layout, brand, and controls, backed by real API calls and auth, with loading/empty/error states, on the real datastore. Live counters/streams poll the backend. Role-based access matches the 18-role model. Visual parity with the demo within agreed tolerance.

---

## 3 · Rollout phases

### P0 — Foundation & parity harness  *(gate before any page work)*
- Shared **design system** extracted from the demo into the React apps: tokens from `branding/gods.brand.css`, the topbar + classification ribbon + left-nav shell, panel/badge/table/counter components, fonts.
- Shared **API client** (typed) over all 53 routes; auth/session; runtime backend URL (already present in portals) reused everywhere.
- **Parity harness:** Playwright visual-regression baselines captured from the demo for each page.
- **Tests/gate:** design-system Storybook renders; API client unit tests; CI runs lint + typecheck + Playwright; baseline screenshots committed.

### P1 — G.O.D.S Admin platform (governance cockpit)  *(highest priority)*
Pages to reach demo parity (wired to routers in brackets):
- Command Centre dashboard — KPIs, live decision counter, audit stream, division cards `[admin, analytics, decisions, audit]`
- 12 Constitutional Pillars + Bill-of-Rights tracking `[compliance, oversight]`
- COB — Oversight Board (queue, HITL approve/pause) `[oversight, decisions]`
- Constitutional Audit + Audit Trail (Merkle chain viewer) `[audit]`
- Breach / Incident Register + Incident Command `[compliance, oversight]`
- System Health `[health]`
- **Tests/gate:** per-page integration tests against a seeded DB; visual diff ≤ tolerance vs demo; HITL decision e2e (create → pause → approve → audit entry); RBAC test (admin vs viewer).

### P2 — UDOC governance suite
- UDOC Dashboard, AI Registry (register/list models), Compliance Engine, Bias Monitor, Sovereignty, Model Lifecycle, Evidence Bundles, Policy-as-Code `[registry, compliance, bias, sovereignty, intelligence, documents]`
- HQ-OS Quantum Layer panel (status/phases — read-only, honest "emulated" labels).
- **Tests/gate:** model-registration e2e (register → governs → appears in registry → audit); bias-scan flow; sovereignty checks; evidence-bundle export verified.

### P3 — Division systems (S.E.T.H.S, T.S, M.A.D.I.B.A)
- Each division console to demo parity, wired to its endpoints `[seths, ts, madiba, analytics]`: dashboards, records, division-specific actions (placements, projects, capital).
- **Tests/gate:** division CRUD + analytics integration tests; cross-division roll-up on Command Centre matches division pages.

### P4 — Portals & cross-portal lifecycle UI
- Student → Employer → Employee portal UI on the existing working lifecycle API `[portal_student, portal_employer, portal_employee]`, including SA UIF/PAYE payslip views.
- **Tests/gate:** full lifecycle e2e through the UI (register → opportunity → apply → offer → placement → timesheet → payslip), recorded by UDOC.

### P5 — Live behaviours & polish
- Real-time: polling/SSE for counters, audit stream, alerts; clock; toasts; optimistic HITL actions.
- Empty/loading/error states; accessibility (WCAG AA); responsive; the pre-registration ribbon retained.
- **Tests/gate:** streaming integration tests; a11y audit; mobile/responsive visual diffs.

### P6 — Hardening & non-functional
- Observability wiring (the `infra/observability` Prometheus/Grafana/OTel starters) to live metrics; structured logs; basic SIEM signals.
- Load/stress (k6/Locust) on hot endpoints; soak; chaos (kill a service, verify audit-chain integrity — extends the existing stress suite).
- Security: auth hardening, dependency scan, OWASP pass; secrets out of code.
- **Tests/gate:** load targets met; chaos suite green; security scan clean.

### P7 — Deploy & UAT
- Deploy the updated frontends + backend to the existing hosting; smoke on the live URL; seed demo accounts (`@gods.local`).
- **UAT script:** walk every demo page on the live deployment and confirm parity + function.
- **Exit:** UAT sign-off; `00_ECOSYSTEM_STATUS.md` updated; tag release.

---

## 4 · Test strategy (applies across phases)
- **Unit** (Vitest/Pytest): components, hooks, API client, backend services.
- **Integration**: each page against a seeded test DB via a running API (Pytest + httpx; React Testing Library + MSW).
- **End-to-end** (Playwright): the user journeys named in each phase gate.
- **Visual regression** (Playwright snapshots): every page vs the demo baseline; fail on > tolerance.
- **Contract**: frontend types generated/checked against the backend OpenAPI (`/openapi.json`).
- **Non-functional**: load/stress/soak/chaos (P6); a11y (P5); security scan (P6).
- **CI gates**: lint + typecheck + unit + integration + visual must pass to merge; e2e + load on a nightly/pre-release pipeline.
- **Definition of Done (per page):** matches demo layout/brand within tolerance · wired to real endpoint(s) · loading/empty/error states · RBAC enforced · unit + integration + visual tests green · appears in the live UAT walkthrough.

## 5 · Milestones (relative, sequence not calendar)
1. **M1 — Parity harness live** (P0 complete): design system + API client + visual baselines in CI.
2. **M2 — Admin cockpit at parity** (P1): the G.O.D.S Admin platform looks/behaves like the demo, live.
3. **M3 — UDOC suite at parity** (P2).
4. **M4 — Divisions + portals at parity** (P3–P4).
5. **M5 — Live & hardened** (P5–P6).
6. **M6 — Deployed + UAT signed off** (P7).

## 6 · Honesty notes
- Where the demo implies a capability with **no real backend** (e.g., parts of HQ-OS quantum, live SOC), the live page is labelled **emulated / forecast** rather than faked — consistent with the project's first pillar.
- Operational items needing real running infra and an ops team (multi-region datastores under load, real SIEM, on-silicon hardware) remain a **deployment/ops boundary**, not application code, and are scoped in P6 as starters.

---
*Build proceeds against this schedule; `MEMORY.md` / `SKILLS.md` track progress so work resumes across usage limits. Status changes update `BRAND_AND_ENTITY_CONSTANTS.md` first.*
