# Chapter 05 — Commits 021–030: SETHS Division Foundation

## Overview

This commit batch establishes the SETHS division: learners, employers, opportunities, applications, and the document management system. After these commits, the employment services functionality is operational end-to-end.

---

## Commit 021: `[DB] MIGRATE: Add SETHS schemas — learners, employers, opportunities, applications`

**What:** Creates the core SETHS database tables.  
**Includes:**
- `seths.learners` — learner profiles
- `seths.employer_profiles` — employer records
- `seths.opportunities` — job/training postings
- `seths.applications` — applications linking learners to opportunities
- All related indexes

**SQL:** `platform-core/migrations/021_seths_core_tables.sql`

---

## Commit 022: `[CORE] ADD: SETHS learner service — registration, profile management`

**What:** Implements `learner_service.py` with:
- `register_learner()` — creates learner record with POPIA consent tracking
- `update_profile()` — profile updates with change audit
- `get_profile()` — full profile retrieval
- `export_data()` — POPIA data subject access export

**Tests:** `tests/test_seths_learner.py`

---

## Commit 023: `[CORE] ADD: SETHS employer service — registration, verification`

**What:** Implements `employer_service.py`:
- `register_employer()` — employer self-registration
- `verify_employer()` — compliance officer verification workflow
- `update_employer()` — profile updates
- `get_employer()` — employer record retrieval

Verification status state machine: `unverified → verified | requires_clarification`

---

## Commit 024: `[CORE] ADD: Opportunity management service`

**What:** Implements opportunity CRUD with governance pre-check:
- `create_opportunity()` — drafts opportunity, triggers GBS compliance pre-check
- `publish_opportunity()` — publishes if pre-check passes
- `close_opportunity()` — closes with reason
- `search_opportunities()` — learner-facing search with filters (NQF, province, sector, remote)

The GBS compliance pre-check on opportunity creation evaluates:
- Salary range vs minimum wage (RC dimension)
- Requirement language for protected characteristic proxies (FA dimension)

---

## Commit 025: `[CORE] ADD: Application pipeline service`

**What:** Implements the application lifecycle:
- `submit_application()` — learner applies to opportunity; triggers GBS initial screen
- `update_application_status()` — employer updates status (shortlist, reject, offer)
- Rejection path: every rejection submitted to GBS path (FA + historical bias check)
- `get_application()` — full application record with governance history

---

## Commit 026: `[DB] MIGRATE: Add SETHS document vault tables`

**What:** Creates document storage tables:
- `seths.documents` — document metadata with SHA-256, UDOC audit ref, storage key
- Indexes on `learner_id`, `document_type`, `created_at`

---

## Commit 027: `[CORE] ADD: Document store service — upload, seal, download, verify`

**What:** Implements `document_store.py` (as specified in Vol II, Chapter 11):
- Upload with SHA-256 sealing + audit chain write
- Download with integrity re-verification
- `DOCUMENT_INTEGRITY_FAILURE` detection and alerting

**Tests:** `tests/test_document_store.py` — includes intentional tamper test

---

## Commit 028: `[CORE] ADD: SETHS API router — all learner and employer endpoints`

**What:** Exposes all SETHS services via `platform-core/app/routers/seths.py`:
- `/seths/learners/*`
- `/seths/employers/*`
- `/seths/opportunities/*`
- `/seths/applications/*`
- `/seths/documents/*`

All routes protected by appropriate RBAC permissions.

---

## Commit 029: `[UI] ADD: SETHS web app — full learner flow`

**What:** Implements the learner-facing SETHS web application:
- Connect screen, registration, login
- Dashboard with opportunity recommendations
- Opportunity search and application submission
- Document upload and management
- Application status tracking

**Path:** `seths-app/`

---

## Commit 030: `[UI] ADD: SETHS web app — employer portal`

**What:** Adds the employer view to the SETHS app:
- Employer registration and verification status
- Opportunity creation and management
- Application pipeline (kanban view)
- Employment equity metrics dashboard
- GBS compliance notifications

Employer routing is separate from learner routing — the app detects role from JWT and shows the appropriate dashboard.
