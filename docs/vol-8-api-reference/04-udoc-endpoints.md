# Chapter 04 — UDOC Endpoints

## Endpoint Summary

| Method | Path | Required Role | Description |
|--------|------|--------------|-------------|
| `POST` | `/registry/models` | `operator` | Register a new AI model |
| `GET` | `/registry/models` | `operator` | List own models (admin: all) |
| `GET` | `/registry/models/{id}` | `operator` | Get model details |
| `PATCH` | `/registry/models/{id}` | `operator` | Update model metadata |
| `POST` | `/registry/models/{id}/certify` | `compliance` | Certify a model |
| `POST` | `/registry/models/{id}/deploy` | `compliance` | Mark model as active |
| `POST` | `/registry/models/{id}/suspend` | `operator` or `gods_admin` | Suspend (kill-switch) |
| `POST` | `/registry/models/{id}/resume` | `compliance` | Resume a suspended model |
| `POST` | `/registry/models/{id}/decommission` | `gods_admin` | Permanently decommission |
| `POST` | `/decisions` | `operator` | Submit a governance request |
| `GET` | `/decisions/{id}` | `operator` | Get a decision record |
| `GET` | `/decisions` | `operator` | List own decisions |
| `GET` | `/registry/models/{id}/decisions` | `operator` | List decisions for a model |
| `GET` | `/udoc/dashboard` | `operator` | Operator dashboard metrics |

---

## POST /registry/models — Register a Model

**Request:**
```json
{
  "name": "Resume Screening Model v3",
  "version": "3.0.1",
  "model_type": "classification",
  "declared_purpose": "Screen job applications against listed requirements. Output: suitability score and ranked list of criteria met.",
  "affected_subjects": ["individual", "employment"],
  "training_data_declaration": "Trained on anonymised historical application data from 2019–2023, reviewed for demographic balance.",
  "third_party_audit": true,
  "audit_report_url": "https://auditor.example.com/reports/xyz",
  "jurisdiction": "ZA"
}
```

**Response 201:**
```json
{
  "data": {
    "id": "model-uuid",
    "status": "pending_review",
    "created_at": "datetime",
    "certification_required_by": "datetime",
    "next_steps": [
      "A compliance officer will review your registration within 5 business days.",
      "You will receive a notification when your model is certified.",
      "Install the udoc-agent on your model host: https://docs.gods.internal/udoc-agent-setup"
    ]
  }
}
```

---

## POST /decisions — Submit a Governance Request

This is the primary endpoint called by the `udoc-agent`, `udoc-gateway`, or direct API clients.

**Request:**
```json
{
  "model_id": "model-uuid",
  "request_id": "client-generated-uuid",
  "input_hash": "sha256-of-the-input-to-the-model",
  "output_category": "classification",
  "declared_confidence": 0.87,
  "affecting_subjects": ["subject-id"],
  "jurisdiction": "ZA",
  "context": {
    "action_type": "employment_screening",
    "affecting_protected_groups": false
  }
}
```

**Response 200:**
```json
{
  "data": {
    "decision_id": "decision-uuid",
    "request_id": "client-generated-uuid",
    "outcome": "APPROVE",
    "reasoning": "Request scored 82/100 overall (EC:88, SI:79, RC:91, FA:85, CC:76, SC:88). Approved under PolicyPack GV3 threshold of 65.",
    "eva_scores": {
      "ethical_cooperation": 88,
      "societal_impact": 79,
      "regulatory_compliance": 91,
      "fairness": 85,
      "confidence_calibration": 76,
      "sovereignty_compliance": 88,
      "overall": 82
    },
    "sealed": true,
    "governance_ms": 23,
    "timestamp": "2025-01-15T10:30:00.123Z"
  }
}
```

**Response when BLOCK:**
```json
{
  "data": {
    "decision_id": "decision-uuid",
    "outcome": "BLOCK",
    "reasoning": "Fairness dimension scored 0: detected explicit reference to protected characteristic 'race' in output category 'employment_screening'. Constitutional violation — automatic BLOCK.",
    "eva_scores": {
      "fairness": 0,
      "overall": 0
    },
    "oversight_case_id": "case-uuid",
    "appeal_instructions": "An oversight case has been opened. The subject may request review at /oversight/cases/{case-uuid}.",
    "sealed": true
  }
}
```

**Performance:** The `/decisions` endpoint is on the critical path. Target response time: <50ms p95.

---

## POST /registry/models/{id}/suspend — Kill-Switch

**Required Role:** `operator` (own models), `gods_admin` (any model)

**Request:**
```json
{
  "reason": "Discovered systematic bias in output distribution during internal review. Suspending pending re-evaluation.",
  "immediate_effect": true,
  "notify_affected_subjects": true
}
```

**Response 200:**
```json
{
  "data": {
    "model_id": "model-uuid",
    "status": "suspended",
    "suspended_at": "datetime",
    "propagation_status": "propagating",
    "edge_nodes_notified": 3,
    "estimated_propagation_ms": 30000,
    "audit_ref_id": "audit-uuid"
  }
}
```

**Effect:** Immediate in `platform-core`. Propagation to edge nodes via Kafka — target <30 seconds. The `propagation_status` field updates to `propagated` once all known edge nodes have confirmed receipt.
