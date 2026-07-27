# Chapter 14 — Error Reference

## Error Response Format

All G.O.D.S API errors follow a consistent JSON structure:

```json
{
  "error": {
    "code": "MODEL_NOT_REGISTERED",
    "message": "The requested model (uuid) is not registered with UDOC.",
    "details": {
      "model_id": "uuid",
      "suggestion": "Register the model at POST /registry/models before submitting governance requests."
    },
    "request_id": "uuid",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

---

## HTTP Status Codes

| Status | Meaning | Common Causes |
|--------|---------|--------------|
| `200 OK` | Success | — |
| `201 Created` | Resource created | POST to create endpoints |
| `202 Accepted` | Async operation started | Report generation, exports |
| `400 Bad Request` | Invalid input | Missing required fields, invalid format |
| `401 Unauthorized` | Not authenticated | Missing/expired JWT |
| `403 Forbidden` | Not authorised | RBAC permission denied |
| `404 Not Found` | Resource not found | Invalid UUID |
| `409 Conflict` | State conflict | Duplicate `request_id`, invalid state transition |
| `422 Unprocessable Entity` | Business rule violation | Model in sanctioned state |
| `429 Too Many Requests` | Rate limit exceeded | — |
| `500 Internal Server Error` | Unexpected server error | Bug or infrastructure failure |
| `503 Service Unavailable` | Dependency unavailable | Governance engine down (fail-closed) |

---

## Error Codes Reference

### Authentication Errors (4xx)

| Code | HTTP | Description |
|------|------|-------------|
| `TOKEN_EXPIRED` | 401 | JWT access token has expired — use refresh token |
| `TOKEN_INVALID` | 401 | JWT signature invalid or malformed |
| `TOKEN_REVOKED` | 401 | Token has been explicitly revoked |
| `REFRESH_TOKEN_INVALID` | 401 | Refresh token invalid — re-authenticate |
| `INSUFFICIENT_PERMISSIONS` | 403 | User lacks required RBAC permission |
| `TENANT_MISMATCH` | 403 | Resource belongs to different tenant |
| `SESSION_EXPIRED` | 401 | Admin session timeout |

### Governance Errors (422, 503)

| Code | HTTP | Description |
|------|------|-------------|
| `MODEL_NOT_REGISTERED` | 422 | Model not in UDOC registry |
| `MODEL_SUSPENDED` | 422 | Model is in `suspended` state |
| `MODEL_REVOKED` | 422 | Model is permanently `revoked` |
| `MODEL_EXPIRED` | 422 | Model certification has expired |
| `MODEL_PENDING_REVIEW` | 422 | Model registration not yet approved |
| `JURISDICTION_MISMATCH` | 422 | Request jurisdiction ≠ declared jurisdiction |
| `GOVERNANCE_TIMEOUT` | 503 | Governance engine unavailable (fail-closed BLOCK) |
| `UDOC_UNAVAILABLE` | 503 | UDOC enforcement engine unavailable |
| `AUDIT_WRITE_FAILURE` | 503 | Audit chain write failed — governance cannot proceed |
| `SEAL_UNAVAILABLE` | 503 | HMAC key service unavailable |
| `CONSTITUTIONAL_VIOLATION` | 422 | Request violates a constitutional check |
| `DUPLICATE_REQUEST_ID` | 409 | `request_id` already exists (returns original decision) |
| `POLICY_DEGRADED` | 503 | PolicyPack unavailable — operating in conservative mode |

### Resource Errors (400, 404, 409)

| Code | HTTP | Description |
|------|------|-------------|
| `RESOURCE_NOT_FOUND` | 404 | UUID does not match any record |
| `VALIDATION_ERROR` | 400 | Request body fails schema validation |
| `INVALID_STATE_TRANSITION` | 409 | FSM transition is not valid from current state |
| `POLICY_PACK_NOT_DRAFT` | 409 | Only draft packs can be modified |
| `POLICY_PACK_NOT_IN_REVIEW` | 409 | Only review-status packs can be activated |
| `DOCUMENT_INTEGRITY_FAILURE` | 422 | Document SHA-256 mismatch on retrieval |
| `CORPUS_DOCUMENT_NOT_INDEXED` | 422 | Document is not yet available for querying |
| `OPPORTUNITY_CLOSED` | 409 | Cannot apply to a closed opportunity |
| `DUPLICATE_APPLICATION` | 409 | Learner has already applied to this opportunity |

### Rate Limiting Errors (429)

| Code | HTTP | Description |
|------|------|-------------|
| `RATE_LIMIT_EXCEEDED` | 429 | Request rate exceeded |
| `AUTH_RATE_LIMIT` | 429 | Authentication attempt rate exceeded |
| `GOVERNANCE_RATE_LIMIT` | 429 | Governance request rate exceeded |

**Rate limit response headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705312200
Retry-After: 60
```

---

## Intelligence-Specific Errors

| Code | HTTP | Description |
|------|------|-------------|
| `CONSTITUTIONAL_REFUSAL` | 200* | Query refused — constitutional limit (*200 with `refused: true` in body) |
| `CORPUS_EMPTY` | 422 | Tenant corpus has no documents — cannot query |
| `EXTERNAL_CONSULTATION_DISABLED` | 422 | External consultation not enabled for this deployment |
| `EXTERNAL_CONSULTATION_SANITISATION_FAILED` | 422 | PII could not be removed from query for external consultation |
| `QUERY_TOO_LONG` | 400 | Query exceeds 2000 character limit |
| `SESSION_NOT_FOUND` | 404 | Session ID not found or expired |

---

## Handling Governance Fail-Closed Errors

When `GOVERNANCE_TIMEOUT`, `UDOC_UNAVAILABLE`, or `AUDIT_WRITE_FAILURE` are returned:

1. **Do not proceed with the action** — the fail-closed response means governance could not be completed
2. **Log the error** with the full `request_id` — this allows G.O.D.S support to locate the failed governance request
3. **Retry after delay** — these errors are typically transient; retry after 30 seconds
4. **Inform the subject** — the person or system whose action was blocked should be informed that a temporary technical issue prevented governance, and they may retry

For persistent `503` errors (> 5 minutes), contact G.O.D.S operations — the governance engine may be in a planned maintenance window.
