# Chapter 04 — CI/CD Infrastructure

## Continuous Integration and Delivery

The CI/CD infrastructure automates the path from code commit to production deployment while enforcing quality and governance standards at every stage.

---

## Pipeline Overview

```
Developer pushes to feature branch
        ↓
GitHub Actions: PR Check (runs on every push to feature branch)
  ├── Python lint (ruff) + type check (mypy)
  ├── TypeScript lint (eslint) + type check (tsc)
  ├── Unit tests (all services)
  ├── Constitutional tests [BLOCKING]
  ├── Integration tests (Docker Compose services)
  ├── Security tests (RBAC, injection, isolation)
  └── Status checks enforced — PR cannot merge without pass

Developer merges to main
        ↓
GitHub Actions: Deploy Pipeline
  ├── Full test suite (re-run)
  ├── Build Docker images
  ├── Push to container registry
  ├── Deploy to staging environment
  ├── Smoke tests against staging [BLOCKING]
  └── Deploy to production (auto, after staging pass)
        ↓
GitHub Actions: Post-Deploy Verification
  ├── Smoke tests against production
  ├── Health check verification
  └── Slack notification (success or failure)
```

---

## GitHub Actions Configuration

All CI/CD configuration lives in `infra/ci/github-actions/`. Key files:

### `ci.yml` — PR Check

Runs on: every `push` to any branch, every `pull_request`

Key jobs:
- `lint` — ruff, mypy, eslint, tsc (parallel)
- `unit-tests` — pytest unit tests with PostgreSQL + Redis service containers
- `constitutional-tests` — 11 constitutional check tests (blocks all downstream on failure)
- `integration-tests` — full integration tests with all service containers
- `security-tests` — RBAC boundary tests, injection tests, cross-tenant isolation

Required status checks on `main` branch:
- All jobs in `ci.yml` must pass
- No bypass permitted (even for repository owners)

### `deploy-render.yml` — Render Deploy

Runs on: push to `main` (only after `ci.yml` passes)

Process:
1. Trigger Render deploy via Render API
2. Poll deploy status until complete or timeout (10 minutes)
3. Run smoke tests against newly deployed instance
4. On smoke test failure: trigger Render rollback automatically
5. Notify Slack of success or failure

### `security-scan.yml` — Weekly Security

Runs on: schedule (Sundays 02:00 UTC), manual trigger

- `pip-audit` — Python dependency vulnerability scan
- `npm audit` — Node.js dependency vulnerability scan
- `bandit` — Python SAST scan
- Results uploaded as CI artifacts + Slack notification if critical findings

---

## Container Registry

Docker images are pushed to the configured container registry (GitHub Container Registry for open-source, private ECR/GCR for enterprise deployments).

Image tagging strategy:
```
gods-platform-core:latest          ← latest main branch build
gods-platform-core:v2.1.0          ← semantic version tag
gods-platform-core:sha-abc123def   ← git SHA (for precise rollback)
```

Images are built with multi-stage Dockerfiles to minimise final image size:
- Builder stage: full Python/Node environment, installs dependencies
- Final stage: minimal runtime, copies built artifacts only
- Result: platform-core image ~250MB (vs ~1.2GB without multi-stage)

---

## Branch Protection Rules

`main` branch:
- Require pull request reviews: 1 approver minimum
- Require status checks: all CI jobs must pass
- Require branches to be up to date before merging
- No force pushes
- No direct commits (all changes via PR)

`develop` branch (staging target):
- Require status checks: CI must pass
- Direct commits permitted for small fixes

---

## Environment Promotion

```
Feature branch → main → Production (Render / Kubernetes)
                      → Staging (auto-deployed on push to main)
```

Every push to `main`:
1. Deploys to staging automatically
2. Runs smoke tests against staging
3. If staging passes: deploys to production automatically
4. If staging fails: production not updated, alert sent

This means production is always at most one staging cycle behind `main`.
