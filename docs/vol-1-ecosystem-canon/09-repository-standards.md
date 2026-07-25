# Chapter 09 — Repository Standards

## How the G.O.D.S Repository Is Organised and Maintained

These standards apply to every contributor. They are not suggestions. A pull request that violates these standards is not merged.

---

## Monorepo Structure

The G.O.D.S codebase is a monorepo. All services, frontends, mobile builds, infrastructure, and documentation live in a single repository. This is a deliberate choice:

**Why a monorepo:**
- Atomic changes across service boundaries (change API and frontend in one commit)
- Single source of truth for version compatibility
- Unified CI/CD pipeline
- Easier cross-service refactoring

**The tradeoff:** The repository is large. Cloning is slower. This is an acceptable tradeoff for the governance and consistency benefits.

---

## Top-Level Directory Layout

```
/
├── platform-core/          # FastAPI backend — primary governance service
├── governance-engines/     # EVA, GIS, UDOC, G.O.D.S engines
├── udoc-app/               # UDOC Control PWA (web)
├── udoc-mobile/            # UDOC Control Capacitor (Android/iOS)
├── udoc-desktop/           # UDOC Control desktop wrapper
├── seths-app/              # SETHS PWA (web)
├── seths-mobile/           # SETHS Capacitor
├── seths-desktop/          # SETHS desktop
├── madiba-app/             # MADIBA PWA (web)
├── madiba-mobile/          # MADIBA Capacitor
├── madiba-desktop/         # MADIBA desktop
├── ts-app/                 # TS Industries PWA (web)
├── ts-mobile/              # TS Industries Capacitor
├── ts-desktop/             # TS Industries desktop
├── platform-web/           # G.O.D.S Admin Console (web)
├── platform-internal/      # Internal staff portal
├── portals-web/            # Student/Employer/Employee portals (web)
├── portals-mobile/         # Portals Capacitor
├── portals-desktop/        # Portals desktop
├── udoc-agent/             # Host-side AI governance attachment
├── udoc-gateway/           # Protocol bridge with mTLS
├── udoc-edge/              # Autonomous local governance node
├── udoc-sidecar/           # Event buffer for offline governance
├── udoc-internal/          # UDOC internal operations
├── udoc-operator/          # UDOC operator tools
├── udoc-public/            # UDOC public-facing service
├── udoc-station/           # UDOC hardware station
├── udoc-portals/           # UDOC portal components
├── udoc-sentinel/          # UDOC monitoring agent
├── udoc-edge/              # Edge governance
├── udoc-sidecar/           # Sidecar buffer
├── mobile-gateways/        # Mobile gateway services
├── gods-mobile/            # G.O.D.S mobile components
├── infra/                  # Docker, Kubernetes, Terraform
├── hw-bringup/             # Hardware initialisation
├── branding/               # Brand assets and entity constants
├── tools/                  # Developer utilities
├── docs/                   # This Engineering Canon
├── smoke_test.py           # End-to-end smoke test suite
├── render.yaml             # Render deployment configuration
└── 00_*.md                 # Project-level documentation (operational)
```

---

## File Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Python modules | `snake_case.py` | `audit_writer.py` |
| TypeScript files | `camelCase.ts` or `PascalCase.tsx` | `auditWriter.ts`, `AuditConsole.tsx` |
| Configuration | `kebab-case.yaml` or `snake_case.env` | `docker-compose.yaml` |
| Documentation | `UPPER_CASE.md` for operational docs | `README.md`, `ARCHITECTURE.md` |
| Documentation | `##-title.md` for canon chapters | `03-constitutional-pillars.md` |
| Database migrations | `YYYYMMDD_NNN_description.sql` | `20240315_001_add_oversight_cases.sql` |

---

## Branch Strategy

| Branch | Purpose | Protection |
|--------|---------|-----------|
| `main` | Production-ready code | Requires PR + CI pass + review |
| `develop` | Integration branch | Requires PR + CI pass |
| `feature/*` | Individual features | None — developer's branch |
| `hotfix/*` | Production emergency fixes | Requires expedited review |
| `release/vX.Y` | Release preparation | Requires senior review |

---

## Commit Standards

Every commit message must follow this format:

```
[SCOPE] ACTION: Short description (max 72 chars)

Optional longer description. Explain WHY, not what.
The what is evident from the diff.

Refs: #issue-number (if applicable)
```

See Volume VI Chapter 02 for the full commit standard including scope and action options.

---

## What Cannot Be Committed

1. **Secrets** — No API keys, passwords, JWT secrets, private keys, or credentials. Use environment variables.
2. **Compiled binaries** — No `.apk`, `.exe`, `.so` files. Build artifacts are produced by CI.
3. **Large binary files** — No video, large images, or model weights in the repository.
4. **Generated code** — No auto-generated files that can be recreated from source.
5. **Personal data** — No real user data, test data with real names/IDs, or PII of any kind.

A `.gitignore` file at each service level enforces these rules. The root `.gitignore` catches common cases.
