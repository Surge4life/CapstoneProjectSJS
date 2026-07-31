# Documentation structure · CapstoneProjectSJS

**Purpose:** Organizational map of all documentation by **category** and **relevance**.  
**Date:** 2026-07-31  
**Rule:** Intent and Capstone evidence live in `udoc-mvp/`. Long-form design law lives in `docs/` (Engineering Canon). Files are not relocated; this index assigns correct category and audience.

---

## Two documentation planes

| Plane | Path | Relevance |
|-------|------|-----------|
| **A. Capstone / live UDOC** | `udoc-mvp/` | Assessor grading, live hosts, packages, smoke, limits, EDRs |
| **B. Engineering Canon** | `docs/vol-*` | Constitutional architecture, engines, API, DB, UI law, infrastructure vision |

**Capstone assessors** start on Plane A.  
**Architects / deep implementers** use Plane B after Plane A intent is clear.  
Canon philosophy is **frozen** for Capstone (`udoc-mvp/CANON_FREEZE_NOTICE.md`); implement from it, do not expand it instead of verifying live.

---

## Plane A — Capstone / live UDOC (`udoc-mvp/`)

### Category 1 · Entry and framing
*Who should read first; what is and is not claimed*

| Document | Relevance |
|----------|-----------|
| [CAPSTONE_COVER_NOTE.md](udoc-mvp/CAPSTONE_COVER_NOTE.md) | Submission framing |
| [ASSESSOR_READING_ORDER.md](udoc-mvp/ASSESSOR_READING_ORDER.md) | 15- and 45-minute paths |
| [GLOSSARY.md](udoc-mvp/GLOSSARY.md) | Shared term meanings |
| [README.md](udoc-mvp/README.md) | Folder index (categorical) |

### Category 2 · Engineering decisions (EDRs)
*Durable “why” records — change these when direction changes*

| Document | Relevance |
|----------|-----------|
| [EDR-001-udoc-only-deploy-layer.md](udoc-mvp/EDR-001-udoc-only-deploy-layer.md) | Only UDOC deploys as product layer |
| [EDR-002-internal-vs-client-packages.md](udoc-mvp/EDR-002-internal-vs-client-packages.md) | Staff vs tenant package split |
| [EDR-003-free-tier-constraints.md](udoc-mvp/EDR-003-free-tier-constraints.md) | Neon/Render limits as design |
| [EDR-004-demo-seed-no-registration-smoke.md](udoc-mvp/EDR-004-demo-seed-no-registration-smoke.md) | Smoke without new registration |

### Category 3 · Architecture and packages
*What deploys, who uses which surface*

| Document | Relevance |
|----------|-----------|
| [ARCHITECTURE_MAP.md](udoc-mvp/ARCHITECTURE_MAP.md) | One-page stack + deploy diagram |
| [CAPSTONE_PACKAGE_STORY.md](udoc-mvp/CAPSTONE_PACKAGE_STORY.md) | Demos 1–7 → Internal/Client channels |
| [UDOC_MVP_PACKAGE_MATRIX.md](udoc-mvp/UDOC_MVP_PACKAGE_MATRIX.md) | Package progress checklist |
| [UDOC_CLIENT_PACKAGE_NOTES.md](udoc-mvp/UDOC_CLIENT_PACKAGE_NOTES.md) | Client channel detail |
| [UDOC_INTERNAL_PACKAGE_NOTES.md](udoc-mvp/UDOC_INTERNAL_PACKAGE_NOTES.md) | Internal channel detail |
| [UDOC_LIVE_ENVIRONMENTS.md](udoc-mvp/UDOC_LIVE_ENVIRONMENTS.md) | Live hosts, routes, user classes |

### Category 4 · Roadmap, limits, honesty
*Scope control and non-claims*

| Document | Relevance |
|----------|-----------|
| [ENGINEERING_ROADMAP_CAPSTONE.md](udoc-mvp/ENGINEERING_ROADMAP_CAPSTONE.md) | Freeze list, phases, Capstone bar |
| [LIMITATIONS_REGISTER.md](udoc-mvp/LIMITATIONS_REGISTER.md) | Named gaps |
| [UDOC_SAAS_READINESS_GAP.md](udoc-mvp/UDOC_SAAS_READINESS_GAP.md) | Not commercial SaaS; P0–P3 |
| [SUBMISSION_TIMELINE.md](udoc-mvp/SUBMISSION_TIMELINE.md) | Orientation to March 2027 |
| [CANON_FREEZE_NOTICE.md](udoc-mvp/CANON_FREEZE_NOTICE.md) | Do not expand Canon instead of smoke |

### Category 5 · Verification and evidence
*How to prove the live loop*

