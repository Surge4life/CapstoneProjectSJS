# Chapter 14 — SETHS Engine

## Purpose

The SETHS Engine manages the complete workforce governance lifecycle — from learner enrolment through skills development, opportunity matching, application management, employment verification, and reintegration support. It is the largest division engine in terms of user-facing features.

---

## Location

- **Router:** `platform-core/app/routers/seths.py`
- **Router:** `platform-core/app/routers/workforce.py`
- **Router:** `platform-core/app/routers/portals_student.py`
- **Router:** `platform-core/app/routers/portals_employer.py`
- **Router:** `platform-core/app/routers/portals_employee.py`
- **Service:** `platform-core/app/services/cetcte_engine.py`
- **Frontend:** `seths-app/`, `portals-web/`
- **Mobile:** `seths-mobile/`

---

## Data Model Overview

```
Learner ──< Application >── Opportunity ──< Employer
   |                                           |
   |──< Document (CV, qualifications)          |──< Employee
   |──< TimesheetEntry                         |
   |──< Student (NQF record)                   |
```

### Key Models

**Learner**
- Personal details (POPIA-governed)
- Skills profile
- Progress tracking (courses, certifications)
- Document references (SHA-256 sealed)
- Reintegration status (CETCTE)

**Employer**
- Registration and verification status
- BEE level and Employment Equity status
- Opportunity postings
- Hiring history (for bias analysis)

**Opportunity**
- Job description
- Required qualifications (NQF level)
- Location and remote status
- Closing date
- Matching criteria

**Application**
- Learner + Opportunity link
- Status: `SUBMITTED | REVIEWED | SHORTLISTED | OFFERED | ACCEPTED | REJECTED | WITHDRAWN`
- Governance decision reference (every status change that rejects an application goes through GBS)
- Supporting documents

---

## CETCTE Engine (Reintegration)

CETCTE — Community and Employer Trust in Community Transition and Employment — is the reintegration support service within SETHS. It manages:

- Individuals transitioning from incarceration, rehabilitation programmes, or long-term unemployment
- Support plan creation and tracking
- Employer trust-building (anonymised matching with disclosure only at employer consent stage)
- Progress tracking and reporting

The CETCTE engine applies heightened GBS scrutiny to decisions that affect CETCTE participants — the EVA thresholds for fairness and societal impact are elevated for this cohort.

---

## Document Governance

The SETHS document system is a significant governance feature:

**Upload flow:**
1. Learner uploads CV, qualification certificates, or supporting documents
2. Document stored in object storage (S3-compatible)
3. SHA-256 hash computed and stored
4. UDOC audit record created (document sealed to audit chain)
5. Document entry created in `Document` table with hash, storage ref, and audit record ID

**Download flow:**
1. Authorised party requests document
2. SHA-256 hash of stored file recomputed
3. Hash verified against stored hash — if mismatch, `INTEGRITY_FAILURE` error (document tampered with)
4. Download access logged in audit chain
5. Document served from object storage

This system provides proof of document integrity — any document served from the SETHS system can be verified against the audit chain.

---

## Opportunity Matching

The SETHS opportunity matching engine uses G.O.D.S Intelligence for initial matching (ranking learners against opportunities by skills, qualifications, and geography), followed by GBS Runtime validation of the match results.

The GBS validation specifically checks:
- No protected-characteristic bias in the ranking
- NQF level requirements are legitimately relevant to the role
- Geographic restrictions are legally permissible
- Salary ranges meet minimum wage requirements

Matches that fail GBS validation are flagged, not suppressed — an employer can see that a match was flagged and why, but the flag is advisory unless the issue is a constitutional violation.

---

## Employment Equity Compliance

The SETHS engine actively tracks employment equity metrics for registered employers. This includes:
- Workforce demographics by occupational level
- Recruitment demographics by applicant pool and hire rate
- Bias detection across demographic groups

The `bias` router in `platform-core` provides these analytics. An employer who shows persistent demographic bias in their hiring receives escalated GBS scrutiny on new opportunity postings.

This is not punitive — it is governance. The system flags the pattern, provides the evidence, and creates an oversight pathway. The compliance officer determines whether the pattern constitutes an Employment Equity Act violation.
