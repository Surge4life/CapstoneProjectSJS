# Chapter 02 — Authentication Endpoints

## Endpoint Summary

| Method | Path | Auth Required | Description |
|--------|------|--------------|-------------|
| `POST` | `/auth/login` | No | Authenticate and get tokens |
| `POST` | `/auth/refresh` | No (refresh token) | Refresh access token |
| `POST` | `/auth/logout` | Yes | Revoke current session |
| `GET` | `/auth/me` | Yes | Get current user identity |
| `POST` | `/auth/change-password` | Yes | Change own password |

---

## POST /auth/login

Authenticates a user with email and password. Returns a JWT access token and a refresh token.

**Request:**
```json
{
  "email": "user@institution.co.za",
  "password": "string"
}
```

**Response 200:**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6InYxIn0...",
    "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 28800,
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@institution.co.za",
      "full_name": "Firstname Lastname",
      "roles": ["operator"],
      "division": "udoc",
      "jurisdiction": "ZA"
    }
  }
}
```

**Errors:**

| Code | Condition |
|------|---------|
| `INVALID_CREDENTIALS` | Wrong email or password |
| `ACCOUNT_SUSPENDED` | Account is suspended |
| `RATE_LIMITED` | More than 10 failed attempts in 15 minutes from this IP |

**Audit:** Every login attempt (success or failure) is recorded in the audit chain with email, IP address, outcome, and timestamp.

---

## POST /auth/refresh

Issues a new access token and refresh token. The provided refresh token is immediately invalidated (single-use).

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response 200:** Same as login response.

**Errors:**

| Code | Condition |
|------|---------|
| `INVALID_TOKEN` | Refresh token malformed or signature invalid |
| `TOKEN_EXPIRED` | Refresh token past 30-day expiry |
| `TOKEN_REVOKED` | Refresh token already used or explicitly revoked |

---

## POST /auth/logout

Revokes the current access token and the corresponding refresh token.

**Headers:** `Authorization: Bearer <access_token>`

**Response 200:**
```json
{
  "data": {
    "message": "Logged out successfully",
    "revoked_at": "2025-01-15T10:30:00Z"
  }
}
```

**What happens:**
1. Token `jti` added to Redis blacklist (immediate effect, before response is sent)
2. Refresh token invalidated in database
3. Logout event written to audit chain

---

## GET /auth/me

Returns the current authenticated user's complete identity and permission context.

**Headers:** `Authorization: Bearer <access_token>`

**Response 200:**
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@institution.co.za",
    "full_name": "Firstname Lastname",
    "roles": ["operator"],
    "permissions": [
      "models:register",
      "models:view_own",
      "decisions:view_own",
      "audit:view_own"
    ],
    "division": "udoc",
    "jurisdiction": "ZA",
    "tenant_id": "uuid",
    "last_login": "2025-01-15T09:00:00Z",
    "session_expires": "2025-01-15T17:00:00Z"
  }
}
```

---

## POST /auth/change-password

Changes the authenticated user's password. Requires the current password for verification.

**Headers:** `Authorization: Bearer <access_token>`

**Request:**
```json
{
  "current_password": "string",
  "new_password": "string",
  "confirm_password": "string"
}
```

**Password requirements:**
- Minimum 12 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

**Response 200:**
```json
{
  "data": {
    "message": "Password changed successfully",
    "all_sessions_revoked": true
  }
}
```

On password change, **all active sessions are revoked** — the user must log in again on all devices. This is not optional. The security requirement takes precedence over convenience.

**Audit:** Password change (not the password itself) is recorded in the audit chain.
