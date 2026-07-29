# UDOC Smoke-Pass Checklist — Capstone / Assessor

**Purpose:** Verify the live UDOC division is operational on Render + Neon without fabricating scale.  
**Constraint:** Neon free ≤500MB · no new human user registration required · prefer seeded `model-001`.  
**Date track:** 2026-07-29 · Task 2 client SaaS runtime path

---

## Surfaces under test

| Surface | URL |
|---------|-----|
| Platform Core | `https://gods-platform-core.onrender.com` |
| Sentinel (EVA + policy runtime) | `https://gods-platform-core.onrender.com/Sentinel` |
| Client console | `gods-udoc-client` host (`udoc-public`) |
| Citizen (public) | client host `/citizen.html` |
| Admin (internal UDOC) | `https://gods-platform-core.onrender.com/udoc-admin` |
| GODS constitutional admin | `https://gods-platform-core.onrender.com/admin` |

Use **existing** operator credentials only (bootstrap / platform admin). Do not create assessor user accounts on the free Neon instance.

---

## A · Core health (unauthenticated)

| # | Check | Pass |
|---|--------|------|
| A1 | `GET /health` | 200 |
| A2 | `GET /version` | JSON with service/commit |
| A3 | `GET /` surfaces list includes `sentinel` | present |

---

## B · Demo seed readiness (authenticated)

Sign in on Sentinel or Client with existing operator.

| # | Check | Pass |
|---|--------|------|
| B1 | `GET /udoc/demo/ready` → `ready: true` | model-001 + ACTIVE demo policy pack |
| B2 | `GET /policy/active` → `enforced_rules > 0` | demo pack live |
| B3 | `GET /registry/models` includes `model-001` | seeded |

If B1 fails: wait for Core redeploy after startup seed commit, or confirm Neon connectivity. **Fail-closed** is correct when the model is absent.

---

## C · Sentinel smoke button

On `/Sentinel` → header **Smoke**.

| # | Step | Pass |
|---|------|------|
| C1 | `/health` | PASS |
| C2 | `/udoc/demo/ready` | PASS |
| C3 | `/policy/active` rules > 0 | PASS |
| C4 | EVA fair on `model-001` | decision ≠ BLOCK |
| C5 | EVA biased | decision = **BLOCK** |

All five green = **runtime smoke-pass**.

---

## D · Client Govern scenarios (`udoc-public`)

| # | Chip | Expected |
|---|------|----------|
| D1 | Fair | Non-BLOCK path; composite EVA shown |
| D2 | Biased → BLOCK | BLOCK + reasons and/or policy findings |
| D3 | High-risk | `risk_tier: HIGH` applied; REVIEW/ESCALATE/BLOCK not pure silent APPROVE |
| D4 | Sovereignty | Sovereignty / block path from degraded signals |
| D5 | Certificate verify (if issued) | VALID on verify control |

Dashboard should show **demo boot posture READY** when B1 is true.

---

## E · Evidence / replay (optional depth)

| # | Check | Pass |
|---|--------|------|
| E1 | Decision row → Evidence | sealed bundle JSON |
| E2 | Replay | REPRODUCIBLE or explicit DRIFT |
| E3 | 12 Pillars tab | ENFORCED counts present |

---

## F · What is *not* required for this pass

- New human user registration or multi-tenant commercial onboarding  
- File uploads into GIS corpus (text path only under DB limits)  
- GODS GBS / SETHS / MADIBA / TS full product depth  
- New Render services beyond the existing blueprint  

---

## Honesty labels (must remain visible)

- Pre-registration entity posture  
- GG54477 withdrawn 26 Apr 2026  
- Standing basis: POPIA s71 + Constitution ss 9/16/33  
- Neon capacity / open-source upgrade path stated on Sentinel and Client footers  

---

## Pass statement

**UDOC division smoke-pass** when A + B + C are green and D2 (biased BLOCK) is observed on Client or Sentinel.  
That is the minimum credible live demonstration for assessor grading of the UDOC showcase path.
