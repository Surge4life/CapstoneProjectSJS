# Chapter 14 — Naming Conventions

## Why Naming Conventions Matter

Consistent naming reduces cognitive load. When every developer uses the same patterns, names communicate intent without requiring comments. When naming is inconsistent, developers waste time deciphering what a name means rather than understanding what the code does.

These conventions are mandatory. Code review should flag naming convention violations just as it flags logic errors.

---

## Python Naming (platform-core, governance-engines/eva, governance-engines/udoc)

| Element | Convention | Examples |
|---------|-----------|---------|
| Modules / files | `snake_case.py` | `audit_writer.py`, `gbs_engine.py` |
| Classes | `PascalCase` | `DecisionRecord`, `AuditRef` |
| Functions | `snake_case` | `get_current_user()`, `write_audit_record()` |
| Variables | `snake_case` | `decision_record`, `current_user` |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT_MS`, `MAX_RETRIES` |
| Type aliases | `PascalCase` | `DecisionOutcome`, `JurisdictionCode` |
| Pydantic models | `PascalCase` with suffix | `DecisionRequest`, `DecisionResponse` |
| FastAPI routers | `snake_case` noun | `router = APIRouter(prefix="/decisions")` |
| Database models | `PascalCase` | `class Decision(Base)` |
| Async functions | Same as regular — no `async_` prefix | `async def get_decision(...)` |

### Router File Naming

Router files are named after the resource they serve:
```
auth.py          → /auth/*
decisions.py     → /decisions/*
registry.py      → /registry/*
oversight.py     → /oversight/*
```

### Service File Naming

Service files are named after what they do:
```
audit_writer.py         → writes to audit chain
governance_bridge.py    → bridges to governance engines
document_store.py       → stores/retrieves documents
gbs_engine.py           → runs GBS evaluation
```

---

## TypeScript/React Naming (frontend apps)

| Element | Convention | Examples |
|---------|-----------|---------|
| Files (components) | `PascalCase.tsx` | `DecisionCard.tsx`, `OversightCase.tsx` |
| Files (hooks) | `camelCase.ts` with `use` prefix | `useDecisions.ts`, `useAuth.ts` |
| Files (utilities) | `camelCase.ts` | `formatDate.ts`, `hashUtils.ts` |
| Files (API) | `api.ts` (one per app) | `api.ts` |
| Files (types) | `types.ts` or `{domain}.types.ts` | `types.ts`, `governance.types.ts` |
| Components | `PascalCase` | `function DecisionCard(...)` |
| Props interfaces | `{Component}Props` | `interface DecisionCardProps` |
| Hooks | `use{Description}` | `useDecisions()`, `useCurrentUser()` |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_PAGE_SIZE`, `API_VERSION` |
| Variables / functions | `camelCase` | `decisionRecord`, `formatOutcome()` |
| CSS classes | `kebab-case` | `decision-card`, `outcome-badge` |

---

## Database Naming (PostgreSQL)

| Element | Convention | Examples |
|---------|-----------|---------|
| Schemas | `snake_case` | `iam`, `governance`, `seths` |
| Tables | `snake_case`, plural noun | `decisions`, `oversight_cases`, `learners` |
| Columns | `snake_case` | `created_at`, `model_id`, `eva_fa_score` |
| Indexes | `{table}_{columns}_idx` | `decisions_model_idx`, `learners_nqf_level_idx` |
| Primary keys | Always `id` | `id UUID PRIMARY KEY` |
| Foreign keys | `{referenced_table_singular}_id` | `model_id`, `tenant_id`, `audit_ref_id` |
| Audit columns | `created_at`, `updated_at`, `deleted_at`, `created_by`, `updated_by`, `deleted_by` |
| Boolean flags | `is_` or `has_` prefix, or descriptive adjective | `is_system_role`, `has_third_party_audit`, `elevated_scrutiny` |

---

## API Endpoint Naming

All API endpoints use `kebab-case` plural nouns for resources:

```
GET    /decisions                    — list decisions
GET    /decisions/{id}               — get one decision
POST   /decisions                    — create / submit
PATCH  /decisions/{id}               — update
DELETE /decisions/{id}               — soft delete

POST   /registry/models/{id}/suspend — action on a resource
POST   /registry/models/{id}/certify — action on a resource
```

Actions on resources use the pattern `/{resource}/{id}/{action}` — never verbs in the resource name itself (`/suspendModel` is wrong; `/models/{id}/suspend` is correct).

---

## Git Branch Naming

```
feature/{short-description}     — New features
fix/{short-description}         — Bug fixes
hotfix/{short-description}      — Production emergency fixes
release/v{major}.{minor}        — Release preparation branches
docs/{short-description}        — Documentation-only changes
```

Examples:
```
feature/seths-document-integrity
fix/governance-latency-p95
hotfix/auth-token-revocation
release/v2.1
docs/vol-7-madiba-tables
```

---

## Commit Message Naming

See Volume VI, Chapter 02 for the full commit message standard. Quick reference:

```
[SCOPE] ACTION: Description (max 72 chars total)

Scopes: CORE SETHS MADIBA TS UDOC INTEL GBS EDGE INFRA DB UI TEST DOCS
Actions: ADD FIX REFACTOR REMOVE MIGRATE CONFIG

[CORE] ADD: EVA 6-dimensional risk scoring engine
[SETHS] FIX: Document integrity check on PDF uploads
[DB] MIGRATE: Add oversight_cases table
[DOCS] ADD: Vol VII Chapter 05 - MADIBA tables
```
