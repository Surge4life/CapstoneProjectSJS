# Chapter 01 — Root Structure

## The Repository Root

The root of the G.O.D.S repository is a monorepo. Understanding what lives at the root and why is the first step to navigating the codebase.

---

## Root-Level Directories

```
gods-ecosystem/
├── platform-core/          Backend governance API (Python/FastAPI)
├── governance-engines/     EVA, GIS, UDOC, G.O.D.S engines
│
├── udoc-app/               UDOC Control — web PWA
├── udoc-mobile/            UDOC Control — Capacitor (Android/iOS)
├── udoc-desktop/           UDOC Control — desktop wrapper
│
├── seths-app/              SETHS — web PWA
├── seths-mobile/           SETHS — Capacitor
├── seths-desktop/          SETHS — desktop
│
├── madiba-app/             MADIBA — web PWA
├── madiba-mobile/          MADIBA — Capacitor
├── madiba-desktop/         MADIBA — desktop
│
├── ts-app/                 TS Industries — web PWA
├── ts-mobile/              TS Industries — Capacitor
├── ts-desktop/             TS Industries — desktop
│
├── platform-web/           G.O.D.S Admin Console (browser-only)
├── platform-internal/      Internal staff portal
├── portals-web/            Learner / Employer / Employee portals (web)
├── portals-mobile/         Portals — Capacitor
├── portals-desktop/        Portals — desktop
│
├── udoc-agent/             Host-side AI governance attachment
├── udoc-gateway/           Protocol bridge + mTLS relay
├── udoc-edge/              Autonomous offline governance node
├── udoc-sidecar/           Event buffer sidecar
├── udoc-internal/          UDOC internal operations interface
├── udoc-operator/          UDOC operator tools
├── udoc-public/            UDOC public-facing endpoints
├── udoc-station/           UDOC hardware station controller
├── udoc-portals/           UDOC portal components
├── udoc-sentinel/          UDOC monitoring agent
│
├── mobile-gateways/        Mobile gateway services
├── gods-mobile/            G.O.D.S shared mobile components
│
├── infra/                  Docker, Kubernetes, Terraform, monitoring
├── hw-bringup/             Hardware initialisation (boot, selftest, init)
│
├── branding/               Brand assets and entity constants
├── tools/                  Developer utilities
├── docs/                   Engineering Canon (this document)
│
├── smoke_test.py           End-to-end smoke test suite (31 paths)
├── render.yaml             Render cloud deployment configuration
├── replit.md               Project overview and user preferences
├── .gitignore              Root-level gitignore
└── 00_*.md                 Operational documentation files
```

---

## Root-Level Files Explained

### `smoke_test.py`

The end-to-end smoke test suite. Runs 31 test paths against a live deployment. Must pass 31/31 before any production deployment.

```bash
python smoke_test.py                                          # Test localhost:8000
python smoke_test.py --target https://gods.example.com       # Test any URL
python smoke_test.py --read-only                             # Skip write operations
```

### `render.yaml`

The Render cloud deployment configuration. Defines all services, their build commands, and environment variable references. See Volume X, Chapter 13.

### `replit.md`

Project overview, how to run, and user preferences. Updated whenever a significant project structure change is made.

### `00_*.md` Operational Files

Files prefixed `00_` are operational documentation generated during the initial build sprint. They document the build progress, architecture decisions, ecosystem status, and build notes. They are not part of the Engineering Canon (which lives in `docs/`) but provide additional operational context.

| File | Contents |
|------|---------|
| `00_APPS_OVERVIEW.md` | Applications summary |
| `00_ARCHITECTURE.md` | Architecture overview |
| `00_BUILD_APKS.md` | Android APK build instructions |
| `00_ECOSYSTEM_STATUS.md` | Current ecosystem status |
| `00_LIVE_BUILD_PROGRESS.md` | Build progress tracking |
| `00_NETWORK_TOPOLOGY.md` | Network topology diagram |
| `00_PROGRESS.md` | Detailed progress log |

---

## Root-Level Ownership

| Item | Owner | Notes |
|------|-------|-------|
| `render.yaml` | Infrastructure | Changes require senior review |
| `smoke_test.py` | All — collective | Tests must be updated with any API change |
| `docs/` | All — collective | Canon chapters are added as features are built |
| `replit.md` | Active developer | Updated per significant change |
| `00_*.md` | Historical | Do not modify — operational record |

---

## The Naming Pattern for Division Directories

All four division application directories follow the pattern `{division}-{type}`:

| Division | Web | Mobile | Desktop |
|----------|-----|--------|---------|
| UDOC | `udoc-app` | `udoc-mobile` | `udoc-desktop` |
| SETHS | `seths-app` | `seths-mobile` | `seths-desktop` |
| MADIBA | `madiba-app` | `madiba-mobile` | `madiba-desktop` |
| TS | `ts-app` | `ts-mobile` | `ts-desktop` |

The `platform-*` and `portals-*` directories follow the same pattern for the shared admin and portal interfaces.
