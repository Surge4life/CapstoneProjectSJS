# Chapter 11 — Commits 081–090: Production Readiness

## Overview

This batch completes the production hardening: security, performance, mobile/desktop builds, portal consolidation, and pre-production validation.

---

## Commit 081: `[CORE] SECURE: JWT token refresh, logout, and revocation`

**What:**
- Refresh token rotation (new refresh token on every refresh)
- Logout endpoint invalidates all tokens for the session
- Token revocation list in Redis (revoked tokens are rejected immediately)
- Refresh token family detection (compromised token detection)

---

## Commit 082: `[CORE] SECURE: Rate limiting and DDoS protection`

**What:**
- Per-endpoint rate limiting using Redis sliding window
- IP-based rate limiting for authentication endpoints (10 attempts/min, 1-hour lockout after 50)
- User-based rate limiting for governance requests (100/min sustained)
- Kubernetes NGINX ingress rate limiting as additional layer

---

## Commit 083: `[CORE] PERF: Governance path optimisation — < 50ms p95 target`

**What:**
- Connection pooling tuning (PgBouncer config, asyncpg pool settings)
- EVA scoring parallelised (all 6 dimensions computed concurrently)
- Policy cache pre-warming on startup
- Redis caching for immutable lookups (model registration status, PolicyPack)
- Benchmark results documented in `platform-core/PERFORMANCE.md`

---

## Commit 084: `[UI] ADD: Portals — learner, employer, employee web portal`

**What:** `portals-web/` complete implementation:
- Student portal: learner registration, opportunity search, application tracking
- Employer portal: verified employer dashboard, opportunity management
- Employee portal: post-hire tracking, compliance view
- Shared authentication and navigation between portals

---

## Commit 085: `[UI] ADD: Mobile builds — all division apps`

**What:** Capacitor configurations for all four division apps:
- `seths-mobile/` — capacitor.config.ts, Android/iOS targets
- `udoc-mobile/` — capacitor.config.ts
- `madiba-mobile/` — capacitor.config.ts
- `ts-mobile/` — capacitor.config.ts
- Push notification integration (Capacitor Push Notifications plugin)

---

## Commit 086: `[UI] ADD: Desktop builds — all division apps`

**What:** Electron configurations for all division apps:
- `seths-desktop/`, `udoc-desktop/`, `madiba-desktop/`, `ts-desktop/`
- Electron main process with contextBridge security
- Auto-update configuration (electron-updater)
- Code signing configuration (requires external keystore)
- Distribution targets: Windows NSIS, macOS DMG, Linux AppImage

---

## Commit 087: `[CORE] ADD: SETHS portal router — learner + employer views`

**What:** `platform-core/app/routers/portals_student.py` and `portals_employer.py`:
- Student portal-specific endpoints (formatted for portal UX)
- Employer portal-specific endpoints
- Portal authentication (separate from admin/operator auth)

---

## Commit 088: `[CORE] ADD: Privacy and data subject rights endpoints`

**What:**
- `GET /privacy/my-data` — download all data (POPIA Section 23)
- `POST /privacy/erasure-request` — submit erasure request
- `GET /privacy/erasure-status/{id}` — check erasure status
- `POST /privacy/consent-update` — update consent declarations
- Privacy notice endpoint: `GET /privacy/notice`

---

## Commit 089: `[CORE] ADD: System health, configuration, and maintenance endpoints`

**What:**
- `GET /health` — comprehensive health check (see Vol II Ch 19)
- `GET /system/config` — current system configuration (gods_admin only)
- `POST /system/policy-cache/refresh` — manual policy cache refresh
- `POST /system/audit-chain/verify` — trigger chain verification job
- `GET /system/metrics` — Prometheus metrics endpoint

---

## Commit 090: `[TEST] ADD: Security and penetration test suite`

**What:** `tests/test_security.py`:
- RBAC boundary tests: every role attempting every action it shouldn't have
- JWT manipulation tests (expired, invalid signature, wrong algorithm)
- Injection tests: SQL injection attempts in all string parameters
- Rate limiting tests: verify limits are enforced
- Audit trail completeness: verify every action creates an audit record
- Cross-tenant isolation: verify no cross-tenant data leakage

Also: `tests/test_governance_constitutional.py` — the 11 constitutional check tests (referenced in Volume V).
