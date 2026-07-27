# Chapter 11 — Portal Endpoints

## Base Paths: `/portals/student`, `/portals/employer`, `/portals/employee`

Portal endpoints are optimised for the learner-facing, employer-facing, and employee-facing portals. They return data formatted for portal UX — aggregated, pre-computed, and paginated for consumer interfaces.

---

## Student Portal

### `GET /portals/student/dashboard`

Student dashboard overview.

**Required role:** `learner`

**Response:** `200 OK`
```json
{
  "learner": {
    "display_name": "Firstname Lastname",
    "nqf_level": 6,
    "skills_count": 14,
    "verified_skills_count": 8,
    "profile_completeness": 0.78
  },
  "applications": {
    "active": 3,
    "total": 12,
    "latest_status_change": {
      "opportunity_title": "Software Developer",
      "status": "shortlisted",
      "updated_at": "2025-01-14T09:00:00Z"
    }
  },
  "recommendations": {
    "new_count": 5,
    "top_match_score": 0.92
  },
  "notifications": {
    "unread_count": 2
  },
  "documents": {
    "uploaded": 4,
    "missing_recommended": ["reference_letter"]
  }
}
```

---

### `GET /portals/student/opportunities`

Opportunity search with intelligent recommendations.

**Query parameters:** `query`, `province`, `nqf_level`, `remote_ok`, `sector`, `salary_min`, `salary_max`, `sort` (`relevance` \| `date` \| `salary`)

**Response includes:** Opportunity details + match score for the authenticated learner

---

### `POST /portals/student/opportunities/{opportunity_id}/apply`

Submit an application.

**Request body:**
```json
{
  "cover_note": "string (optional, max 500 chars)",
  "document_ids": ["uuid", "uuid"]
}
```

**Response:** `201 Created` — Application record  
**Side effect:** GBS initial screen; learner and employer notified

---

### `GET /portals/student/applications`

Learner's application history with status and next steps.

---

### `POST /portals/student/applications/{application_id}/challenge`

Initiate a governance challenge on a rejected application.

**Request body:**
```json
{
  "challenge_reason": "string (required, min 100 chars)",
  "additional_evidence": "string (optional)"
}
```

**Response:** `201 Created` — Oversight case opened

---

## Employer Portal

### `GET /portals/employer/dashboard`

Employer dashboard.

**Required role:** `employer`

**Response:**
```json
{
  "employer": {
    "company_name": "Acme Corp",
    "verification_status": "verified",
    "active_opportunities": 5,
    "bias_score": 0.12
  },
  "pipeline": {
    "new_applications": 23,
    "under_review": 14,
    "shortlisted": 8,
    "interviews_scheduled": 3
  },
  "compliance": {
    "pending_governance_reviews": 1,
    "overdue_rejections": 0,
    "equity_score": "good"
  }
}
```

---

### `GET /portals/employer/opportunities/{opportunity_id}/pipeline`

Application pipeline for a specific opportunity — kanban view.

**Response:** Applications grouped by status with candidate summaries (no PII for CETCTE applicants in initial stage)

---

### `POST /portals/employer/applications/{application_id}/shortlist`

Move application to shortlisted status.

**Response:** `200 OK`  
**Side effect:** Learner notified; GBS positive decision recorded

---

### `POST /portals/employer/applications/{application_id}/reject`

Reject an application.

**Request body:**
```json
{
  "rejection_reason_code": "skills_mismatch | experience_insufficient | position_filled | other",
  "rejection_notes": "string (required for governance record)"
}
```

**Response:** `200 OK`  
**Side effect:** Rejection submitted to GBS path (FA bias check); learner notified with governance reference

---

## Employee Portal

### `GET /portals/employee/profile`

Post-hire employee profile — employment record, compliance status, training progress.

**Required role:** `seths_employee` (post-hire role assigned after successful offer acceptance)

---

### `GET /portals/employee/compliance`

Employee compliance status — mandatory training, documentation requirements.
