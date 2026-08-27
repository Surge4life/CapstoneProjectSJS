# Volume VI — Developer Implementation Guide
## Every Commit. In Order.

> This volume is the step-by-step build guide. A developer who follows this guide from Commit 001 to the final commit will have built the complete G.O.D.S ecosystem **as specified**. Every commit is atomic, testable, and meaningful.

**Folder merge (2026-08-27):** chapters previously split under `docs/vol-6-developer-implementation/` now live here. Links below match **actual filenames**.

---

## Contents

| Chapter | Title | File |
|---------|-------|------|
| [01](01-environment-setup.md) | Environment Setup | `01-environment-setup.md` |
| [02](02-commit-philosophy.md) | Commit Philosophy & Standards | `02-commit-philosophy.md` |
| [03](03-commits-001-010.md) | Commits 001–010: Core Intelligence Foundation | `03-commits-001-010.md` |
| [04](04-commits-011-020.md) | Commits 011–020: Governance Runtime | `04-commits-011-020.md` |
| [05](05-commits-021-030-seths.md) | Commits 021–030: SETHS Division | `05-commits-021-030-seths.md` |
| [06](06-commits-031-040-madiba.md) | Commits 031–040: MADIBA Division | `06-commits-031-040-madiba.md` |
| [07](07-commits-041-050-ts.md) | Commits 041–050: TS Industries Division | `07-commits-041-050-ts.md` |
| [08](08-commits-051-060-udoc.md) | Commits 051–060: UDOC Control Division | `08-commits-051-060-udoc.md` |
| [09](09-commits-061-070-analytics.md) | Commits 061–070: Analytics & Reporting | `09-commits-061-070-analytics.md` |
| [10](10-commits-071-080-infra.md) | Commits 071–080: Infrastructure & Deployment | `10-commits-071-080-infra.md` |
| [11](11-commits-081-090-production.md) | Commits 081–090: Production Readiness | `11-commits-081-090-production.md` |
| [12](12-testing-strategy.md) | Testing Strategy | `12-testing-strategy.md` |
| [13](13-ci-cd-pipeline.md) | CI/CD Pipeline | `13-ci-cd-pipeline.md` |
| [14](14-commits-091-100-final.md) | Commits 091–100: Final / close-out | `14-commits-091-100-final.md` |

---

## Commit Naming Convention

```
[SCOPE] ACTION: Description

Scope options:
  CORE     — platform-core backend
  SETHS    — SETHS division
  MADIBA   — MADIBA division
  TS       — TS Industries division
  UDOC     — UDOC Control division
  INTEL    — G.O.D.S Intelligence
  GBS      — GBS Constitutional Runtime
  EDGE     — Edge components (agent/gateway/edge/sidecar)
  INFRA    — Infrastructure
  DB       — Database migrations
  UI       — Frontend changes
  TEST     — Tests only
  DOCS     — Documentation only

Action options:
  ADD      — New feature
  FIX      — Bug fix
  REFACTOR — Code restructure (no behaviour change)
  REMOVE   — Delete code
  MIGRATE  — Database migration
  CONFIG   — Configuration change
```

**Example:** `[CORE] ADD: EVA 6-dimensional risk scoring engine`
