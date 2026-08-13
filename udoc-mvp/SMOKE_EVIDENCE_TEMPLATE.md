# Smoke evidence template · operator record

**Purpose:** Capture a single live verification run so Capstone evidence is a dated fact, not a commit message.  
**Related:** `UDOC_SMOKE_PASS.md` · `P6_ASSESSOR_SIDE_BY_SIDE.md` · `CAPSTONE_ASSESSOR_PACK.md`  
**Rule:** Task 2 closes only when this (or equivalent) is filled with **live** results — not simulated UI.

Copy this section into a dated note, issue, or Capstone evidence folder when you run the check.

---

## Run header

| Field | Value |
|-------|--------|
| Date (SAST) | 2026-08-13 |
| Operator | automation + founder confirm |
| Core API base | `https://gods-platform-core.onrender.com` |
| Browser / hard-refresh | Recommended before assessor demo |
| Notes (cold start, etc.) | demo/ready auto-healed model-001 SUSPENDED→ACTIVE |

---

## A — Core health

| Check | URL / action | Result (pass/fail) | Observation |
|-------|--------------|--------------------|-------------|
| Health | `GET /health` | **PASS** | status ok |
| Demo ready | `GET /udoc/demo/ready` | **PASS** | ready true · model-001 ACTIVE · pack ACTIVE · 5 rules |
| Policy active | `GET /policy/active` (or Sentinel) | (operator) | |

---

## B — Sentinel

| Check | Result | Observation |
|-------|--------|-------------|
| DEMO READY / boot banner | (operator) | |
| Fair scenario ≠ BLOCK | **PASS** (API) | APPROVE |
| **Biased scenario = BLOCK** | **PASS** (API) | **Required** |
| Smoke panel (if present) | (operator) | Assessor one-click preferred |
| Full EVA batch / outcome KPIs | (operator) | optional density |

URL: `https://gods-platform-core.onrender.com/Sentinel`

---

## C — Client Govern

| Check | Result | Observation |
|-------|--------|-------------|
| Sign-in (existing operator) | (operator) | no new registration · client@udoc.demo or staff |
| Fair / healthy ≠ BLOCK | (operator) | |
| **Biased = BLOCK** | (operator) | **Required** |
| Client mini-smoke (if button present) | (operator) | |
| Cert / evidence after EVA | (operator) | optional |

URL: `https://gods-udoc-client.onrender.com` → Govern

---

## D — Citizen (public)

| Check | Result | Observation |
|-------|--------|-------------|
| `/citizen.html` loads without login | (operator) | |
| Challenge returns case_ref | (operator) | POST /citizen/challenge |
| Status lookup works | (operator) | |

---

## E — Package honesty (spot check)

| Check | Result |
|-------|--------|
| Client App/Mobile: no Hardware plane as product path | (operator) |
| Gateway role routes to expected host | (operator) |
| Internal Admin reachable as staff path | (operator) |
| Division login chips present | **PASS** (static) · 4-role fillLogin |

---

## Verdict

| Gate | Pass? |
|------|-------|
| A health + demo/ready | **YES** (2026-08-13 API) |
| B biased BLOCK | **YES** (API) |
| C biased BLOCK | (operator UI confirm) |
| D citizen public | (operator) |
| **Task 2 close eligible** | Yes when A+B+C pass on live hosts |

**Signature / initials:** _______________  
**Follow-up if fail:** list only failed surfaces — fix those, do not expand scope.

---

## Automation stamp (not a substitute for operator UI)

- 2026-08-13: health ok · demo/ready true · EVA fair=APPROVE biased=BLOCK on Core batch endpoint.
- Login density residual closed on all operator + admin surfaces.
- Website / Netlify §7 still human-pending (website last).
