# Chapter 08 — Governance Endpoints

## Base Path: `/governance`

Governance endpoints provide access to the GBS Runtime, oversight case management, PolicyPack management, and governance records.

---

## Governance Decisions

### `POST /governance/decisions`

Submit a governance request. This is the primary entry point to the GBS Runtime.

**Required role:** `operator` (own models), `gods_admin` (any model)

**Request body:**
```json
{
  "model_id": "uuid (required)",
  "request_id": "uuid (required — client-provided idempotency key)",
  "input_hash": "sha256:abc123... (required — SHA-256 of model input bytes)",
  "output_category": "classification | generation | employment_decision | risk_assessment | recommendation",
  "affecting_subjects": [
    {
      "subject_type": "individual | organisation | group",
      "subject_id": "uuid (optional — if subject is in G.O.D.S system)",
      "protected_characteristic_weight": 0.3
    }
  ],
  "declared_confidence": 0.87,
  "jurisdiction": "ZA",
  "metadata": {}
}
```

**Response:** `200 OK`
```json
{
  "decision_id": "uuid",
  "request_id": "uuid (echoed)",
  "outcome": "APPROVE | REVIEW | ESCALATE | BLOCK",
  "reasoning": "Model scored 84 overall with strong fairness (87) and regulatory compliance (91). Approved.",
  "eva_scores": {
    "ec": 88, "si": 79, "rc": 91, "fa": 87, "cc": 82, "sc": 90, "overall": 86
  },
  "policy_rule_fired": "Good Governance — Approve with Monitoring",
  "policy_version": 3,
  "governance_ms": 34,
  "decision_seal": "HMAC-SHA256:abc123...",
  "audit_ref_id": "uuid",
  "oversight_case_id": null,
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Idempotency:** Submitting the same `request_id` twice returns the original decision without re-running governance.

**Errors:**
- `404` — Model not found
- `403` — Model not owned by caller
- `422` — Model in sanctioned state (details in `error.code`)
- `503` — Governance engine unavailable (fail-closed)

---

### `GET /governance/decisions`

List governance decisions.

**Query parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | UUID | Filter by model |
| `outcome` | string | APPROVE \| REVIEW \| ESCALATE \| BLOCK |
| `from_date` | date | Start date |
| `to_date` | date | End date |
| `page` | int | Page number |

---

### `GET /governance/decisions/{decision_id}`

Full decision record.

**Response:** `200 OK` — Complete `DecisionRecord` with EVA scores, reasoning, seal, audit trail link, and oversight case (if any)

---

## Oversight Cases

### `GET /governance/oversight`

List oversight cases.

**Required role:** `supervisor`, `compliance`, `gods_admin`

**Query parameters:** `status`, `assigned_to`, `case_type`, `sla_breached` (boolean)

---

### `GET /governance/oversight/{case_id}`

Full oversight case with decision record, subject profile, and action history.

---

### `POST /governance/oversight/{case_id}/resolve`

Resolve an oversight case.

**Required role:** `supervisor` (STANDARD_REVIEW), `compliance` (ESCALATED_REVIEW)

**Request body:**
```json
{
  "resolution": "CONFIRM_APPROVE | CONFIRM_BLOCK | CONFIRM_REVIEW",
  "override_outcome": "APPROVE (required if resolution != CONFIRM_BLOCK)",
  "notes": "string (required — reviewer notes, min 50 chars)",
  "additional_evidence": "string (optional)"
}
```

**Audit:** `GOVERNANCE.OVERSIGHT_RESOLVED`

---

## Policy Management

### `GET /governance/policy-packs`

List all PolicyPack versions.

**Required role:** `compliance`, `gods_admin`

---

### `POST /governance/policy-packs`

Create a new PolicyPack draft.

**Required role:** `compliance`

**Request body:** Full PolicyPack structure (see Volume V, Chapter 04)

---

### `POST /governance/policy-packs/{pack_id}/activate`

Activate a PolicyPack (replaces current active pack).

**Required role:** `compliance` (submit for approval) + `gods_admin` (final activation)  
**Two-step approval required** — compliance submits, admin activates.

**Audit:** `GOVERNANCE.POLICY_ACTIVATED`

---

### `GET /governance/constitution`

Current constitutional check status — which of the 11 constitutional checks are active.

**Required role:** Any authenticated user (read-only visibility)  
**Response:** Constitutional check registry — immutable, for transparency
