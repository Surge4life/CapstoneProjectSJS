# UDOC Smoke-Pass Checklist — Capstone / Assessor

**Purpose:** Verify the live UDOC division is operational on Render + Neon without fabricating scale.  
**Constraint:** Neon free ≤500MB · no new human user registration required · prefer seeded `model-001`.  
**Date track:** 2026-07-30 · Task 2 density wave  
**Side-by-side matrix:** `udoc-mvp/P6_ASSESSOR_SIDE_BY_SIDE.md`

---

## Surfaces under test

| Surface | URL |
|---------|-----|
| Platform Core | `https://gods-platform-core.onrender.com` |
| Sentinel (EVA + policy runtime) | `https://gods-platform-core.onrender.com/Sentinel` |
| 24 Portals | `https://gods-platform-core.onrender.com/portals` |
| Client console | `https://gods-udoc-client.onrender.com` |
| Citizen (public) | `https://gods-udoc-client.onrender.com/citizen.html` |
| Client SaaS portals | `https://gods-udoc-portals.onrender.com` |
| Admin (internal UDOC) | `https://gods-udoc-admin.onrender.com` |
| Sector | Sector host (gods-udoc-sector) |
| GODS constitutional admin | `https://gods-platform-core.onrender.com/admin` |
| Gateway | `https://gods-udoc-gateway.onrender.com` |

Use **existing** operator credentials only. Do not create assessor user accounts on free Neon.

---

## A · Core health (unauthenticated)

| # | Check | Pass |
|---|--------|------|
| A1 | `GET /health` | 200 |
| A2 | `GET /citizen/health` | `surface: citizen` |
| A3 | `GET /udoc/demo/ready` (may need auth) | seed status |

---

## B · Demo seed readiness (authenticated)

| # | Check | Pass |
|---|--------|------|
| B1 | `GET /udoc/demo/ready` → `ready: true` | model-001 + ACTIVE pack |
| B2 | `GET /policy/active` → `enforced_rules > 0` | demo pack live |
| B3 | `GET /registry/models` includes `model-001` | seeded |

---

## C · Sentinel smoke + Full EVA matrix

On `/Sentinel` → header **Smoke** and **EVA Command → Run Full EVA matrix**.

| # | Step | Pass |
|---|------|------|
| C1 | `/health` | PASS |
| C2 | `/udoc/demo/ready` | PASS |
| C3 | `/policy/active` rules > 0 | PASS |
| C4 | EVA fair on `model-001` | decision ≠ BLOCK |
| C5 | EVA biased | decision = **BLOCK** |
| C6 | Full EVA matrix | biased row **BLOCK** + KPIs |

---

## C2 · Client dashboard mini-smoke + Govern batch

On Client → Dashboard → **Run client smoke** · Govern → **Run Full EVA batch**.

| # | Step | Pass |
|---|------|------|
| C2.1 | `/health` | PASS |
| C2.2 | `/udoc/demo/ready` | PASS |
| C2.3 | EVA fair | ≠ BLOCK |
| C2.4 | EVA biased | = **BLOCK** |
| C2.5 | Full EVA batch | outcome KPIs populated |

---

## D · Client Govern scenarios

| # | Chip | Expected |
|---|------|----------|
| D1 | Fair | Non-BLOCK; composite EVA |
| D2 | Biased → BLOCK | **BLOCK** + terminal |
| D3 | High-risk | risk path not silent APPROVE |
| D4 | Sovereignty | degraded signals path |
| D5 | Client smoke 4/4 | same asserts as C2 |

---

## E · Citizen (public, no login)

| # | Check | Pass |
|---|--------|------|
| E1 | Open `/citizen.html` | rights banner |
| E2 | Submit challenge | `case_ref` from Core |
| E3 | Check case status | timeline from Neon |
| E4 | Core pill | citizen live / online |

---

## F · Admin (hard-refresh ×2 for SW **v4**)

| # | Check | Pass |
|---|--------|------|
| F1 | Command Centre DEMO READY + outcome strip | after login |
| F2 | EVA Command chips + **Full EVA batch** | Biased BLOCK |
| F3 | HITL → Portals link | opens `/portals` |
| F4 | Infra links | Sentinel / Health / Jobs / Portals / Citizen |

---

## H · Sector

| # | Check | Pass |
|---|--------|------|
| H1 | Overview DEMO READY + BLOCK/APPROVE KPIs | visible |
| H2 | Decisions Full EVA batch | Biased BLOCK |
| H3 | Switch PUBLIC/PRIVATE | profile reload |

---

## I · 24 Portals dual-path

| # | Check | Pass |
|---|--------|------|
| I1 | Open HITL / Border control | `live → case_ref` |
| I2 | Resolve with Target=`COB-…` | RESOLVED/OVERRIDDEN |
| I3 | CITIZEN card | full AI-Rights UI |

---

## G · What is *not* required

- New human user registration  
- File uploads into GIS corpus  
- GODS GBS / SETHS / MADIBA / TS full product depth  
- New Render services beyond existing blueprint  

---

## Pass statement

**UDOC division smoke-pass** when A + B + (C or C2) are green and D2 (biased BLOCK) is observed.  
**Task 2 close:** walk `P6_ASSESSOR_SIDE_BY_SIDE.md` surfaces 1–5 on live Render (operator-verified).
