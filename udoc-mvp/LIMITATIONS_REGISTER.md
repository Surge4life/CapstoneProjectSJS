# UDOC Capstone · Limitations register

**Purpose:** Explicit list of known limits so assessors do not have to infer gaps from silence.  
**Updated:** 2026-08-14  
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
| Operator UI evidence not yet signed | API gates green; formal Task 2 close needs operator hard-refresh tick on Client + Sentinel | `SMOKE_EVIDENCE_TEMPLATE.md` (API pre-filled 2026-08-13/14) |
| StayChain full product UI | Partial vs demos 6–7 | Patent control map documents gap |
| Multi-tenant isolation unproven | Fields exist; cross-tenant hard test not automated | P1 in `UDOC_SAAS_READINESS_GAP.md` |
| MFA / invite / recovery | Basic JWT only | Not pilot-ready; documented |
| GIS product depth | Engines/docs ≠ full intelligence product on free tier | Deferred after smoke (`EDR-001`) |
| GBS franchise runtime | Framework narrative + live `/gbs` page; not full franchise ops | Capstone freeze = designed_not_built for Sovereign-Verified |
| Hardware appliance ops | Architecture > live node ops | Not Capstone software blocker |
| Capital / MADIBA scale | Ledger metrics only | **≠ AUM** · capital **not_deployed** |

## Documentation / process

| Limitation | Effect | Mitigation / honesty |
|------------|--------|----------------------|
| Solo developer | Review bandwidth limited | EDRs + freeze list reduce thrash |
| Demo pixel parity | Functional loop prioritised over pixel-identical Netlify HTML | P6 matrix is functional, not pixel SoT |
| Netlify Holdings paste | Public site still pending §7 honesty paste | Website last · `LIVE_SITE_CORRECTION_PACK.md` |
| Commercial outcome unknown | Not a grading claim | Cover note + gap doc |

---

## Resolved (do not re-open without evidence)

| Item | Resolved | Pointer |
|------|----------|---------|
| Login density residual (operator + admin surfaces) | 2026-08-13 | `DIVISION_SURFACE_DENSITY_PLAN.md` · 4-role fillLogin |
| Core EVA gate fair≠BLOCK / biased=BLOCK (API) | 2026-08-13 · 2026-08-14 | `/decisions/batch` + `/udoc/demo/ready` auto-heal |
| Division operator loop SETHS→TS→MADIBA | 2026-08 | live Core surfaces |

---

## How to use

- Before claiming a feature “done,” check this register.  
- When a limitation is removed (e.g. smoke filed), update this file in the same change set as the evidence.  
- Do not delete limitations quietly — mark **Resolved** with date and pointer.
