# Chapter 06 — G.O.D.S Admin Console

## Overview

The G.O.D.S Admin Console (`platform-web`) is the sovereign-operator mainframe. It provides full control of the entire ecosystem from a single, password-protected browser interface. It is the only application in the G.O.D.S ecosystem that has no mobile counterpart — it is browser-only, by design.

**Who uses it:** G.O.D.S administrators, governance officers, compliance officers. Not operators. Not learners. Not employers. This is the control plane.

---

## Information Architecture

```
G.O.D.S Admin Console
├── Dashboard (overview of all four divisions + governance health)
├── UDOC Console
│   ├── Model Registry (all registered models, status, metrics)
│   ├── Governance Decisions (live feed + historical)
│   ├── Oversight Cases (open, assigned, resolved)
│   ├── Edge Nodes (status, connectivity, registry sync)
│   └── Operator Accounts
├── SETHS Console
│   ├── Learner Overview
│   ├── Employer Overview
│   ├── Applications Pipeline
│   ├── Document Audit
│   └── Employment Equity Metrics
├── MADIBA Console
│   ├── Capital Pipeline
│   ├── Institutional Milestones
│   └── Investor Registry
├── TS Console
│   ├── Project Pipeline
│   ├── SPV Registry
│   └── Partner Applications
├── Compliance
│   ├── GBS Rule Engine (view/edit PolicyPacks)
│   ├── Conformance Scans
│   ├── Bias Reports
│   └── Regulatory Reports
├── Intelligence
│   ├── Corpus Management
│   ├── Query Logs
│   └── Calibration Reports
├── Administration
│   ├── Users & Roles
│   ├── Tenant Management
│   ├── System Configuration
│   └── Audit Explorer
└── Infrastructure (health, metrics, logs)
```

---

## The Dashboard

The admin dashboard provides a real-time overview of governance health across the ecosystem. Layout:

### Top Bar: System Health
A persistent top bar showing the status of all core services:
- `platform-core` health (green/amber/red)
- Governance engine health
- Database connectivity
- Kafka connectivity
- Audit chain status (is the chain healthy and up-to-date?)

### Four Division Tiles
Each division has a summary tile showing:
- Active records count
- Today's governance decisions (approved/reviewed/escalated/blocked)
- Open oversight cases count (with overdue count highlighted in red)
- 7-day trend sparkline

### Governance Activity Feed
A live feed of governance decisions as they happen (WebSocket-based, real-time):
- Model name
- Outcome badge (colour-coded)
- Jurisdiction
- Governance latency
- Click-through to full decision record

### Critical Alerts Panel
Any item requiring immediate attention:
- Overdue oversight cases (past SLA)
- Model suspensions in the last 24 hours
- Governance path errors
- Audit chain anomalies

---

## UDOC Console Detail

### Model Registry View

A filterable, sortable table of all registered AI models:

| Column | Description |
|--------|-------------|
| Model Name | With version tag |
| Operator | Linked to operator profile |
| Status | Colour-coded badge |
| Jurisdiction | Flag + code |
| Requests Today | Count with trend arrow |
| Block Rate | 7-day block rate % |
| Last Decision | Timestamp |
| Actions | Certify / Suspend / View |

**Bulk actions:** Select multiple models → suspend, export metrics, generate compliance report.

### Decision Inspector

Clicking any decision record opens the Decision Inspector panel:
- Full EVA score breakdown (hexagon radar chart for the 6 dimensions)
- Reasoning text (the human-readable explanation)
- Input/output hashes
- Governance path timing breakdown
- Cryptographic seal verification status
- Related oversight case (if applicable)
- Lineage trail (this decision in the audit chain)

---

## Oversight Case Management

The oversight case management interface is designed for efficiency — compliance officers may have dozens of open cases.

### Case Queue

Filterable list of cases with priority indicators:
- `CRITICAL` — system impact, requires same-day resolution
- `HIGH` — individual impact, SLA < 1 day remaining
- `STANDARD` — normal SLA
- `OVERDUE` — SLA breached (red, always shown at top)

### Case Detail View

When a reviewer opens a case:
1. **Summary:** What was blocked, and why (EVA score breakdown + reasoning)
2. **Subject information:** Who was affected (with appropriate redactions based on reviewer's scope)
3. **Original decision record:** Full decision with seal verification
4. **Evidence panel:** Any additional information the subject has provided
5. **Action panel:** Confirm / Override / Escalate / Request More Info
6. **Audit trail:** Full history of this case

**Confirming a decision:** Requires the reviewer to write a reasoning note (minimum 50 characters). One-click confirmations are not permitted for oversight cases.

**Overriding a decision:** Requires extended reasoning (minimum 200 characters) + evidence references. The override is recorded with the reviewer's identity and is subject to a second-level audit.

---

## Corpus Management (Intelligence Section)

The admin corpus management interface:

- **Document library:** All documents in the corpus, with tier, upload date, uploader, and usage count
- **Upload interface:** Drag-and-drop upload with tier selection, source URL field, and description
- **Chunk preview:** After upload, shows how the document was chunked and embedded
- **Usage analytics:** Which documents are being retrieved most often in intelligence queries
- **Outdated document alerts:** Documents that have a newer version available (detected by title similarity)
- **Tier audit:** Compliance report of documents by tier, with upload authority verification
