# Chapter 03 — Admin Endpoints

## Base Path: `/admin`

Admin endpoints are accessible only to users with `gods_admin` or `compliance` roles. They provide platform-level control and visibility.

---

## User Management

### `GET /admin/users`

List all users across all tenants.

**Required role:** `gods_admin`

**Query parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `tenant_id` | UUID | Filter by tenant |
| `role` | string | Filter by role name |
| `status` | string | `active` \| `suspended` \| `deleted` |
| `page` | int | Page number (default: 1) |
| `page_size` | int | Results per page (default: 50, max: 200) |

**Response:** `200 OK`
```json
{
  "users": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "display_name": "Firstname Lastname",
      "tenant_id": "uuid",
      "roles": ["compliance"],
      "status": "active",
      "created_at": "2025-01-01T00:00:00Z",
      "last_login_at": "2025-01-15T08:30:00Z"
    }
  ],
  "total": 1543,
  "page": 1,
  "page_size": 50
}
```

---

### `POST /admin/users/{user_id}/suspend`

Suspend a user account.

**Required role:** `gods_admin`

**Request body:**
```json
{
  "reason": "string (required)",
  "suspend_until": "2025-02-01T00:00:00Z (optional — null = indefinite)"
}
```

**Response:** `200 OK` — Updated user record  
**Audit:** `AUTH.USER_SUSPENDED`

---

### `POST /admin/users/{user_id}/roles`

Assign a role to a user.

**Required role:** `gods_admin` or `division_admin` (for within-division roles only)

**Request body:**
```json
{
  "role_name": "compliance",
  "scope": {
    "tenant_id": "uuid (optional)",
    "division": "seths (optional)"
  },
  "expires_at": "2026-01-01T00:00:00Z (optional — required for external_auditor)"
}
```

**Response:** `201 Created`  
**Audit:** `AUTH.ROLE_ASSIGNED`

---

### `DELETE /admin/users/{user_id}/roles/{role_name}`

Revoke a role from a user.

**Required role:** `gods_admin` or `division_admin`

**Query parameters:** `reason` (required)

**Response:** `200 OK`  
**Audit:** `AUTH.ROLE_REVOKED`

---

## Tenant Management

### `GET /admin/tenants`

**Required role:** `gods_admin`

Returns all tenants with their configuration and status.

---

### `POST /admin/tenants`

Create a new tenant.

**Required role:** `gods_admin`

**Request body:**
```json
{
  "tenant_name": "Acme Corp",
  "tenant_code": "acme",
  "plan_tier": "professional",
  "default_jurisdiction": "ZA"
}
```

**Response:** `201 Created` — New tenant record with ID

---

## System Operations

### `POST /admin/policy-cache/refresh`

Force a PolicyPack cache refresh across all platform-core instances.

**Required role:** `gods_admin`

**Response:** `200 OK` — `{"status": "refresh_triggered", "instances_notified": 3}`

---

### `GET /admin/system-health`

Full system health report including all service dependencies.

**Required role:** `gods_admin`, `compliance`

**Response:** `200 OK` — Extended health report with all service checks, version info, and recent error counts.

---

### `POST /admin/audit-chain/verify`

Trigger an audit chain integrity verification job.

**Required role:** `gods_admin`

**Request body:**
```json
{
  "from_date": "2025-01-01",
  "to_date": "2025-01-31"
}
```

**Response:** `202 Accepted`
```json
{
  "job_id": "uuid",
  "status": "running",
  "estimated_duration_seconds": 120
}
```

Poll `GET /admin/audit-chain/verify/{job_id}` for status. When complete, the report is available at `GET /admin/audit-chain/reports/{report_id}`.

---

### `GET /admin/governance-sign-off`

Current production readiness sign-off status.

**Required role:** `gods_admin`, `compliance`

**Response:** `200 OK`
```json
{
  "signed_off": true,
  "signed_off_by": "uuid",
  "signed_off_at": "2025-01-15T09:00:00Z",
  "smoke_tests_passed": 31,
  "constitutional_tests_passed": 11,
  "platform_version": "2.1.0"
}
```
