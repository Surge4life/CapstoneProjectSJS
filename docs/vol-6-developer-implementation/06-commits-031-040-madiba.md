# Chapter 06 — Commits 031–040: MADIBA Division Foundation

## Overview

This batch builds the MADIBA (investment and capital management) division. MADIBA manages the capital pipeline, milestone tracking, and institutional investor engagement.

---

## Commit 031: `[DB] MIGRATE: Add MADIBA schemas — projects, milestones, investors`

**What:** Core MADIBA database tables:
- `madiba.projects` — capital pipeline projects with governance fields
- `madiba.milestones` — project milestones with completion tracking
- `madiba.investors` — institutional investor registry
- `madiba.capital_allocations` — capital assignment records
- `madiba.project_updates` — project progress updates (immutable log)

---

## Commit 032: `[CORE] ADD: MADIBA project service`

**What:** Project lifecycle management:
- `create_project()` — project submission with governance pre-check
- `update_project_status()` — status transitions through governance path
- `get_project()` — full project record
- `list_projects()` — pipeline view with filtering

Project creation GBS pre-check evaluates:
- Project alignment with constitutionally permissible economic development (SI dimension)
- Operator history (operator_history → EC dimension)
- Jurisdiction validity (SC dimension)

---

## Commit 033: `[CORE] ADD: MADIBA milestone service`

**What:** Milestone tracking:
- `create_milestone()` — define project milestones with criteria
- `record_completion()` — milestone completion with evidence upload
- `get_milestone_status()` — current status with history
- Automated notification to investors when milestones are completed

---

## Commit 034: `[CORE] ADD: MADIBA investor service — registry and capital allocation`

**What:**
- `register_investor()` — institutional investor registration
- `allocate_capital()` — capital assignment to projects
- `get_allocation_record()` — full allocation record
- `generate_investor_report()` — capital deployment and impact report

All capital allocations are governance events — submitted to the GBS path before finalisation.

---

## Commit 035: `[DB] MIGRATE: Add MADIBA governance tracking tables`

**What:**
- `madiba.governance_reviews` — records of governance decisions on MADIBA events
- `madiba.compliance_flags` — flags raised during compliance monitoring
- Indexes for compliance dashboard queries

---

## Commit 036: `[CORE] ADD: MADIBA API router`

**What:** `platform-core/app/routers/madiba.py`:
- `/madiba/projects/*`
- `/madiba/milestones/*`
- `/madiba/investors/*`
- `/madiba/allocations/*`

Role-based access: `investor` role for own records; `division_admin` for all.

---

## Commit 037: `[UI] ADD: MADIBA web application`

**What:** `madiba-app/` — investor-facing web PWA:
- Connect screen + login/registration
- Dashboard: capital pipeline overview, active milestones
- Projects: browse and view project details
- Milestones: track completion across portfolio
- Reports: capital deployment summary

---

## Commit 038: `[UI] ADD: MADIBA admin console section`

**What:** MADIBA section in `platform-web`:
- Full project pipeline management
- Investor management
- Compliance flag review
- Capital allocation oversight
- MADIBA division metrics dashboard

---

## Commit 039: `[CORE] ADD: MADIBA analytics service`

**What:**
- Capital pipeline metrics (total capital, deployed, committed, returned)
- Project success rate by sector
- Milestone completion rate
- Investor engagement metrics
- Integration with the reporting engine for quarterly MADIBA reports

---

## Commit 040: `[TEST] ADD: MADIBA integration tests`

**What:** Full end-to-end tests for the MADIBA division:
- Project creation → milestone tracking → completion
- Capital allocation → investor reporting
- GBS governance path for MADIBA events
- RBAC enforcement for investor vs admin roles
- Governance decision audit trail integrity

`tests/test_madiba_integration.py` — 25 test cases
