# Chapter 12 — Analytics Endpoints

## Base Path: `/analytics`

Analytics endpoints expose governance metrics, bias detection data, and report generation for compliance and administrative users.

---

## Live Metrics

### `GET /analytics/governance-summary`

Real-time governance decision metrics.

**Required role:** `compliance`, `gods_admin`, `division_admin`

**Query parameters:** `from_date`, `to_date`, `tenant_id`, `division`

**Response:** `200 OK`
```json
{
  "period": { "from": "2025-01-01", "to": "2025-01-31" },
  "decisions": {
    "total": 14823,
    "by_outcome": { "APPROVE": 9834, "REVIEW": 3219, "ESCALATE": 847, "BLOCK": 923 },
    "block_rate": 0.062,
    "avg_governance_ms": 38,
    "p95_governance_ms": 74
  },
  "eva_averages": {
    "ec": 84.2, "si": 77.8, "rc": 88.6, "fa": 81.4, "cc": 79.1, "sc": 87.3, "overall": 82.9
  },
  "oversight": {
    "cases_opened": 1770,
    "cases_resolved": 1694,
    "avg_resolution_hours": 18.4,
    "sla_compliance_rate": 0.993,
    "sla_breaches": 12
  }
}
```

---

### `GET /analytics/governance-trend`

Governance metrics over time (for trend charts).

**Query parameters:** `from_date`, `to_date`, `granularity` (`day` \| `week` \| `month`)

**Response:** `200 OK` — Array of `{date, decisions, block_rate, avg_eva_overall}` data points

---

### `GET /analytics/top-blocks`

Most common BLOCK reasons in the period.

**Query parameters:** `from_date`, `to_date`, `limit` (default: 10)

**Response:**
```json
{
  "top_block_reasons": [
    { "reason_code": "FAIRNESS_THRESHOLD", "count": 312, "pct": 0.34 },
    { "reason_code": "POLICY_RULE_5", "count": 189, "pct": 0.20 }
  ]
}
```

---

### `GET /analytics/bias-scores`

Employer bias score overview.

**Required role:** `compliance`, `gods_admin`

**Response:** Aggregated bias score distribution across employers (no individual employer identified except to compliance)

---

### `GET /analytics/seths-pipeline`

SETHS division employment pipeline metrics.

**Required role:** `compliance`, `division_admin`, `gods_admin`

**Response:**
```json
{
  "period_summary": {
    "total_applications": 4832,
    "shortlisting_rate": 0.23,
    "offer_rate": 0.08,
    "acceptance_rate": 0.71
  },
  "equity_metrics": {
    "applications_by_province": { "Gauteng": 1823, "Western Cape": 912, "...": "..." },
    "nqf_level_distribution": { "3": 234, "4": 891, "5": 1203, "6": 1504, "7+": 1000 }
  }
}
```

---

## Reports

### `POST /analytics/reports/generate`

Generate a governance report.

**Required role:** `compliance`, `gods_admin`

**Request body:**
```json
{
  "report_type": "governance_summary | employment_equity | audit_chain_integrity | saas_usage",
  "scope": {
    "tenant_id": "uuid (optional)",
    "division": "seths (optional)",
    "from_date": "2025-01-01",
    "to_date": "2025-03-31"
  },
  "format": "pdf | json | csv"
}
```

**Response:** `202 Accepted`
```json
{
  "report_id": "uuid",
  "report_type": "governance_summary",
  "status": "generating",
  "estimated_ready_in_seconds": 30
}
```

---

### `GET /analytics/reports/{report_id}`

Check report generation status.

**Response:** `200 OK`
```json
{
  "report_id": "uuid",
  "status": "ready | generating | failed",
  "download_url": "https://...(signed URL, valid 24h)",
  "expires_at": "2025-01-16T12:00:00Z",
  "file_size_bytes": 248320
}
```

---

### `GET /analytics/reports`

List generated reports.

**Query parameters:** `report_type`, `from_date`, `to_date`, `status`

---

### `GET /analytics/model-performance/{model_id}`

Governance performance metrics for a specific AI model.

**Required role:** Model operator (own model) or `compliance`, `gods_admin`

**Response:**
```json
{
  "model_id": "uuid",
  "period": "30d",
  "total_decisions": 2847,
  "outcome_distribution": { "APPROVE": 0.71, "REVIEW": 0.18, "ESCALATE": 0.06, "BLOCK": 0.05 },
  "eva_trend": [
    { "date": "2025-01-01", "overall": 84.2, "fa": 82.1 }
  ],
  "block_trend": "stable",
  "governance_score": 84.2
}
```
