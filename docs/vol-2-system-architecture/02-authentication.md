# Chapter 02 — Authentication Service

## Purpose

The Authentication Service is the identity foundation of the G.O.D.S ecosystem. Every API request (except health checks and the login endpoint) must carry a valid JWT token issued by this service. The token establishes the caller's identity, their roles, and their jurisdiction context.

---

## Location

- **Router:** `platform-core/app/routers/auth.py`
- **Schema:** `platform-core/app/schemas/auth.py`
- **Security utilities:** `platform-core/app/core/security.py`
- **Dependencies:** `platform-core/app/core/dependencies.py`

---

## Endpoints

### POST /auth/login

Authenticates a user with email and password. Returns an access token and refresh token.

**Request:**
```json
{
  "email": "operator@institution.co.za",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 28800,
  "user": {
    "id": "uuid",
    "email": "operator@institution.co.za",
    "roles": ["operator"],
    "division": "udoc",
    "jurisdiction": "ZA"
  }
}
```

**Errors:**
- `401 INVALID_CREDENTIALS` — Wrong email or password
- `403 ACCOUNT_SUSPENDED` — Account is suspended by admin action
- `429 RATE_LIMITED` — Too many failed attempts (5 in 15 minutes)

---

### POST /auth/refresh

Issues a new access token using a valid refresh token. The refresh token is single-use — a new refresh token is issued with each refresh.

**Request:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response:** Same as `/auth/login`

---

### POST /auth/logout

Revokes the current access token (adds to Redis blacklist) and invalidates the refresh token.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "message": "Logged out successfully",
  "revoked_at": "2025-01-15T10:30:00Z"
}
```

---

### GET /auth/me

Returns the current user's identity and role context.

**Response:**
```json
{
  "id": "uuid",
  "email": "string",
  "roles": ["string"],
  "division": "string | null",
  "jurisdiction": "string",
  "last_login": "datetime",
  "session_expires": "datetime"
}
```

---

## Token Architecture

### Access Token Claims (JWT Payload)
```json
{
  "sub": "user-uuid",
  "email": "user@email.com",
  "roles": ["role1", "role2"],
  "division": "seths",
  "jurisdiction": "ZA",
  "iat": 1705316400,
  "exp": 1705345200,
  "jti": "unique-token-id",
  "kid": "key-rotation-id"
}
```

### Token Validation Sequence
1. Extract `Authorization: Bearer <token>` header
2. Decode JWT header — extract `kid`
3. Fetch public key matching `kid` from key service
4. Verify JWT signature
5. Check `exp` — reject if expired
6. Check `jti` against Redis blacklist — reject if revoked
7. Load user from database by `sub`
8. Check user status — reject if suspended
9. Return validated user object

This validation happens in `platform-core/app/core/dependencies.py` via `get_current_user()`.

---

## Audit Trail

Every login, logout, token refresh, and failed authentication attempt is written to the audit chain with:
- User identity (or attempted identity)
- IP address
- Timestamp
- Outcome
- Failure reason (if applicable)

Authentication audit records cannot be deleted or modified.
