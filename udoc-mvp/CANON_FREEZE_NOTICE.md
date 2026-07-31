# Canon freeze notice · Engineering volumes

**Status:** Recommended freeze for Capstone philosophy  
**Date:** 2026-07-31  
**Location of Canon:** `docs/` (Volumes I–XI and related)

---

## Decision

Treat the existing Engineering Canon as **Canon v1.0 for Capstone purposes**: implement and demonstrate from it; do **not** expand philosophy volumes as a substitute for live verification or package honesty.

| Do | Do not |
|----|--------|
| Reference Canon when implementing | Rewrite Canon weekly to chase new ideas |
| Add an EDR when a *decision* changes | Add parallel “final system” essays |
| Fix contradictions that block smoke or assessors | Open ADR/domain/event catalogues unless implementation forces them |
| Keep `udoc-mvp/` intent spine current | Claim commercial completeness in Canon prose |

---

## Why freeze

External and internal reviews agree: documentation maturity is high; remaining Capstone risk is **operational honesty and scope control**, not missing manifesto text. Unfrozen Canon invites infinite redesign.

---

## Allowed updates during freeze

- Factual corrections (dead links, renamed hosts, wrong Neon claims)  
- Pointers from `udoc-mvp/` into Canon  
- New EDRs in `udoc-mvp/` for decisions that affect live Capstone code  
- Smoke evidence and limitations register updates  

## Disallowed without explicit re-open

- New “Volume XII: everything else” style expansion as Capstone critical path  
- GIS/GBS deep product Canon as blocker before Task 2 green  
- Replacing live hosts with paper-only redesigns  

---

## Related

- `ENGINEERING_ROADMAP_CAPSTONE.md`  
- `LIMITATIONS_REGISTER.md`  
- `UDOC_SAAS_READINESS_GAP.md`  
