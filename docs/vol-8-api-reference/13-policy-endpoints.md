# Chapter 13 — Policy Endpoints

## Base Path: `/governance/policy-packs`

Policy endpoints provide full CRUD management for PolicyPacks — the configurable governance ruleset.

---

### `GET /governance/policy-packs`

List all PolicyPack versions.

**Required role:** `compliance`, `gods_admin`

**Response:** `200 OK`
```json
{
  "policy_packs": [
    {
      "id": "uuid",
      "version": 3,
      "name": "Standard Employment Governance v3",
      "status": "active",
      "activated_at": "2025-01-10T09:00:00Z",
      "activated_by_name": "Sarah Johnson",
      "rule_count": 7,
      "default_outcome": "REVIEW"
    },
    {
      "id": "uuid",
      "version": 2,
      "name": "Standard Employment Governance v2",
      "status": "archived",
      "activated_at": "2024-07-01T09:00:00Z",
      "archived_at": "2025-01-10T09:00:00Z"
    }
  ]
}
```

---

### `GET /governance/policy-packs/{pack_id}`

Full PolicyPack detail including all rules.

**Response:** `200 OK` — Complete PolicyPack with weights, hard-block thresholds, and all rules

---

### `POST /governance/policy-packs`

Create a new PolicyPack draft.

**Required role:** `compliance`

**Request body:**
```json
{
  "name": "Standard Employment Governance v4",
  "description": "Updated fairness thresholds based on Q1 review",
  "weight_ec": 0.20,
  "weight_si": 0.20,
  "weight_rc": 0.20,
  "weight_fa": 0.20,
  "weight_cc": 0.10,
  "weight_sc": 0.10,
  "hard_block_fa": 45,
  "hard_block_rc": 35,
  "hard_block_sc": 30,
  "default_outcome": "REVIEW",
  "rules": [
    {
      "priority": 1,
      "name": "Excellent Governance — Auto Approve",
      "condition": {
        "min_overall": 90,
        "min_fa": 85
      },
      "outcome": "APPROVE",
      "reasoning_template": "Model scored {overall} overall with strong fairness ({fa_score}). Auto-approved."
    }
  ]
}
```

**Validation rules:**
- Weights must sum to 1.0 (±0.001 for floating point)
- `hard_block_fa` cannot be below 40 (constitutional minimum)
- `hard_block_rc` cannot be below 35
- `hard_block_sc` cannot be below 30
- At least one rule must exist
- Rule priorities must be unique

**Response:** `201 Created` — PolicyPack in `draft` status

---

### `PATCH /governance/policy-packs/{pack_id}`

Update a draft PolicyPack.

**Required role:** `compliance`  
**Constraint:** Only `draft` status packs can be updated

---

### `POST /governance/policy-packs/{pack_id}/submit-for-review`

Submit a draft PolicyPack for review.

**Required role:** `compliance`  
**Transitions:** `draft → review`  
**Audit:** `GOVERNANCE.POLICY_SUBMITTED_FOR_REVIEW`

---

### `POST /governance/policy-packs/{pack_id}/activate`

Activate a PolicyPack (replaces the current active pack).

**Required role:** `gods_admin`  
**Constraint:** Only `review` status packs can be activated  
**Side effect:** Current active pack archived; policy cache refreshed across all instances  
**Audit:** `GOVERNANCE.POLICY_ACTIVATED`

**Response:** `200 OK`
```json
{
  "pack_id": "uuid",
  "version": 4,
  "status": "active",
  "activated_at": "2025-01-15T14:00:00Z",
  "previous_version": 3,
  "cache_refreshed": true,
  "instances_updated": 3
}
```

---

### `GET /governance/policy-packs/active`

Current active PolicyPack.

**Required role:** Any authenticated user (transparency requirement)

**Response:** Full PolicyPack including all rules (read-only, immutable once active)

---

### `GET /governance/policy-packs/{pack_id}/impact-analysis`

Analyse the impact of a draft PolicyPack against historical decisions.

**Required role:** `compliance`, `gods_admin`

**Response:** `200 OK` — Simulation of how the last 30 days of decisions would have been categorised under the proposed PolicyPack vs the current one

```json
{
  "simulation_period": "2025-01-01 to 2025-01-31",
  "decisions_simulated": 14823,
  "outcome_comparison": {
    "current": { "APPROVE": 9834, "REVIEW": 3219, "ESCALATE": 847, "BLOCK": 923 },
    "proposed": { "APPROVE": 9421, "REVIEW": 3612, "ESCALATE": 847, "BLOCK": 943 }
  },
  "net_change": {
    "APPROVE": -413,
    "REVIEW": +393,
    "BLOCK": +20
  },
  "assessment": "The proposed policy is slightly more conservative. Review volume increases by 12%. No constitutional limits affected."
}
```
