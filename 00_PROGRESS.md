> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# GODS ECOSYSTEM — BUILD PROGRESS & SESSION HANDOFF
**This is the resume-point file.** Any new session reads this first, then continues from
the next unchecked item. It replaces redoing work with clean continuation.

> This is an engineering handoff document, not an instruction to bypass judgment.
> It records what is built, what is verified, and what is next — nothing more.

---

## THE TASK (as scoped honestly)
Build the **full software stack** for the G.O.D.S Holdings ecosystem — the code that gets
flashed onto / deployed to the UDOC sovereign hardware node — structured so that on boot
it validates each hardware connection, reports pass/fail, and reaches live status.
Software is built for real and tested in **emulation**; the final on-silicon pass happens
when the physical hardware is switched on (only the real board can return that result).

Target hardware = the architecture in `UDOC_Full_Hardware_Specification v1.0` (read & captured).

## HARDWARE TARGET (from the spec — what the code is written against)
- **5 planes:** embedded governance fabric · ingestion/control · governance/processing ·
  immutable data operations core · security/operations.
- **Node classes:** K8s control (3/site), ingress/API (2–4), governance workers (4–8, FastAPI),
  GPU analytics (0–2), PostgreSQL HA (3), Cassandra/WORM audit (6), Kafka (5 brokers),
  Redis (3), OpenSearch (ingest+data), object archive (S3 immutable), HSM (2/site).
- **Peripherals the boot self-test must validate:** FPGA-over-PCIe (enforcement),
  HSM/TPM (sovereign key + crypto), NIC (sovereignty packet inspection) — "full UDOC node".
- **Non-negotiables:** air-gap capable · every AI event → immutable signed audit + lineage ·
  mandatory human-oversight enforcement/suspension/override · sub-50 ms governance overhead ·
  master key never leaves HSM · FIPS 140-3 L3 (gov) · PQC: CRYSTALS-Dilithium signatures,
  hybrid TLS 1.3 · signed offline-capable release pipeline.
- **4 governance attachment packages:** UDOC Agent (host process), UDOC Sidecar (container),
  UDOC Gateway (appliance), UDOC Edge Node (1–3 appliance cluster). Fail-closed for critical.

## CANONICAL EXISTING STACK (from `_zip` → package_v38 — build ON this, don't reinvent)
React 18 + Vite + TS (apps/web) · FastAPI + SQLAlchemy2 + Pydantic2 (apps/api) ·
PostgreSQL 16 · Redis 7 · Redpanda/Kafka · OpenSearch 2.15 · JWT+bcrypt · docker-compose ·
API routers already exist for: admin, audit, auth, bias, compliance, decisions, health,
intelligence, lineage, madiba, oversight, registry, seths, sovereignty, ts, workforce.

---

## DELIVERY STRUCTURE (per-system zips → one ecosystem zip)
```
GODS_ECOSYSTEM/
├── 00_TASK1_CONTENT_INVENTORY.md          [DONE]
├── 00_PROGRESS.md                         [this file]
├── 00_ARCHITECTURE.md                     [DONE]
├── platform-core/        FastAPI backend (all division routers + governance) [IN PROGRESS]
├── platform-web/         React: GODS Admin + division consoles                [TODO]
├── udoc-public/          External clients/gov platform + API                  [TODO]
├── udoc-internal/        GODS-internal audit/monitoring platform              [TODO]
├── governance-engines/   EVA + UDOC orchestrator + GODS loop (TS, hardened)   [TODO - port from capstone-source]
├── hw-bringup/           ★ boot-to-live: bootloader cfg, init, device drivers,
│                          self-test, systemd units, OS image build            [TODO]
├── udoc-agent/           host-process governance attachment                   [TODO]
├── udoc-sidecar/         container governance attachment                      [TODO]
├── udoc-gateway/         appliance governance attachment                      [TODO]
├── udoc-edge/            edge node governance attachment                      [TODO]
├── infra/                docker-compose, k8s manifests, CI                    [TODO]
└── DEPLOY.md             one-command run + flash-to-hardware guide            [TODO]
```

---

## BUILD CHECKLIST (tick as completed; each item is independently verifiable)

### Phase A — Foundation & records
- [x] A1. Unlock both zips, full content inventory → `00_TASK1_CONTENT_INVENTORY.md`
- [x] A2. Read hardware spec, capture node classes/peripherals → this file + ARCHITECTURE
- [x] A3. Write ARCHITECTURE.md (planes → services → hardware map)
- [x] A4. Scaffold GODS_ECOSYSTEM dir tree + root README + DEPLOY.md skeleton

