# Chapter 08 — platform-internal

## What Is platform-internal?

`platform-internal/` is the internal staff portal — a React web application for G.O.D.S internal operations staff. It sits between the full administrative power of `platform-web` and the end-user division apps.

---

## Distinction from platform-web

| Feature | platform-web | platform-internal |
|---------|-------------|------------------|
| Target users | Administrators, compliance officers | Internal operations staff, support |
| Access level | Full platform control | Operational management within defined scope |
| Typical actions | Policy changes, RBAC, system config | User support, case management, reporting |
| Roles required | `gods_admin`, `compliance`, `sovereignty` | `division_admin`, `supervisor`, `analyst` |

---

## Directory Structure

```
platform-internal/
├── src/
│   ├── App.tsx
│   ├── api.ts
│   ├── pages/
│   │   ├── InternalDash.tsx      Overview of operational metrics
│   │   ├── UserManagement.tsx    Support tickets, user queries
│   │   ├── OversightQueue.tsx    Oversight case queue (for supervisors)
│   │   ├── Reports.tsx           Operational reports
│   │   └── Login.tsx
│   └── components/
├── vite.config.ts
└── package.json
```

---

## Use Cases

**Supervisor (oversight review):**
- Receive assigned oversight cases
- Review the decision record and subject information
- Confirm or override the governance decision
- Track case progress against SLA

**Operations analyst:**
- View division-level governance metrics
- Generate and download operational reports
- Monitor application pipeline health (SETHS)

**Support staff:**
- View user account status (read-only)
- Look up specific decisions by request_id or decision_id
- Escalate issues to the appropriate admin

---

## Access

- Authentication: same JWT auth as all platform services
- Roles: `division_admin`, `supervisor`, `analyst`, `external_auditor`
- No write access to platform configuration
- No access to raw database operations
- Every action is recorded in the audit chain

---

## Render Deployment

Deployed as a static site on Render (`gods-platform-internal` service in `render.yaml`). Served separately from the division apps and platform-web, allowing independent access control at the CDN/DNS level if required.
