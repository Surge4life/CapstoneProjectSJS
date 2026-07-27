# Chapter 07 — TS Industries Endpoints

## Base Path: `/ts`

TS Industries endpoints manage industrial project submissions, sector information, and partner management.

---

## Projects

### `GET /ts/projects`

List industrial pipeline projects.

**Required role:** Any authenticated user (results scoped by role)

**Query parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `sector_code` | string | Filter by sector |
| `province` | string | Filter by province |
| `status` | string | Project status filter |
| `submission_type` | string | new_build \| expansion \| rehabilitation \| maintenance \| feasibility |
| `project_type` | string | public_private_partnership \| public_works \| municipal_infrastructure \| sez |

**Response:** `200 OK`
```json
{
  "projects": [
    {
      "id": "uuid",
      "project_name": "string",
      "project_code": "TS-2025-001",
      "sector": { "code": "ENERGY", "name": "Energy" },
      "province": "Northern Cape",
      "estimated_value": 2500000000,
      "status": "approved",
      "submission_type": "new_build",
      "job_creation_target": 500,
      "partners_assigned": 3,
      "created_at": "2025-01-10T00:00:00Z"
    }
  ],
  "total": 124
}
```

---

### `POST /ts/projects`

Submit a new industrial project.

**Required role:** `gods_admin`, `division_admin`, or users with `ts:project:submit` permission

**Request body:**
```json
{
  "project_name": "string (required)",
  "sector_code": "ENERGY",
  "description": "string (required)",
  "province": "Northern Cape",
  "municipality": "string (optional)",
  "estimated_value": 2500000000,
  "duration_months": 48,
  "job_creation_target": 500,
  "submission_type": "new_build",
  "project_type": "public_private_partnership",
  "gpo_reference": "GPO-2025-0042 (optional)"
}
```

**Response:** `201 Created` — Project record with governance outcome  
**Side effect:** GBS pre-check run; project assigned auto-generated `project_code`

---

### `GET /ts/projects/{project_id}`

Full project record with partners, compliance flags, and governance history.

---

### `POST /ts/projects/{project_id}/assign-partner`

Assign a partner to a project.

**Required role:** `division_admin`

**Request body:**
```json
{
  "partner_id": "uuid",
  "role": "lead_contractor",
  "scope_of_work": "string (required)",
  "contract_value": 800000000
}
```

**Response:** `201 Created` — Assignment record  
**Side effect:** GBS governance path for partner assignment (FA + SC dimensions)

---

## Sectors

### `GET /ts/sectors`

List all sectors with their requirements.

**Response:** `200 OK`
```json
{
  "sectors": [
    {
      "code": "ENERGY",
      "name": "Energy",
      "regulator": "NERSA",
      "primary_legislation": ["Electricity Regulation Act", "MPRDA"],
      "active_projects": 23,
      "governance_configuration": {
        "elevated_rc_weight": true,
        "policy_pack_active": "ENERGY_GV2"
      }
    }
  ]
}
```

---

### `GET /ts/sectors/{sector_code}/requirements`

Detailed governance requirements for a specific sector.

**Response:** `200 OK` — Full sector governance specification including EVA weight overrides and policy pack rules

---

## Partners

### `GET /ts/partners`

Browse registered build assistant partners.

**Query parameters:** `sector_code`, `province`, `bee_level_max`, `cidb_grading`, `verified_only`

---

### `POST /ts/partners`

Register as a build assistant partner.

**Request body:**
```json
{
  "company_name": "string (required)",
  "registration_number": "string (required — CIPC)",
  "cidb_grading": "7CE",
  "bee_level": 2,
  "sector_capabilities": ["ENERGY", "INFRASTRUCTURE"],
  "specialisations": ["Solar PV", "Grid Infrastructure"],
  "max_project_value": 1000000000
}
```

**Response:** `201 Created` — Partner record; verification status starts as `pending`

---

### `GET /ts/partners/{partner_id}/match`

Intelligence-powered partner capability match for a project.

**Query parameters:** `project_id` (required)

**Response:** `200 OK`
```json
{
  "partner_id": "uuid",
  "match_score": 0.87,
  "matching_capabilities": ["Solar PV", "Grid Infrastructure"],
  "capability_gaps": [],
  "similar_projects_completed": 3,
  "recommendation": "Excellent match — all required capabilities present."
}
```
