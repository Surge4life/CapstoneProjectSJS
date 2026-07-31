# UDOC Capstone · Limitations register

**Purpose:** Explicit list of known limits so assessors do not have to infer gaps from silence.  
**Date:** 2026-07-31  
**Stance:** Naming a limitation is integrity, not failure.

---

## Infrastructure

| Limitation | Effect | Mitigation / honesty |
|------------|--------|----------------------|
| Neon ≤500MB | Cannot treat DB as unbounded user/corpus store | Demo seed; no-registration smoke (`EDR-004`); gap doc |
| Render free tier | Cold starts; service count cap | Existing hosts only; document wake behaviour |
| No paid always-on SLA | Pilot SLAs not offered | Not claimed as commercial SaaS |
| External Neon (Render Postgres expired) | Dependency on Neon availability | Core config; DR still weak (gap doc) |

## Product / governance

| Limitation | Effect | Mitigation / honesty |
|------------|--------|----------------------|
| Task 2 not operator-closed | Live biased=BLOCK not yet filed as evidence | `SMOKE_EVIDENCE_TEMPLATE.md` |
| StayChain full product UI | Partial vs demos 6–7 | Patent control map documents gap |
| Multi-tenant isolation unproven | Fields exist; cross-tenant hard test not automated | P1 in `UDOC_SAAS_READINESS_GAP.md` |
| MFA / invite / recovery | Basic JWT only | Not pilot-ready; documented |
| GIS product depth | Engines/docs ≠ full intelligence product on free tier | Deferred after smoke (`EDR-001`) |
| GBS franchise runtime | Framework narrative, not full runtime | Deferred |
| Hardware appliance ops | Architecture > live node ops | Not Capstone software blocker |

## Documentation / process

| Limitation | Effect | Mitigation / honesty |
|------------|--------|----------------------|
| Solo developer | Review bandwidth limited | EDRs + freeze list reduce thrash |
| Demo pixel parity | Functional loop prioritised over pixel-identical Netlify HTML | P6 matrix is functional, not pixel SoT |
| Commercial outcome unknown | Not a grading claim | Cover note + gap doc |

---

## How to use

- Before claiming a feature “done,” check this register.  
- When a limitation is removed (e.g. smoke filed), update this file in the same change set as the evidence.  
- Do not delete limitations quietly — mark **Resolved** with date and pointer.
