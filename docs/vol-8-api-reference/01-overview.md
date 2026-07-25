# Chapter 01 — API Overview, Versioning & Authentication

## Base URLs

| Environment | Base URL |
|------------|---------|
| Local development | `http://localhost:8000` |
| Render production | `https://gods-platform-core.onrender.com` |
| Air-gapped / LAN | Configured at deployment — no hardcoded URL |

---

## API Conventions

### HTTP Methods

| Method | Usage |
|--------|-------|
| `GET` | Retrieve a resource or list. Never modifies state. |
| `POST` | Create a resource or trigger an action. |
| `PATCH` | Update a resource (partial update). |
| `DELETE` | Soft-delete a resource. Does not physically remove data. |

`PUT` is not used. All updates are `PATCH`.

### Response Format

All responses are JSON. Successful responses have this envelope:

```json
{
  "data": { ... },
  "meta": {
    "request_id": "uuid",
    "timestamp": "datetime",
    "api_version": "1"
  }
}
```

Error responses:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": { ... },
    "request_id": "uuid"
  }
}
```

### Pagination

List endpoints support cursor-based pagination:

```
GET /seths/learners?limit=50&cursor=opaque-cursor-string
```

Response includes:
```json
{
  "data": [ ... ],
  "pagination": {
    "next_cursor": "next-opaque-cursor",
    "has_more": true,
    "total_count": 1234
  }
}
```

### Filtering

List endpoints support field-based filtering via query parameters:

```
GET /governance/decisions?outcome=BLOCK&jurisdiction=ZA&from=2025-01-01&to=2025-12-31
```

### Sorting

```
GET /seths/learners?sort=created_at:desc,full_name:asc
```

---

## Authentication

All endpoints except `/health` and `/auth/login` require Bearer JWT authentication:

```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InYxIn0...
```

Token acquisition: `POST /auth/login`

Token refresh: `POST /auth/refresh`

Token expiry: 8 hours (configurable per deployment, minimum 1 hour)

---

## Error Codes Reference

### Authentication Errors (4xx)

| Code | HTTP Status | Meaning |
|------|------------|---------|
| `AUTHENTICATION_REQUIRED` | 401 | No token provided |
| `INVALID_TOKEN` | 401 | Token malformed or signature invalid |
| `TOKEN_EXPIRED` | 401 | Token past expiry timestamp |
| `TOKEN_REVOKED` | 401 | Token has been revoked (logged out) |
| `INVALID_CREDENTIALS` | 401 | Wrong email or password |
| `ACCOUNT_SUSPENDED` | 403 | Account suspended by admin |
| `INSUFFICIENT_PERMISSIONS` | 403 | Authenticated but lacks required role/permission |
| `RATE_LIMITED` | 429 | Too many requests |

### Resource Errors (4xx)

| Code | HTTP Status | Meaning |
|------|------------|---------|
| `RESOURCE_NOT_FOUND` | 404 | The requested resource does not exist |
| `RESOURCE_DELETED` | 404 | Resource exists but has been soft-deleted |
| `VALIDATION_ERROR` | 422 | Request body failed validation |
| `CONFLICT` | 409 | Resource already exists (unique constraint) |
| `CROSS_TENANT_ACCESS` | 403 | Attempt to access another tenant's resource |

### Governance Errors (4xx/5xx)

| Code | HTTP Status | Meaning |
|------|------------|---------|
| `MODEL_NOT_REGISTERED` | 422 | AI model is not registered in the UDOC registry |
| `MODEL_SUSPENDED` | 403 | AI model is currently suspended |
| `MODEL_NOT_CERTIFIED` | 403 | AI model has not been certified |
| `GOVERNANCE_BLOCK` | 403 | GBS Runtime blocked this request |
| `JURISDICTION_MISMATCH` | 403 | Request jurisdiction does not match deployment |
| `GOVERNANCE_UNAVAILABLE` | 503 | Governance service unreachable — fail closed |

### System Errors (5xx)

| Code | HTTP Status | Meaning |
|------|------------|---------|
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `AUDIT_WRITE_FAILURE` | 500 | Failed to write audit record — critical |
| `DATABASE_UNAVAILABLE` | 503 | Database connection failed |

---

## Rate Limiting

All endpoints are rate-limited per authenticated user (or per IP for unauthenticated endpoints).

| Endpoint Class | Rate Limit |
|---------------|-----------|
| `/auth/login` | 10 requests per minute per IP |
| `/decisions/*` | 1000 requests per minute per operator |
| `/intelligence/*` | 100 requests per minute per user |
| All other endpoints | 500 requests per minute per user |

Rate limit headers are included in every response:

```http
X-RateLimit-Limit: 500
X-RateLimit-Remaining: 487
X-RateLimit-Reset: 1705316460
```

When rate limited, the response is `429 Too Many Requests` with a `Retry-After` header.
