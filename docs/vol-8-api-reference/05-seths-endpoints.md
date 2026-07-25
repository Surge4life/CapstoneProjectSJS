# Chapter 05 — SETHS Endpoints

## Endpoint Summary

| Method | Path | Required Role | Description |
|--------|------|--------------|-------------|
| `POST` | `/seths/learners` | `learner` (self) or `gods_admin` | Register as a learner |
| `GET` | `/seths/learners/{id}` | `learner` (own), `supervisor`, `gods_admin` | Get learner profile |
| `PATCH` | `/seths/learners/{id}` | `learner` (own), `gods_admin` | Update learner profile |
| `GET` | `/seths/learners/{id}/applications` | `learner` (own) | Get own applications |
| `POST` | `/seths/employers` | `employer` (self) | Register as an employer |
| `GET` | `/seths/employers/{id}` | Authenticated | Get employer profile |
| `POST` | `/seths/opportunities` | `employer` | Post a new opportunity |
| `GET` | `/seths/opportunities` | Authenticated | Search/list opportunities |
| `GET` | `/seths/opportunities/{id}` | Authenticated | Get opportunity detail |
| `POST` | `/seths/opportunities/{id}/apply` | `learner` | Apply for an opportunity |
| `PATCH` | `/seths/applications/{id}/status` | `employer` | Update application status |
| `POST` | `/seths/documents` | `learner` | Upload a document |
| `GET` | `/seths/documents/{id}` | `learner` (own), `employer` (if application active) | Download a document |
| `GET` | `/workforce/portals/student` | `learner` | Student portal data |
| `GET` | `/workforce/portals/employer` | `employer` | Employer portal data |

---

## POST /seths/opportunities/{id}/apply

A learner applies for a job opportunity.

**Request:**
```json
{
  "cover_letter": "string — optional"
}
```

**Response 201:**
```json
{
  "data": {
    "application_id": "uuid",
    "opportunity": {
      "id": "uuid",
      "title": "Junior Software Developer",
      "employer_name": "Acme Corp"
    },
    "status": "submitted",
    "submitted_at": "datetime"
  }
}
```

---

## PATCH /seths/applications/{id}/status

An employer updates an application's status (shortlist, offer, reject).

**Required Role:** `employer` (must own the opportunity)

**Request:**
```json
{
  "status": "shortlisted",
  "notes": "Strong NQF 6 qualification, relevant portfolio. Moving to interview stage."
}
```

For `rejected` status, an additional field is required:
```json
{
  "status": "rejected",
  "rejection_reason": "qualification_mismatch",
  "rejection_detail": "The role requires NQF 7 (degree level). Applicant holds NQF 6."
}
```

**GBS Governance Integration:**  
Every status change that results in a rejection is submitted to the governance path before being applied. The request payload includes:
- `action_type: "employment_rejection"`
- `rejection_reason` (checked against protected characteristics)
- Employer's historical bias score

If the GBS engine returns `BLOCK` (e.g., rejection reason implies protected characteristic bias), the status change is not applied and an oversight case is created. The employer receives a governance error response.

**Response 200 (if APPROVE):**
```json
{
  "data": {
    "application_id": "uuid",
    "new_status": "rejected",
    "governance_decision": {
      "outcome": "APPROVE",
      "decision_id": "uuid",
      "governance_ms": 18
    }
  }
}
```

**Response 403 (if BLOCK):**
```json
{
  "error": {
    "code": "GOVERNANCE_BLOCK",
    "message": "This rejection could not be processed. A governance review has been opened.",
    "oversight_case_id": "case-uuid",
    "decision_id": "decision-uuid"
  }
}
```

---

## POST /seths/documents — Upload a Document

A learner uploads a document (CV, qualification certificate, etc.).

**Content-Type:** `multipart/form-data`

**Form fields:**
- `file` — the file (required, max 10MB)
- `document_type` — `cv | qualification | id_document | reference | portfolio | other`
- `nqf_level` — integer 1–10 (required if type is `qualification`)
- `institution` — string (required if type is `qualification`)
- `year_obtained` — integer (required if type is `qualification`)

**Response 201:**
```json
{
  "data": {
    "document_id": "uuid",
    "file_name": "Sashin_Singh_CV_2025.pdf",
    "sha256_hash": "a8b3f1...",
    "udoc_audit_ref": "audit-uuid",
    "sealed": true,
    "message": "Document uploaded and sealed to the UDOC audit chain."
  }
}
```

The `sealed: true` means the document's SHA-256 hash has been recorded in the audit chain. Any future download will have its hash verified against this record. If the hashes do not match, the download is rejected with `INTEGRITY_FAILURE`.

---

## GET /seths/documents/{id} — Download a Document

**Response:**

If the document hash passes integrity verification:
- HTTP 200 with `Content-Type` matching the document MIME type
- Binary file content
- Headers: `X-Document-Hash: <sha256>`, `X-Integrity-Verified: true`

If the hash fails:
```json
{
  "error": {
    "code": "INTEGRITY_FAILURE",
    "message": "Document hash does not match the sealed record. This document may have been tampered with.",
    "document_id": "uuid",
    "sealed_hash": "expected-hash",
    "actual_hash": "computed-hash"
  }
}
```

An `INTEGRITY_FAILURE` is also written to the audit chain as a critical security event.
