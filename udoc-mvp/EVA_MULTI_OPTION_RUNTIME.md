# UDOC EVA multi-option runtime

**Task 2 · systems development** (while GBS V2 / 11-document collection is finalized offline)  
**Endpoint:** `POST /decisions/batch` on `gods-platform-core`  
**Updated:** 2026-08-03

---

## Purpose

One API call runs **multiple EVA options** on the same non-bypassable path as single `POST /decisions`:

| Option | Intent |
|--------|--------|
| `fair` | Balanced fairness counts → expect ≠ BLOCK |
| `biased` | Disparate impact → expect **BLOCK** |
| `high` | `risk_tier=HIGH` → BLOCK + HITL policy |
| `sov` | Weak sovereignty signals → sovereignty gate |
| `custom` | Overrides via `items[]` fields |

Default body:

```json
{ "model_id": "model-001", "options": ["fair", "biased", "high", "sov"] }
```

Response includes `outcomes` KPIs and `gate.fair_neq_block` / `gate.biased_eq_block` for smoke.

---

## Relationship to GBS-T.S. (honest)

GBS-T.S. proposes reusing **EVA/UDOC assurance** for a wider class of systems (not only AI decision events). This batch endpoint is **UDOC runtime systems work** — Capstone evidence that multiple assurance questions can be executed live under one fail-closed engine. It does **not** implement GBS-T.S. certification for non-AI systems; that remains designed / post–founder-confirm (Option A vs B on T.S. eighth subsidiary).

---

## UI surfaces

Client / Sentinel / Admin / Sector already run scenario chips client-side. After Core deploy they may call `/decisions/batch` for a single round-trip Full EVA matrix.

---

## Task 1 note

Task 1 (Canon / GIS–GBS collection commits) waits until you finalize the 11-document V2 pass offline. Task 2 continues on UDOC EVA/runtime only.
