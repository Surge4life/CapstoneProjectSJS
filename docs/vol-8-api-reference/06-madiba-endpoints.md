# Chapter 06 — MADIBA Endpoints

## Base Path: `/madiba`

MADIBA endpoints manage the capital investment pipeline. Access is scoped to the authenticated user's role: `investor` sees their own records; `division_admin` sees all.

---

## Projects

### `GET /madiba/projects`

List capital pipeline projects.

**Required role:** `investor`, `division_admin`, `compliance`

**Query parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by status |
| `sector` | string | Filter by sector |
| `province` | string | Filter by province |
| `min_capital` | number | Minimum capital required (ZAR) |
| `max_capital` | number | Maximum capital required (ZAR) |

**Response:** `200 OK`
```json
{
  "projects": [
    {
      "id": "uuid",
      "project_name": "string",
      "sector": "string",
      "capital_required": 50000000,
      "capital_committed": 30000000,
      "status": "funded",
      "province": "Gauteng",
      "jobs_projected": 150,
      "milestone_completion_rate": 0.67,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "total": 47
}
```

---

### `POST /madiba/projects`

Submit a new capital pipeline project.

**Required role:** `investor` (project proposer), `division_admin`

**Request body:**
```json
{
  "project_name": "string (required)",
  "sector": "string (required)",
  "description": "string (required, min 100 chars)",
  "province": "string (required)",
  "municipality": "string (optional)",
  "capital_required": 50000000,
  "capital_currency": "ZAR",
  "duration_months": 36,
  "job_creation_target": 150,
  "target_start_date": "2025-06-01",
  "sdg_alignment": ["SDG8", "SDG9"]
}
```

**Response:** `201 Created` — Project record with ID and governance outcome  
**Side effect:** Project submitted to GBS governance path  
**Audit:** `DATA_CHANGE.MADIBA_PROJECT_SUBMITTED`

---

### `GET /madiba/projects/{project_id}`

Get full project record.

**Response:** `200 OK` — Project record with milestones, allocations, and governance history

---

### `PATCH /madiba/projects/{project_id}`

Update project details. Only `submitted` or `under_review` projects can be updated.

**Required role:** Project owner or `division_admin`

---

## Milestones

### `GET /madiba/projects/{project_id}/milestones`

List project milestones.

**Response:** `200 OK`
```json
{
  "milestones": [
    {
      "id": "uuid",
      "milestone_name": "Site acquisition",
      "sequence_number": 1,
      "status": "completed",
      "target_date": "2025-03-31",
      "completed_at": "2025-03-28T10:00:00Z",
      "capital_release_amount": 5000000,
      "capital_released": true
    }
  ]
}
```

---

### `POST /madiba/projects/{project_id}/milestones/{milestone_id}/complete`

Record milestone completion.

**Required role:** Project owner or `division_admin`

**Request body:**
```json
{
  "completion_notes": "string (required)",
  "evidence_document_id": "uuid (optional — document must be uploaded first)"
}
```

**Response:** `200 OK` — Updated milestone record  
**Side effect:** Investor notification sent; capital release triggered if configured  
**Audit:** `DATA_CHANGE.MADIBA_MILESTONE_COMPLETED`

---

## Capital Allocations

### `POST /madiba/allocations`

Record a capital allocation from an investor to a project.

**Required role:** `investor` or `division_admin`

**Request body:**
```json
{
  "project_id": "uuid (required)",
  "amount": 25000000,
  "currency": "ZAR",
  "allocation_type": "equity",
  "disbursement_schedule": [
    {"date": "2025-06-01", "amount": 10000000},
    {"date": "2025-09-01", "amount": 15000000}
  ]
}
```

**Response:** `201 Created` — Allocation record with governance outcome  
**Side effect:** GBS governance path run on allocation  
**Audit:** `DATA_CHANGE.MADIBA_ALLOCATION_CREATED`

---

## Investor Management

### `GET /madiba/investors/{investor_id}`

Get investor profile.

**Required role:** Own record (investor), `division_admin`

---

### `POST /madiba/investors`

Register as an investor.

**Request body:**
```json
{
  "entity_name": "string (required)",
  "entity_type": "institutional",
  "registration_number": "string",
  "jurisdiction": "ZA",
  "investment_mandate": "string",
  "minimum_ticket_size": 5000000,
  "maximum_ticket_size": 500000000,
  "preferred_sectors": ["ENERGY", "INFRASTRUCTURE"]
}
```

**Response:** `201 Created` — Investor record with ID and verification status
