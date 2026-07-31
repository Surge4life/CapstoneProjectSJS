# EDR-004 · Demo seed and no-registration smoke policy

**Status:** Accepted  
**Date:** 2026-07-31  
**Context:** CapstoneProjectSJS · Neon ≤500MB · Task 2 live verification

## Problem

A Capstone smoke path that requires creating many new users or models will exhaust free Neon storage and obscure whether governance (EVA + policy) works. Assessors need a **repeatable** path that does not depend on registration growth.

## Decision

**Smoke and Capstone demonstration use a fixed demo seed and the existing operator account only.**

| Element | Policy |
|---------|--------|
| **Operator** | Existing seed user (e.g. `admin@gods.local`) — no new user required to pass smoke |
| **Model** | `model-001` (or documented demo model) present at boot / seed |
| **Policy** | ACTIVE demo pack (e.g. POPIA + fairness rules) so biased path can **BLOCK** |
| **Ready probe** | `GET /udoc/demo/ready` asserts seed presence |
| **Citizen** | Public challenge/status without login; cases may write OversightCase rows sparingly |
| **Registration** | Optional for product demos; **not** part of Task 2 pass criteria |

Fail-closed behaviour when seed is missing is preferred over silent mock scores.

## Alternatives considered

1. **Smoke creates fresh users/models every run** — rejected (Neon growth, non-repeatable).  
2. **Fully offline mock UI** — rejected (does not prove live policy_enforced / BLOCK).  
3. **Paid DB required before any smoke** — rejected (Capstone must demonstrate under stated free-tier limits).

## Consequences

- `UDOC_SMOKE_PASS.md` and `SMOKE_EVIDENCE_TEMPLATE.md` forbid “must register first.”  
- Docs and UI may say pre-registration / forecast; they must not imply unlimited onboarding on free Neon.  
- Future multi-tenant isolation tests may use minimal extra rows only when isolation is the explicit goal (P1 in gap doc), not for everyday smoke.

## Related

- `EDR-003-free-tier-constraints.md`  
- `UDOC_SMOKE_PASS.md`  
- `ENGINEERING_ROADMAP_CAPSTONE.md`  
