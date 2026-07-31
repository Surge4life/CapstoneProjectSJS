# Smoke evidence template · operator record

**Purpose:** Capture a single live verification run so Capstone evidence is a dated fact, not a commit message.  
**Related:** `UDOC_SMOKE_PASS.md` · `P6_ASSESSOR_SIDE_BY_SIDE.md`  
**Rule:** Task 2 closes only when this (or equivalent) is filled with **live** results — not simulated UI.

Copy this section into a dated note, issue, or Capstone evidence folder when you run the check.

---

## Run header

| Field | Value |
|-------|--------|
| Date (SAST) | |
| Operator | |
| Core API base | `https://gods-platform-core.onrender.com` |
| Browser / hard-refresh | Yes / No |
| Notes (cold start, etc.) | |

---

## A — Core health

| Check | URL / action | Result (pass/fail) | Observation |
|-------|--------------|--------------------|-------------|
| Health | `GET /health` | | |
| Demo ready | `GET /udoc/demo/ready` | | model-001 + ACTIVE pack? |
| Policy active | `GET /policy/active` (or Sentinel) | | |

---

## B — Sentinel

| Check | Result | Observation |
|-------|--------|-------------|
| DEMO READY / boot banner | | |
| Fair scenario ≠ BLOCK | | |
| **Biased scenario = BLOCK** | | **Required** |
| Smoke panel (if present) | | |
| Full EVA batch / outcome KPIs | | optional density |

URL: `https://gods-platform-core.onrender.com/Sentinel`

---

## C — Client Govern

| Check | Result | Observation |
|-------|--------|-------------|
| Sign-in (existing operator) | | no new registration |
| Fair / healthy ≠ BLOCK | | |
| **Biased = BLOCK** | | **Required** |
| Client mini-smoke (if button present) | | |
| Cert / evidence after EVA | | optional |

URL: `https://gods-udoc-client.onrender.com` → Govern

---

## D — Citizen (public)

| Check | Result | Observation |
|-------|--------|-------------|
| `/citizen.html` loads without login | | |
| Challenge returns case_ref | | |
| Status lookup works | | |

---

## E — Package honesty (spot check)

| Check | Result |
|-------|--------|
| Client App/Mobile: no Hardware plane as product path | |
| Gateway role routes to expected host | |
| Internal Admin reachable as staff path | |

---

## Verdict

| Gate | Pass? |
|------|-------|
| A health + demo/ready | |
| B biased BLOCK | |
| C biased BLOCK | |
| D citizen public | |
| **Task 2 close eligible** | Yes only if A+B+C pass |

**Signature / initials:** _______________  
**Follow-up if fail:** list only failed surfaces — fix those, do not expand scope.
