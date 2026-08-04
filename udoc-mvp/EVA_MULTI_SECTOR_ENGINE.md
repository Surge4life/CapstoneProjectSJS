# EVA multi-sector engine

**Commits:** `199be1ae` (governance_bridge) · `134ccce3` (decisions wire)

## Sectors (weights + thresholds)

| Sector | Emphasis |
|--------|----------|
| GENERAL | Baseline SA 6-D |
| PUBLIC | Compliance + societal elevated |
| PRIVATE | Risk + confidence |
| HEALTH | Risk floor stricter |
| FINANCE | DI / parity strict |
| EDUCATION | Inclusion + societal |
| JUSTICE | Explainability + audit floors |
| WELFARE | Inclusion + fairness |

Aliases: GOV→PUBLIC, BANKING→FINANCE, MEDICAL→HEALTH, SASSA→WELFARE, etc.

## Metric scales

- `dimensions` — 0–10 (UI legacy)
- `scales.scale_0_100` — 0–100 inclusive reporting
- `scales.normalized_0_1` — full metric vector
- `composite_eva` — 0–10 · `scales.composite_0_100` — 0–100

## Deterministic controllers

RISK_CAP · COMPLIANCE_FLOOR · DISPARATE_IMPACT · STATISTICAL_PARITY · DISTRIBUTION_DRIFT · ETHICAL_COOPERATION · UNACCEPTABLE_TIER · EXPLAINABILITY · AUDIT_TRAIL · INCLUSION_ACCESS · HITL_REQUIRED · SOVEREIGNTY · SECTOR_DUTY · soft bands APPROVE/REVIEW/ESCALATE

Each returns `{controller, fired, severity, message}` on the decision response.

## API

```json
POST /decisions
{
  "model_id": "model-001",
  "sector": "HEALTH",
  "explainability": 0.9,
  "audit_trail": 0.95,
  "inclusion_access": 0.8,
  "human_oversight_present": true
}
```

Batch accepts optional `sector` for the matrix pack.

## Smoke

Legacy fair≠BLOCK / biased=BLOCK preserved with default metrics (explainability/audit/inclusion defaults above floors).
