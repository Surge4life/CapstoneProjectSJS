# Chapter 07 — Commits 041–050: TS Industries Division

## Overview

This batch implements the TS Industries division — project submission, industrial pipeline management, and partner management for SPVs and government project offices.

---

## Commit 041: `[DB] MIGRATE: Add TS schemas — projects, sectors, partners`

**What:**
- `ts.projects` — industrial project records
- `ts.sectors` — sector registry (energy, infrastructure, manufacturing, agriculture, technology, etc.)
- `ts.partners` — build assistant partner registry
- `ts.project_partners` — project-partner assignments
- `ts.project_documents` — project documentation (linked to document store)

---

## Commit 042: `[CORE] ADD: TS project service`

**What:**
- `create_ts_project()` — project submission with governance pre-check
- `update_project()` — status and detail updates
- `assign_partner()` — assign a build assistant partner to a project
- `get_project()` — full project record
- `list_projects()` — pipeline view

The GBS pre-check for TS projects evaluates:
- Jurisdictional compliance for the project location (SC dimension)
- Societal impact of the industrial project (SI dimension)
- Fairness of partner selection criteria (FA dimension)

---

## Commit 043: `[CORE] ADD: TS sector management service`

**What:**
- `get_sectors()` — sector list with requirements
- `get_sector_requirements()` — governance requirements by sector
- Sector-specific EVA weight overrides (e.g., energy sector has elevated RC weight due to regulatory complexity)
- Sector policy packs (each sector can have customised PolicyPack rules)

---

## Commit 044: `[CORE] ADD: TS partner service`

**What:**
- `register_partner()` — partner registration and verification
- `verify_partner()` — compliance verification (B-BBEE status, CIPC registration, sector qualifications)
- `get_partner_profile()` — partner capability profile
- `match_partners_to_project()` — intelligence-powered partner matching

Partner matching uses G.O.D.S Intelligence to match project requirements against partner capability profiles in the corpus.

---

## Commit 045: `[DB] MIGRATE: Add TS compliance and governance tables`

**What:**
- `ts.governance_decisions` — TS-specific governance decision tracking
- `ts.compliance_reviews` — compliance review records for projects
- `ts.partner_certifications` — partner certification tracking

---

## Commit 046: `[CORE] ADD: TS API router`

**What:** `platform-core/app/routers/ts.py`:
- `/ts/projects/*`
- `/ts/sectors/*`
- `/ts/partners/*`

---

## Commit 047: `[UI] ADD: TS web application`

**What:** `ts-app/` — SPV and government project office PWA:
- Connect screen + login
- Dashboard: active projects, milestones, partner assignments
- Projects: submit, view, and track industrial projects
- Partners: browse certified partners, initiate engagement
- Sectors: sector information, requirements, and governance standards
- Reports: project pipeline summary

---

## Commit 048: `[UI] ADD: TS admin console section`

**What:** TS section in `platform-web`:
- Full project pipeline management
- Partner registry management
- Compliance review interface
- Sector configuration
- TS division metrics

---

## Commit 049: `[CORE] ADD: TS reporting service`

**What:**
- Project pipeline by sector and status
- Partner utilisation metrics
- Governance compliance rate
- Project completion rate by sector
- Government project office-specific reporting views

---

## Commit 050: `[TEST] ADD: TS integration tests`

**What:**
- Project creation and lifecycle
- Partner assignment with governance check
- Sector policy pack application
- RBAC enforcement
- End-to-end governance audit trail

`tests/test_ts_integration.py` — 20 test cases
