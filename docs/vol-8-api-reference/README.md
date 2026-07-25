# Volume VIII — API Reference
## Every Endpoint. Request. Response. Permissions. Errors. Examples.

> This volume is the complete API reference for the G.O.D.S platform-core. Every endpoint is documented with its HTTP method, path, authentication requirements, request schema, response schema, error codes, and a working example.

---

## Contents

| Chapter | Title |
|---------|-------|
| [01](01-overview.md) | API Overview, Versioning & Authentication |
| [02](02-auth-endpoints.md) | Authentication Endpoints (`/auth/*`) |
| [03](03-admin-endpoints.md) | Admin Endpoints (`/admin/*`) |
| [04](04-udoc-endpoints.md) | UDOC Endpoints (`/registry/*`, `/decisions/*`, `/udoc/*`) |
| [05](05-seths-endpoints.md) | SETHS Endpoints (`/seths/*`, `/workforce/*`) |
| [06](06-madiba-endpoints.md) | MADIBA Endpoints (`/madiba/*`) |
| [07](07-ts-endpoints.md) | TS Industries Endpoints (`/ts/*`) |
| [08](08-governance-endpoints.md) | Governance Endpoints (`/compliance/*`, `/bias/*`, `/sovereignty/*`) |
| [09](09-intelligence-endpoints.md) | Intelligence Endpoints (`/intelligence/*`, `/client-knowledge/*`) |
| [10](10-audit-endpoints.md) | Audit Endpoints (`/audit/*`, `/lineage/*`) |
| [11](11-portal-endpoints.md) | Portal Endpoints (`/portals/*`) |
| [12](12-analytics-endpoints.md) | Analytics Endpoints (`/analytics/*`) |
| [13](13-policy-endpoints.md) | Policy Endpoints (`/policy/*`) |
| [14](14-error-reference.md) | Error Reference |

---

## Base URL

| Environment | URL |
|------------|-----|
| Local development | `http://localhost:8000` |
| Render production | `https://gods-platform-core.onrender.com` |
| Air-gapped / LAN | Configured at connect screen |

## Authentication

All endpoints (except `/auth/login` and `/health`) require a Bearer JWT token:

```http
Authorization: Bearer <token>
```

Tokens are issued by the `/auth/login` endpoint, signed with the platform's RSA key pair, and expire after 8 hours by default. The `kid` (key ID) header in the JWT identifies which key was used for verification — this supports key rotation without downtime.

## API Versioning

The current API version is **v1**. Versioning is handled via URL prefix where needed: `/api/v1/`. Breaking changes increment the version number. Non-breaking additions do not.
