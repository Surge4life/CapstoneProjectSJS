# EDR-003 · Free-tier constraints are accepted design limits

**Status:** Accepted  
**Date:** 2026-07-31  
**Context:** CapstoneProjectSJS · Render free · Neon Postgres · March 2027

## Problem

Unlimited design ambition collides with fixed hosting quotas. Treating free-tier limits as temporary embarrassment leads to overclaim ("full SaaS", "unlimited registration", "new service per feature") and broken assessor trust when the live stack cannot match the claim.

## Decision

**Neon ≤500MB and Render free-tier service limits are first-class design constraints**, not afterthoughts.

| Constraint | Design consequence |
|------------|--------------------|
| Neon ≤ **500MB** | Demo seed only; no bulk new user registration for smoke; no large binary corpora in DB; prefer text/policy packs over file dumps |
| Render **~20 active services** | No new service for Citizen or 24-portals; fold into Client and Core `/portals` |
| Cold starts | Document wake behaviour; smoke may need retry; do not claim always-on SLA |
| Auto-deploy from `main` | Small reversible commits; freeze working modules |
| Pre-registration honesty | No live company/trademark legal claims in product chrome |

These limits **shape** the Capstone product story. A smaller, honest system is preferable to a larger system that cannot run as described.

## Alternatives considered

1. **Ignore limits and document ideal architecture only** — rejected (assessor grades live evidence).  
2. **Paid infra mid-Capstone as requirement** — rejected (not required for documented intent; optional later).  
3. **Mock all governance offline** — rejected (live EVA + BLOCK path is the honesty gate).

## Consequences

- Task 2 / smoke uses **existing** operator; registration is not part of the pass.  
- GIS file-corpus and commercial multi-tenant proof stay deferred or proven carefully without blowing storage.  
- Gap docs (`UDOC_SAAS_READINESS_GAP.md`) remain mandatory reading.  
- "Better code than the world" is irrelevant if the world is not bound by the same quotas; **intent under constraints** is the Capstone asset.

## Related

- `ENGINEERING_ROADMAP_CAPSTONE.md`  
- `UDOC_LIVE_ENVIRONMENTS.md`  
- `UDOC_SAAS_READINESS_GAP.md`  
- `EDR-001` · `EDR-002`  