### Phase B — Platform core (backend)
- [x] B1. FastAPI app skeleton: config, security(JWT+bcrypt), db session, health
- [x] B2. SQLAlchemy models + initial migration (registry, decisions, audit refs, workforce, capital, projects)
- [x] B3. Division routers w/ real service logic: SETHS, MADIBA, TS, oversight, sovereignty, compliance, bias, decisions, audit, registry, intelligence, lineage
- [x] B4. Governance engine bridge (Python EVA/UDOC in governance_bridge.py) (call EVA/UDOC TS engines or port logic to Python service)
- [x] B5. Event bus + immutable audit writer (hash-chain + Merkle) (Kafka/Redpanda producer/consumer) + immutable-audit writer (Cassandra pattern, hash-chain + Dilithium ref)
- [x] B6. pytest suite 8/8 green; uvicorn boots clean suite, all green; `uvicorn` boots clean

### Phase C — Governance engines
- [x] C1. Ported EVA+UDOC+GODS into governance-engines/, all run & verified EVA + UDOC orchestrator + GODS loop from capstone-source into governance-engines/, compile clean, demos run
- [x] C2. Documented bridge relationship; Python governance_bridge is the sync svc path as a callable service (HTTP or child-process) the backend uses

### Phase D — Frontends (React)
- [x] D1. platform-web shell: routing, auth, branded layout, API client: routing, auth, shared UI, GODS branding (navy/gold, logo)
- [x] D2. GODS Admin console (AdminDash + loop snapshot) (consolidate mainframe HTML → React)
- [x] D3-D5. SETHS + MADIBA + TS consoles (live metrics + actions) · D4. MADIBA console · D5. TS Industries console
- [x] D6. UDOC public console (live decision runner + registry) (client/gov: registry, decisions, compliance views)
- [x] D7. UDOC internal audit console (chain verify + Merkle) (audit, lineage, sovereignty, bias monitoring)
- [x] D8. Vite production build clean (42 modules, bundle emitted) for each

