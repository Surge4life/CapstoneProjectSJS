# Chapter 10 — Audit Endpoints

## Base Path: `/audit`

Audit endpoints provide read access to the governance audit chain. All read operations are themselves audited.

---

### `GET /audit/records`

Query audit records from the operational database (PostgreSQL — 7-year queryable window).

**Required role:** `compliance`, `gods_admin`, `external_auditor`

**Query parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `event_type` | string | Filter by event type (e.g., `GOVERNANCE.DECISION`) |
| `resource_type` | string | Filter by resource type |
| `resource_id` | UUID | Filter by specific resource |
| `actor_id` | UUID | Filter by actor |
| `from_date` | datetime | Start of range |
| `to_date` | datetime | End of range |
| `page` | int | Page number |
| `page_size` | int | Default: 100, max: 500 |

**Response:** `200 OK`
```json
{
  "records": [
    {
      "audit_ref_id": "uuid",
      "event_type": "GOVERNANCE.DECISION",
      "event_category": "GOVERNANCE",
      "resource_type": "Decision",
      "resource_id": "uuid",
      "actor_id": "uuid",
      "actor_role": "operator",
      "event_summary": {
        "outcome": "BLOCK",
        "model_id": "uuid",
        "eva_overall": 42
      },
      "ip_address": "192.168.1.1",
      "integrity_verified": true,
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "total": 45320,
  "page": 1,
  "page_size": 100
}
```

---

### `GET /audit/records/{audit_ref_id}`

Single audit record with full content.

**Response:** `200 OK` — Full `AuditRef` record including the HMAC seal and chain position

---

### `GET /audit/chain/verify`

Verify the integrity of the audit chain for a date range.

**Required role:** `gods_admin`, `external_auditor`

**Query parameters:** `from_date` (required), `to_date` (required)

**Response:** `200 OK`
```json
{
  "verification_id": "uuid",
  "from_date": "2025-01-01",
  "to_date": "2025-01-31",
  "status": "verified | anomaly_detected",
  "records_verified": 14823,
  "chain_intact": true,
  "merkle_roots": [
    {"date": "2025-01-01", "root": "sha256:...", "records": 487},
    {"date": "2025-01-02", "root": "sha256:...", "records": 512}
  ],
  "anomalies": [],
  "verified_at": "2025-01-15T12:00:00Z",
  "verified_by": "uuid"
}
```

If `chain_intact: false`, the `anomalies` array contains the specific records where the chain breaks.

---

### `GET /audit/chain/merkle-roots`

Retrieve daily Merkle roots for a date range.

**Required role:** `compliance`, `gods_admin`, `external_auditor`

**Query parameters:** `from_date`, `to_date`

**Response:** `200 OK` — Array of `{date, merkle_root, record_count}` objects

These Merkle roots can be independently verified against the Cassandra audit chain.

---

### `GET /audit/records/export`

Export audit records for an external audit.

**Required role:** `gods_admin`, `external_auditor`

**Query parameters:** `from_date` (required), `to_date` (required), `format` (`json` \| `csv`)

**Response:** `202 Accepted` — Export job started
```json
{
  "export_id": "uuid",
  "status": "generating",
  "estimated_size_mb": 45,
  "estimated_ready_in_seconds": 60
}
```

Poll `GET /audit/records/export/{export_id}` for status. When `status: "ready"`, the `download_url` is valid for 24 hours.

---

### `GET /audit/summary`

Aggregate audit statistics for a period.

**Required role:** `compliance`, `gods_admin`

**Query parameters:** `from_date`, `to_date`, `tenant_id` (optional)

**Response:** `200 OK`
```json
{
  "period": { "from": "2025-01-01", "to": "2025-01-31" },
  "totals": {
    "all_events": 48920,
    "governance_decisions": 14823,
    "auth_events": 12450,
    "data_change_events": 18300,
    "system_events": 3347
  },
  "governance_outcomes": {
    "APPROVE": 9834,
    "REVIEW": 3219,
    "ESCALATE": 847,
    "BLOCK": 923
  },
  "oversight_cases": {
    "opened": 1770,
    "resolved": 1694,
    "sla_breached": 12
  }
}
```
