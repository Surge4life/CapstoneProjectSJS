# Chapter 02 — Commit Philosophy

## Why Commit Standards Matter

A commit is more than a save point. It is a historical record of intent. When you read a commit message six months from now, you should be able to understand why that change was made — not just what changed. When a compliance officer reviews a change to the governance engine, the commit message is part of the audit trail.

The G.O.D.S commit standard is strict because the codebase is constitutional infrastructure. Vague commits like "fix stuff" or "update" are unacceptable in this repository.

---

## The Commit Format

```
[SCOPE] ACTION: Short description (max 72 chars total)

Optional body: why the change was made, what tradeoff was accepted,
what the alternatives were. Reference to relevant architecture decision.
Max 100 chars per line.

Refs: #issue-number (if applicable)
```

---

## Scope Codes

| Scope | What It Covers |
|-------|---------------|
| `CORE` | `platform-core/` — backend API, services, models |
| `SETHS` | SETHS division code (any layer) |
| `MADIBA` | MADIBA division code |
| `TS` | TS Industries code |
| `UDOC` | UDOC components, edge, gateway |
| `INTEL` | Intelligence system (corpus, retrieval, synthesis) |
| `GBS` | Governance engines, GBS runtime |
| `EDGE` | Edge node, sidecar, hardware code |
| `INFRA` | `infra/` — Docker, K8s, CI/CD, monitoring |
| `DB` | Database migrations, schema changes |
| `UI` | Any frontend (`*-app/`, `*-web/`, `portals-*`) |
| `TEST` | Test code only (no production code change) |
| `DOCS` | Documentation only (no code change) |

---

## Action Words

| Action | When to Use |
|--------|------------|
| `ADD` | New functionality added (endpoint, feature, component) |
| `FIX` | Bug fix |
| `REFACTOR` | Internal restructure, no behaviour change |
| `REMOVE` | Code, files, or dependencies removed |
| `MIGRATE` | Database migration |
| `CONFIG` | Configuration change (not a code change) |
| `SECURE` | Security-specific fix (treated as high-priority in review) |
| `PERF` | Performance improvement |
| `TEST` | Adding or updating tests |
| `DOCS` | Documentation change |

---

## Good vs Bad Commits

**Bad:**
```
fix bug
update seths
changes
wip
temp fix, will clean up later
```

**Good:**
```
[SETHS] FIX: Document integrity check fails on PDFs with binary streams

SHA-256 was computed on the raw upload bytes, but PDF binary streams
were being normalised by the upload middleware before the hash.
Now hash computed before middleware processes the file.

[GBS] ADD: Hard block threshold for SC < 30 (sovereignty floor)

EVA sovereignty scores below 30 indicate severe jurisdiction compliance
risk. Added constitutional check - cannot be lowered by PolicyPack.
Tests: tests/test_constitutional_checks.py::test_sc_below_30_always_blocks

[DB] MIGRATE: Add oversight_cases table with SLA enforcement

Adds seths.oversight_cases with SLA deadline, reviewer assignment,
and indexed columns for the oversight queue dashboard.
Migration: 003_add_oversight_cases.sql
```

---

## Commits on the Governance Critical Path

Any commit that modifies the governance critical path (`gbs_engine.py`, `audit_writer.py`, `eva/`, `udoc/`) must include:

1. **What changed** — which behaviour was modified
2. **Why** — the governance rationale
3. **Test coverage** — which test(s) verify the behaviour

Governance critical path commits that fail CI (any test failure) must not be merged. This is a hard rule in the CI configuration.

---

## The Semantic Commit Rule

Each commit should be **semantically complete** — it should make the codebase better in some specific, describable way. A commit should not:
- Leave the tests failing
- Leave an import that doesn't resolve
- Mix unrelated changes (formatting refactor + logic change)
- Be a work-in-progress state

If you are mid-change, use a draft PR and squash before merging. The main branch history should read as a coherent sequence of completed improvements.

---

## Atomic Migrations

Every database migration is a single commit, separate from any application code changes that depend on it. The migration commit comes first. This enforces:

1. Migration → Review → Merge → Deploy
2. Application code that uses the new schema follows in a separate commit

This sequence ensures zero-downtime deployment: the schema change is live before the code that depends on it.