| Document | Relevance |
|----------|-----------|
| [CAPSTONE_EVIDENCE_PACK.md](udoc-mvp/CAPSTONE_EVIDENCE_PACK.md) | What counts as evidence |
| [UDOC_SMOKE_PASS.md](udoc-mvp/UDOC_SMOKE_PASS.md) | Minimum pass definition |
| [SMOKE_EVIDENCE_TEMPLATE.md](udoc-mvp/SMOKE_EVIDENCE_TEMPLATE.md) | Operator dated record |
| [P6_ASSESSOR_SIDE_BY_SIDE.md](udoc-mvp/P6_ASSESSOR_SIDE_BY_SIDE.md) | Demo vs live per surface |
| [TASK2_DEMO_PARITY_STATUS.md](udoc-mvp/TASK2_DEMO_PARITY_STATUS.md) | Task 2 status (close only after live green) |

### Category 6 · Demo and control mapping
*Netlify SoT → live control coverage*

| Document | Relevance |
|----------|-----------|
| [UDOC_DEMO_INVENTORY.md](udoc-mvp/UDOC_DEMO_INVENTORY.md) | Seven demo slugs |
| [UDOC_V93_DEMO67_PATENT_CONTROLS.md](udoc-mvp/UDOC_V93_DEMO67_PATENT_CONTROLS.md) | Demos 6–7 patent/control map |
| [PORTAL_LIVE_CORE.md](udoc-mvp/PORTAL_LIVE_CORE.md) | 24-portal dual-path behaviour |

### Category 7 · Historical session logs
*Build diary — not primary assessor path; archive relevance*

| Document | Relevance |
|----------|-----------|
| SESSION9 … SESSION14, SESSION_CITIZEN_PORTALS_1 | Incremental density / fidelity notes from build sessions |

**Assessor tip:** Prefer Categories 1–5. Use Category 6 for demo depth. Category 7 only if reconstructing how a surface evolved.

---

## Plane B — Engineering Canon (`docs/`)

Master index: [docs/ENGINEERING_CANON.md](docs/ENGINEERING_CANON.md)

| Vol | Folder | Category | Relevance |
|-----|--------|----------|-----------|
| **I** | `vol-1-ecosystem-canon/` | Constitution / philosophy | Vision, pillars, human primacy, GBS doctrine, security doctrine |
| **II** | `vol-2-system-architecture/` | System architecture | Engines (UDOC, GBS, intelligence, audit, franchise, SETHS, …) |
| **III** | `vol-3-repository-blueprint/` | Repository layout | Folders, frontend/mobile/desktop, naming |
| **IV** | `vol-4-intelligence-whitepaper/` | Intelligence / corpus | Institutional intelligence, multi-tenancy theory, data governance |
| **V** | `vol-5-gbs-constitutional-runtime/` + `vol-5-gbs-runtime/` | GBS / EVA runtime law | Deterministic engines, policy, EVA scoring, sovereignty FSM |
| **VI** | `vol-6-developer-implementation*` | Implementation history | Commit philosophy and sequenced commit guides |
| **VII** | `vol-7-database-design/` | Data model | Schema, UDOC/SETHS/MADIBA/TS tables, audit chain |
| **VIII** | `vol-8-api-reference/` | API law | Endpoint families by domain |
| **IX** | `vol-9-ui-ux-design*` | UI/UX design system | Design language, portals, accessibility |
| **X** | `vol-10-infrastructure/` | Infrastructure | Docker, HA, DR, **Ch 13 Render** (live Capstone honesty) |
| **XI** | `vol-11-roadmap/` | Long-horizon roadmap | Production path → expansion (aspirational; not Capstone bar) |

### Canon reader roles

| Role | Start volumes |
|------|----------------|
| Capstone assessor | Plane A first; then Vol IX tokens; Vol X Ch 13 |
| New contributor | Vol I → Vol III → Vol VI |
| Architect | Vol II → Vol V → Vol X |
| Data engineer | Vol VII → Vol VIII |
| Frontend | Vol IX → live package notes in Plane A |
| Security / governance | Vol I → Vol IV → Vol V |

---

## Relevance matrix (quick)

| Need | Go to |
|------|--------|
| What is this Capstone claiming? | Cover note · Limitations · SaaS gap |
| How is the system structured live? | Architecture map · Live environments |
| Staff vs client product? | EDR-002 · Package story · matrix |
| How do I verify live? | Smoke pass · P6 · Evidence template |
| Why these limits? | EDR-003 · EDR-004 · Roadmap |
| Full constitutional design | Canon Vol I–XI (frozen philosophy) |
| API / DB detail | Canon Vol VII–VIII |
| GIS/GBS product depth | Deferred after Task 2; Canon Vol V / IV for theory |

---

## Maintenance

- New **Capstone intent** docs → add under the correct Category 1–6 in this file and in `udoc-mvp/README.md`.  
- New **Canon** chapters → under the matching volume; do not use Canon expansion to replace smoke evidence.  
- Session logs stay Category 7 unless promoted into an EDR or limitation update.
