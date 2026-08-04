# Capstone submission timeline · due **30 October 2027**

**Updated:** 2026-08-04  
**Previous target:** March 2027 (superseded)  
**New deadline:** **30 October 2027**  
**Constraint:** Free-tier Render + Neon ≤500MB · intent documented · no commercial SaaS claim required for grade

Runway from Aug 2026 → Oct 2027 ≈ **14–15 months**.  
**Immediate focus (next 8 weeks):** finish UDOC environments + close Task 2 smoke · then GBS/docs (Task 1) without new service sprawl.

---

## Phase map

| Phase | Window | Focus | Exit criteria |
|-------|--------|--------|----------------|
| **P0 Finish environments** | **Now → ~8 weeks** | Task 2 operator green; EVA multi-sector stable; policy upload UI; no extra Render services | Surfaces 1–5 biased=BLOCK; evidence screenshots |
| **P1 Evidence pack** | +2 months | Assessor walkthrough, smoke template filled, environment classification current | `CAPSTONE_EVIDENCE_PACK` usable by a stranger |
| **P2 GBS / Canon (Task 1)** | After P0 | Founder GBS V2 docs → selective routes; S.E.T.H.S / M.A.D.I.B.A / T.S. framing | Docs frozen; runtime only if quota allows |
| **P3 Hardening (optional)** | Mid 2027 | Identity/tenancy docs + minimal tests if claimed | Honest gap register |
| **P4 Submission freeze** | Sep–Oct 2027 | Claims match live; video; cover note | Limitations register current · no last-week features |

---

## Next 8 weeks (environment finish)

### Week 1–2 — Close Task 2
- Operator ticks: Sentinel · Client · Citizen · Admin · Sector (biased=BLOCK)
- File screenshots into smoke evidence template
- Admin Policy-to-Code upload → activate → runtime-matrix once

### Week 3–4 — Stability
- Permanent UI embeds (local git) if bootstrap flash still annoys
- Exercise multi-sector EVA (`sector`: PUBLIC/PRIVATE/HEALTH/FINANCE) once each
- Keep Neon lean; no bulk Drive ingest

### Week 5–6 — Package honesty
- Re-read `UDOC_LIVE_ENVIRONMENT_CLASSIFICATION` + gateway links
- Client vs Internal package story matches live hosts
- Freeze “what we claim” list for assessors

### Week 7–8 — Handoff to Task 1
- Only after Task 2 closed: start GBS V2 / Canon alignment docs
- No new Render services unless one existing host is replaced

---

## Explicit non-goals before submission

- Guaranteed commercial multi-tenant SaaS  
- Full GIS/GBS product depth on free Neon  
- Hardware field deployment  
- 24 separate portal services  
- LLM as governance controller  

---

## Weekly habit

1. Direction change → EDR/roadmap **before** large code.  
2. Smoke fails → fix that surface only.  
3. New subsystem → *which documented intent does this implement?*  

---

## Live checkpoint (2026-08-04)

- Core commit includes multi-sector EVA (`134ccce3`)  
- Batch gate fair≠BLOCK / biased=BLOCK **PASS**  
- Decision response includes `sector_eva`, `controllers`, `scales`  
