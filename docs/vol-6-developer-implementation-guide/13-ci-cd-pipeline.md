# Chapter 13 — CI/CD Pipeline

## The Continuous Integration Philosophy

The CI/CD pipeline is not an afterthought. It is the mechanism by which the constitutional requirements are enforced automatically — every merge to `main` must pass the full suite of tests, including the constitutional checks. No human can override this without pipeline access, which is restricted to `gods_admin` equivalents.

---

## Pipeline Architecture

```
Developer PR
    ↓
GitHub Actions: PR Check
    ├── Lint (ruff, mypy, eslint)
    ├── Unit tests (all services)
    ├── Constitutional tests [BLOCKING]
    ├── Integration tests
    ├── Security tests
    └── Status: PASS → PR can be merged
              FAIL → PR blocked

Merge to main
    ↓
GitHub Actions: Deploy Pipeline
    ├── All tests (re-run to confirm)
    ├── Build container images
    ├── Push to container registry
    ├── Deploy to staging (Render staging service)
    ├── Smoke tests against staging [BLOCKING]
    └── Status: PASS → auto-deploy to production
              FAIL → stop, alert, manual investigation
```

---

## `ci.yml` — PR Check Workflow

```yaml
name: PR Check
on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Python lint
        run: |
          pip install ruff mypy
          ruff check platform-core/ governance-engines/
          mypy platform-core/app/

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_DB: gods_test, POSTGRES_PASSWORD: test }
      redis:
        image: redis:7-alpine
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: pip install -r platform-core/requirements.txt
      - name: Run tests
        run: python -m pytest tests/ -v --tb=short
        env:
          DATABASE_URL: postgresql://postgres:test@localhost/gods_test
          REDIS_URL: redis://localhost:6379
          ENVIRONMENT: test

  constitutional-tests:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Run constitutional checks
        run: python -m pytest tests/test_constitutional_checks.py -v --tb=long
        # Failure here triggers a blocking check — never auto-skippable
```

---

## `deploy-render.yml` — Production Deploy Workflow

```yaml
name: Deploy to Render
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run full test suite
        run: python -m pytest tests/ -v

      - name: Deploy backend to Render
        run: |
          curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
            -H "Authorization: Bearer $RENDER_API_KEY"
        env:
          RENDER_SERVICE_ID: ${{ secrets.RENDER_SERVICE_ID }}
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}

      - name: Wait for deployment
        run: |
          sleep 90
          curl --retry 5 --retry-delay 15 \
            https://gods-platform-core.onrender.com/health

      - name: Run smoke tests
        run: python smoke_test.py --target https://gods-platform-core.onrender.com
```

---

## `security-scan.yml` — Weekly Security Scan

```yaml
name: Weekly Security Scan
on:
  schedule:
    - cron: '0 2 * * 0'  # Every Sunday at 02:00 UTC

jobs:
  dependency-audit:
    steps:
      - name: Python dependency audit
        run: pip-audit --requirement platform-core/requirements.txt

  sast-scan:
    steps:
      - name: Bandit SAST scan
        run: bandit -r platform-core/app/ -f json -o bandit-results.json
      - name: Upload results
        uses: actions/upload-artifact@v4
        with: { name: sast-results, path: bandit-results.json }
```

Security scan results are uploaded as CI artifacts and reviewed by the designated security reviewer monthly.

---

## Environment Management

| Environment | Branch | Auto-Deploy | Smoke Tests |
|-------------|--------|------------|------------|
| Development | Feature branches | No | No |
| Staging | `develop` | Yes (on merge) | Yes (after deploy) |
| Production | `main` | Yes (after staging passes) | Yes (after deploy) |

**Production deploy gate:** Production deploys are gated on staging smoke tests passing. This means the deploy sequence is always: deploy to staging → smoke test staging → deploy to production. There is no mechanism to deploy directly to production without staging first.

---

## Deployment Notifications

Deployment events are published to the `#gods-deployments` Slack channel:
- Deployment started
- Deployment succeeded (with git SHA and commit message)
- Deployment failed (with error and link to CI logs)
- Smoke test failure (with which tests failed)