### Phase E — Hardware bring-up (the flash-to-hardware stack)
- [x] E1. OS image plan + build recipe (boot/OS_IMAGE.md) (minimal Linux, immutable rootfs) + build script
- [x] E2. Bootloader (GRUB UEFI) + systemd units (selftest→platform→live-status) targeting the spec node class
- [x] E3. Device drivers: FPGA-PCIe, HSM-PKCS11, NIC-inspect (+emulation shims): FPGA-over-PCIe driver/IOCTL contract, HSM/TPM (PKCS#11) client, NIC inspection hook — written against the spec, emulation-mocked
- [x] E4. udoc-selftest: probes FPGA/HSM/NIC/data-core, PASS→live / fault→fail-closed (`udoc-selftest`): probes FPGA, HSM, NIC, DB reachability; emits pass/fail + reaches live status; systemd unit ordering
- [x] E5. boot-sequence emulator proves gated boot logic (healthy→LIVE, fault→HELD) proving the boot sequence + self-test logic runs and reports correctly with mocked devices
- [x] E6. Signed offline release/import manifest tooling — pack+verify, tamper-detecting (infra/release-tooling)

### Phase F — Integration, infra, packaging
- [x] F1. docker-compose full stack + Dockerfiles (dev + prod profile): full stack up (postgres, redis, redpanda, opensearch, api, web, udoc-public, udoc-internal)
- [x] F2. Inter-service handshakes verified live (agent→core APPROVE/BLOCK, fail-closed, edge offline) (service↔service mTLS contract, auth tokens, health gating)
- [x] F3. 4 attachment packages built (agent/sidecar/gateway/edge), all run + sidecar/agent/gateway/edge deployment templates
- [x] F4. End-to-end smoke test — 17/17 stages pass (smoke_test.py)
- [x] F5. Per-system zips (9) + master GODS_ECOSYSTEM.zip; verified run-from-extracted, then one GODS_ECOSYSTEM.zip; verify everything resolves
- [x] F6. DEPLOY.md complete (local run + flash-to-hardware + honest boundary) complete (one-command local run + honest flash-to-hardware procedure)

---

## VERIFICATION RULE (every phase)
Nothing is ticked until it is actually verified: backend → `pytest` + `uvicorn` boots;
frontends → `vite build` succeeds; engines → compile + demo runs; bring-up → QEMU/emulation
harness runs the boot+selftest logic; packaging → zip link/contents check. Honest status only.

## HONEST BOUNDARY (restated, lives in every component README)
- Software, OS image, drivers, bootloader, self-test, services = **built for real**, tested in **emulation**.
- Final "runs error-free on the physical board" = **happens when hardware is switched on**;
  the self-test we ship is exactly what produces that pass/fail on first boot.
- No fabricated "validated on silicon" claims. Driver code targets the spec's interfaces;
  where the spec leaves a device detail open, the code uses a clearly-marked contract/stub
  a hardware engineer finalises against the real datasheet.

## NEXT ACTION
→ ALL PHASES COMPLETE (A–F). Ecosystem verified end-to-end (17/17). Build is feature-complete for the software scope; remaining work is real-hardware finalisation (on-silicon driver register specifics + first-boot PASS), which is out of software scope by definition.

### Phase G — Dedicated division platforms + UDOC analytics (added)
- [x] G1. UDOC data-record-and-analytics backend: DivisionRecord model + analytics_engine
      (record/timeseries/totals/recent/kpis) + /analytics/{division}/* router (39 routes total)
- [x] G2. Division routers wired to record every event into the UDOC analytics store
- [x] G3. seths-platform/ — standalone React app (KPIs, output time-series, records); vite build clean
- [x] G4. madiba-platform/ — standalone React app (inflow-vs-recycled bars, ratio); vite build clean
- [x] G5. ts-platform/ — standalone React app (SPV revenue bars, portfolio); vite build clean
- [x] G6. All three platform data paths verified live through UDOC analytics
- [x] G7. Smoke test extended → 22/22 stages pass (incl. analytics layer)


### Phase H — Portals, PWA, native .apk project, assessment response (this session)
- [x] H1. Portal models: students, employers, opportunities, applications, employees, timesheets
- [x] H2. Student portal API (register, progress, browse, apply)
- [x] H3. Employer portal API (register, post opportunity, review applicants, offer→placement)
- [x] H4. Employee portal API (profile, timesheet, payslip w/ SA UIF+PAYE)
- [x] H5. portals-web installable PWA — Student/Employer/Employee, runtime-configurable backend URL
- [x] H6. Full cross-portal lifecycle verified over HTTP (student→employer→employee→payslip)
- [x] H7. CORS verified for capstoneprojectsjs.netlify.app origin
- [x] H8. Smoke test extended → 26/26 (incl. portal lifecycle)
- [x] H9. Real Capacitor Android project generated (android/ — gradlew, build.gradle, app module)
- [x] H10. BUILD_APK.md — 3-command .apk build on user's machine (sandbox blocks Google SDK only)
- [x] H11. 00_ECOSYSTEM_STATUS.md — response to external assessment (10 gaps mapped, ~88-92%)
- [x] H12. infra starters: terraform/, k8s/, observability/, IDENTITY.md, SECURITY.md, TRACEABILITY.md, openapi.json
- [x] H13. IP/ patent evidence repository structure

## .APK BOUNDARY (confirmed this session — tools, not skills)
The full native Android project builds with `npm run apk:debug` on any machine with Android
Studio. This sandbox cannot compile it ONLY because dl.google.com (Android SDK) and
services.gradle.org are not in its network allowlist — proven by direct test (403). JDK 21 is
present; the project, gradle wrapper, and build files are all generated and valid.

### Phase H — Portals, mobile, analytics, assessment response (added)
- [x] H1. Portal models: students, employers, opportunities, applications, employees, timesheets
- [x] H2. Student portal API (register, progress, browse, apply)
- [x] H3. Employer portal API (register, post opportunity, review applicants, offer→placement)
- [x] H4. Employee portal API (profile, timesheet, payslip with SA UIF/PAYE)
- [x] H5. Full cross-portal lifecycle verified over HTTP + in smoke test (26/26)
- [x] H6. portals-web — installable PWA, runtime-configurable backend URL, 3 role portals; vite+PWA build clean
- [x] H7. CORS verified for capstoneprojectsjs.netlify.app origin (live web→backend connection)
- [x] H8. portals-mobile — complete Capacitor Android project for real .apk (compile needs SDK on a real machine)
- [x] H9. UDOC analytics layer + 3 standalone division platforms (seths/madiba/ts) — built earlier this arc
- [x] H10. Assessment response (00_ECOSYSTEM_STATUS.md): 10 gaps mapped; infra starters (terraform/k8s/observability),
          IP/ repo, IDENTITY/SECURITY/TRACEABILITY docs, OpenAPI export (45 paths) all added
- [x] H11. Smoke test extended to 26 stages (analytics + portal lifecycle), all green

## .APK — honest status
The full Capacitor project (portals-mobile/) is built and bundles the real portals web app.
A signed .apk cannot be compiled in this sandbox: no Android SDK, and Google's Maven + Gradle
distribution are firewall-blocked (403). On any machine with Android Studio + JDK, three commands
(`npm i` → `npx cap add android` → build) produce the signed .apk. The PWA is installable today
with no toolchain. This is a sandbox/tooling limit, not a design gap.

### Phase I — Four dedicated app backends + document store (IN PROGRESS)
- [x] I1. Document store service (real file persistence, sha256 integrity, UDOC-recorded) + /documents API (upload/download/list/meta)
- [x] I2. SaaSClient model + /saas API — UDOC .apk: clients register, get API key, govern OWN AIs, kill-switch suspend/resume, dashboard
- [x] I3. MADIBA engagement model + /madiba/engage API — investor pipeline (INTRODUCED→FUNDED), project updates
- [x] I4. TS submission + partner models + /ts/submit API — project submit/track + apply-to-partner
- [x] I5. SETHS document upload/download wired to records DB via UDOC (the requested fetch-from-DB feature)
- [x] I6. All 4 app backends verified; backend now 70 routes
- [x] I7. UDOC client app (PWA+Capacitor): AI control console, kill-switch — build clean (PWA + Capacitor): AI control console
- [x] I8. SETHS app (PWA+Capacitor): student + document upload/download UI — build clean (PWA + Capacitor): student/employer/employee + doc upload/download UI
- [x] I9. MADIBA app (PWA+Capacitor): investor engagement + pipeline UI — build clean (PWA + Capacitor): investor engagement + project updates UI
- [x] I10. TS app (PWA+Capacitor): project submit/track + partner application UI — build clean (PWA + Capacitor): project submission/tracking + partner application UI
- [x] I11. G.O.D.S admin stays platform-web (browser-only, password HTTPS) — no apk by design: password-protected HTTPS web only (NO apk) — already platform-web; add auth gate note
- [x] I12. 4 Capacitor projects (udoc/seths/madiba/ts-mobile) for real .apk; smoke test 31/31; repackaged projects for real .apk compile; extend smoke test; repackage

## App distribution model (per your spec)
- UDOC .apk — SaaS clients control their deployed AIs
- SETHS .apk — students/employers/employees + document upload/fetch from records DB
- MADIBA .apk — sovereign/institutional investor engagement + project updates
- TS .apk — SPV/gov/private project submission, tracking, partner-build applications
- G.O.D.S — NO .apk; secure password-protected HTTPS web access only (control plane stays browser-only)

### Phase J — Internal/external network split + internal staff consoles
- [x] J1. Network topology documented (00_NETWORK_TOPOLOGY.md): internal bind + external gateway, deny-by-default
- [x] J2. NGINX external edge allow-list (infra/edge/nginx.conf) — only external-safe paths proxied; internal blocked
- [x] J3. platform-internal SPA — staff work environment, network-locked, 5 consoles
- [x] J4. SETHS Ops console (cohort management)
- [x] J5. MADIBA Ops console (capital cycles + investor pipeline review)
- [x] J6. TS Industries Ops console (submission screening + SPV deployment)
- [x] J7. UDOC Governance console (decisions, oversight cases, audit, sovereignty) — INTERNAL ONLY
- [x] J8. operator_id surfaced in registry; all four consoles verified live; build clean

### Phase K — G.O.D.S core as role/division launcher
- [x] K1. access_control service: role+division → permitted internal systems (server-authoritative)
- [x] K2. /access/profile (launcher source) + /access/guard/{system} (hard 403 enforcement)
- [x] K3. platform-internal rebuilt as a LAUNCHER: shows only permitted systems; Guarded console wrappers
- [x] K4. seed extended with staff roles (operator/auditor/exec/viewer across divisions)
- [x] K5. verified: SETHS op scoped to own systems, hard-denied udoc-gov; admin opens all; smoke 34/34

### Phase L — V&V stress + chaos suite (assessment gap #10 closed)
- [x] L1. tests/stress_chaos.py — 500 concurrent decisions, adversarial inputs, malformed payloads, outage fail-closed, unknown-model burst
- [x] L2. FOUND & FIXED a real concurrency bug: audit hash-chain race under concurrent writes → serialized appends (_append_lock)
- [x] L3. verified: 10/10 stress+chaos checks pass; governance p95 0.08ms under 500-way load; chain intact; unit tests still 8/8
- [x] L4. assessment gap #10 (V&V) moved Partial → DONE

### Phase M — Render deployment (Netlify suspended → Render)
- [x] M1. config accepts Render DATABASE_URL (unprefixed) + normalizes postgres:// → postgresql://; psycopg added
- [x] M2. render.yaml blueprint: Postgres + platform-core (web) + platform-internal + portals (static), health check, generated JWT secret
- [x] M3. .gitignore (excludes node_modules/dist/db/_packages/.env)
- [x] M4. 00_DEPLOY_TO_RENDER.md — GitHub-first then one-click Blueprint guide; free-tier caveats documented
- [x] M5. verified: unit tests 8/8 after config change; DATABASE_URL override + scheme fix confirmed

### Phase N — .apk SDK build prep (complete except on-machine compile)
- [x] N1. Android resources for all 5 mobile projects: network_security_config (cleartext for LAN/tunnel), strings.xml, manifest permissions
- [x] N2. build-apk.sh per project: web build → cap add android → sync → apply resources → assembleRelease
- [x] N3. fresh web builds rebundled into each */www (apps wrap current code)
- [x] N4. non-SDK build steps dry-run validated (web build, resource copy, config, bash syntax)
- [x] N5. master 00_BUILD_APKS.md at root: prerequisites + one-command build + signing steps
- [ ] N6. SDK compile → signed .apk (USER-SIDE: runs on a desktop with Android Studio + JDK17 + Node18)

### Phase O — LIVE on Render (deployed + verified)
- [x] O1. Backend gods-platform-core LIVE: /health ok, /docs live, environment=production
- [x] O2. Fixed psycopg driver: postgresql+psycopg:// (psycopg2 not installed) — deploy succeeded
- [x] O3. Auth verified live: admin login → 200 + JWT (role/division from live Postgres)
- [x] O4. EVA governance engine verified live: BLOCK (HIGH risk, sealed) + APPROVE (MINIMAL, sealed), sub-ms
- [x] O5. Both static sites deployed (gods-platform-internal, gods-portals)
- [x] O6. Fixed VITE_API_BASE → full https URL for both static sites; portals default to env var

### Phase P — Desktop (.exe) applications via Electron
- [x] P1. Five Electron projects: udoc/seths/madiba/ts/portals-desktop (load live site in native window)
- [x] P2. main.js per app (window, no menu bar, external links to browser, offline-friendly fallback); all validated with node --check
- [x] P3. electron-builder config → Windows .exe (NSIS installer + portable); icons generated
- [x] P4. verified electron-builder installs/runs; Electron runtime downloads on user desktop (firewall-blocked in sandbox)
- [x] P5. master 00_BUILD_DESKTOP_APPS.md + per-project READMEs; PWA-install path documented as the no-build option
- [ ] P6. .exe compile (USER-SIDE: npm install && npm run dist on a Windows desktop with Node 18+)

### Phase Q — Full start-to-finish APK build runbook
- [x] Q1. 00_START_HERE_BUILD_APK.md — nothing-assumed Windows runbook: files → Node → terminal → cap add/sync → Android Studio → APK → install on phone
- [x] Q2. Cheat-sheet of the 6 common first-build snags with exact fixes (SDK location, Gradle JDK, platform, ANDROID_HOME, cleartext, stuck sync)
- [x] Q3. UDOC app defaults to live Render backend so the .apk auto-connects

### Phase R — First .apk built + handoff for next chapter
- [x] R1. udoc-mobile .apk BUILT on user desktop (app-debug.apk 3.8MB), installed on Android, connects live to Render, client-register + 4 dashboards working
- [x] R2. MEMORY.md — full project state/handoff for a fresh chat (what is live, fixes applied, systems map, next chapter)
- [x] R3. SKILLS.md — all hard-won technical know-how, gotchas, exact build/deploy/git/apk procedures
- [ ] R4. NEXT CHAPTER (new chat): systematically upgrade live system toward the .html demo vision → SaaS-client-ready stack
