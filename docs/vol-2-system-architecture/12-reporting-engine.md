# Chapter 12 — Reporting Engine

## Purpose

The Reporting Engine generates structured reports for compliance officers, administrators, government bodies, and clients. Every report is generated from the audit chain and operational database — never from estimates or approximations.

---

## Location

- **Router:** `platform-core/app/routers/analytics.py` (report generation endpoints)
- **Service:** `platform-core/app/services/analytics_engine.py`
- Scheduled reports managed by APScheduler

---

## Report Types

### Governance Report

A periodic summary of all governance decisions within a scope (tenant, division, time range).

**Contents:**
- Total decisions: count by outcome (APPROVE, REVIEW, ESCALATE, BLOCK)
- Decision distribution by model
- Average EVA scores by dimension
- Top BLOCK reasons
- Oversight case resolution rate and average resolution time
- SLA compliance rate
- PolicyPack version in effect during the period

**Audiences:** Compliance officers, clients, regulators  
**Schedule:** Monthly (automated), on-demand via API  
**Format:** PDF + JSON

---

### Employment Equity Report (SETHS)

Generated for registered employers and for the SETHS division overview.

**Contents:**
- Applicant pool demographics by opportunity (where declared)
- Shortlisting rate by demographic group
- Hire rate by demographic group
- Bias detection flags during the period
- Comparison to national employment equity benchmarks (where available)
- Year-on-year trend (if historical data available)

**Audiences:** Employers (own data), compliance officers (all employers), government labour bodies  
**Regulatory basis:** Employment Equity Act (No. 55 of 1998), Chapter III

---

### Audit Chain Integrity Report

Verifies the integrity of the audit chain for a specified period.

**Contents:**
- Date range covered
- Total records in range
- Hash chain verification result (VERIFIED or BROKEN — with break location if broken)
- Merkle root for each day in the range
- HMAC seal verification status for sampled records
- Any anomalies detected

**Audiences:** External auditors, compliance officers, gods_admin  
**Schedule:** Weekly (automated), on-demand  
**This report cannot be generated without triggering a fresh chain verification** — it is not a cached summary.

---

### Client SaaS Usage Report

For UDOC SaaS clients, a usage and billing report.

**Contents:**
- Total governance requests in period
- Breakdown by model and outcome
- Average governance latency
- Suspension events (if any)
- New model registrations
- Policy compliance score trend

**Audiences:** SaaS client operators  
**Schedule:** Monthly (automated for billing)

---

## Report Generation API

```
POST /analytics/reports/generate
{
    "report_type": "governance_summary",
    "scope": {
        "tenant_id": "uuid",          -- optional: if gods_admin, can be any tenant
        "division": "seths",          -- optional
        "from_date": "2025-01-01",
        "to_date": "2025-03-31"
    },
    "format": "pdf"                   -- pdf | json | csv
}
```

**Response:**
```json
{
    "report_id": "uuid",
    "status": "generating",
    "estimated_ready_in_seconds": 30
}
```

Reports are generated asynchronously (may take 5–60 seconds depending on data volume). Poll `GET /analytics/reports/{report_id}` for status. When `status: "ready"`, the `download_url` field contains a signed URL valid for 24 hours.

---

## Scheduled Reports

The APScheduler configuration includes:

| Report | Schedule | Recipients |
|--------|----------|-----------|
| Governance summary | 1st of each month, 06:00 | All division admins, compliance |
| Employment equity | Last day of quarter, 06:00 | SETHS division admin, compliance |
| Audit chain integrity | Every Sunday, 02:00 | gods_admin |
| SaaS usage | 1st of each month, 07:00 | Each SaaS client operator |

All scheduled reports are stored in the database and accessible via the admin console. They are never emailed directly — the notification system sends a link to the report.
