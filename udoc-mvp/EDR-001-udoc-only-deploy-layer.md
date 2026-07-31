# EDR-001 · UDOC is the only customer-deployed layer

**Status:** Accepted  
**Date:** 2026-07-31  
**Context:** CapstoneProjectSJS · Render free · Neon ≤500MB · March 2027 submission

## Problem

The ecosystem names many layers (G.O.D.S, GBS, GIS, EVA, UDOC, portals, Sentinel, Intelligence). Without a written boundary, every layer competes to become “the product,” which explodes scope, services, and database use under free-tier limits.

## Decision

**Only UDOC is deployed as the operational product surface to users in this Capstone environment.**

- **G.O.D.S** — constitutional / holdings authority (intent and governance posture).  
- **GBS** — constitutional framework for franchises / divisions (documented, not a separate free-tier SaaS).  
- **GIS** — deterministic intelligence; engines and approved access paths are **controlled by UDOC**, not a parallel public product in this phase.  
- **EVA** — evaluation and coordination **inside** UDOC runtime (e.g. `/Sentinel`, Govern, policy-to-code).  
- **UDOC** — Client package, Internal package, Citizen, Gateway, and Core API routes that operators and tenants actually open.

Country or sector difference is achieved by **corpus, policy packs, and configuration**, not by rewriting UDOC per jurisdiction.

## Alternatives considered

1. **Ship every named system as its own Render service** — rejected (quota, Neon size, assessor confusion).  
2. **Defer all UI until full GIS/GBS product** — rejected (Capstone needs a demonstrable operational loop now).  
3. **Merge everything into one mega-HTML** — rejected (Internal vs Client package story is required for role honesty).

## Consequences

- New work must map to **Internal** or **Client** (or public Citizen), not invent a third commercial product line without docs.  
- GIS/GBS depth is **scheduled after** live UDOC smoke honesty (Task 2 / M7).  
- Documentation of intent (roadmap, package story, gap list) outranks speculative commercial completeness.  
- Free-tier constraints remain binding; “better code than the world” is not the success metric — **known intention** is.

## Related

- `ENGINEERING_ROADMAP_CAPSTONE.md`  
- `CAPSTONE_PACKAGE_STORY.md`  
- `UDOC_SAAS_READINESS_GAP.md`  
