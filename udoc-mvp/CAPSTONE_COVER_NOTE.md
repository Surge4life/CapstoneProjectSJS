# Capstone cover note · UDOC under G.O.D.S ecosystem constraints

**Project:** CapstoneProjectSJS  
**Product focus:** UDOC (operational governance platform)  
**Environment:** GitHub → Render auto-deploy · Neon Postgres ≤500MB  
**Horizon:** Submission March 2027  
**Date of this note:** 2026-07-31

---

## What this Capstone is

A **documented, live, constrained** implementation of UDOC as the operational layer of a broader constitutional stack (G.O.D.S → GBS → GIS → EVA → UDOC). The live system demonstrates a governance loop: register/context → policy-aware EVA decision → fail-closed bias handling → audit/cert path → public citizen challenge path — on free-tier infrastructure.

## What this Capstone is not

- A claim of commercial SaaS readiness or guaranteed market success  
- A claim of full hardware appliance operations  
- A claim that every named ecosystem brand (GIS product depth, GBS franchise runtime) is fully productised on free Neon  
- A competition with unconstrained global codebases on novelty alone

**Success criterion:** known intention, honest limits, verifiable live behaviour, and package boundaries an assessor can follow in writing.

## How to read the work

1. `ASSESSOR_READING_ORDER.md` (15- and 45-minute paths)  
2. `ARCHITECTURE_MAP.md` + EDRs 001–004  
3. `CAPSTONE_EVIDENCE_PACK.md`  
4. Live smoke via `UDOC_SMOKE_PASS.md` and a filled `SMOKE_EVIDENCE_TEMPLATE.md`  
5. Engineering Canon under `docs/` for long-form design law

## Constraints that shaped the design

| Constraint | Effect |
|------------|--------|
| Neon ≤500MB | Demo seed; no registration required for smoke |
| Render service quota | Citizen and 24-portals folded into existing hosts |
| Solo Capstone timeline | Freeze working modules; expand only against written phases |

## Packages

- **Internal** — staff Admin / Sentinel / Portals / constitutional `/admin`  
- **Client** — tenant Models · Policy · Reports · Govern · App/Mobile  
- **Citizen** — public rights and challenge  
- **Gateway** — role → package routing  

## Integrity statement

Where the live system is incomplete relative to Netlify demos or whitepapers, the gap is **documented** (`UDOC_SAAS_READINESS_GAP.md`, Task 2 status, patent control map). Overclaim is treated as a defect.

---

*Intent first. Code second. Limits written down.*
