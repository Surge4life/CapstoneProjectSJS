# Chapter 07 — platform-web

## What Is platform-web?

`platform-web/` is the G.O.D.S Admin Console — the Sovereign-Operator mainframe. It is a React + Vite web application that provides comprehensive administrative control of the entire G.O.D.S ecosystem from a single browser interface.

Unlike the four division apps, `platform-web` has no mobile counterpart and no Capacitor build. It is browser-only, by design. This is a security choice: the administrative console should only be accessed from a desktop browser on a managed device.

---

## Directory Structure

```
platform-web/
├── public/
│   └── manifest.json       (not a PWA — no service worker)
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── api.ts              Admin API client (all admin endpoints)
│   ├── types.ts
│   ├── components/
│   │   ├── layout/         Sidebar, header, navigation
│   │   ├── governance/     Decision inspector, oversight case manager
│   │   ├── udoc/           Model registry, edge node status
│   │   ├── seths/          SETHS admin components
│   │   ├── madiba/         MADIBA admin components
│   │   ├── ts/             TS admin components
│   │   ├── intelligence/   Corpus management, query logs
│   │   ├── compliance/     GBS rules, bias reports, conformance
│   │   └── system/         Users, roles, configuration, health
│   ├── pages/
│   │   ├── AdminDash.tsx   Main dashboard
│   │   ├── UDOCConsole.tsx
│   │   ├── SETHSConsole.tsx
│   │   ├── MADIBAConsole.tsx
│   │   ├── TSConsole.tsx
│   │   ├── AuditConsole.tsx
│   │   ├── ComplianceConsole.tsx
│   │   ├── IntelligenceConsole.tsx
│   │   └── Login.tsx
│   └── assets/
├── vite.config.ts
├── tsconfig.json
└── package.json
```

---

## Access Control

`platform-web` enforces strict access control:

1. **Authentication:** RS256 JWT required (same auth as platform-core)
2. **Role requirement:** User must have `gods_admin`, `compliance`, `sovereignty`, or `division_admin` role
3. **No public routes:** Every route (except `/login`) requires authentication
4. **Session timeout:** Admin sessions timeout after 2 hours of inactivity (configurable, maximum 4 hours)
5. **IP allowlist (optional):** Deployments can configure an IP allowlist at the infrastructure level (NGINX/Kubernetes NetworkPolicy)

---

## Why No Mobile?

The admin console is deliberately desktop-only for several reasons:

1. **Screen density:** The admin interface is data-dense. A compliance officer reviewing governance decisions needs a large screen to work effectively.
2. **Security surface:** Mobile devices have a larger attack surface (lost devices, malware, shoulder surfing). Administrative access to the full governance platform should be restricted to managed desktop devices.
3. **Keyboard-first operations:** Many admin operations are keyboard-intensive (search, filter, bulk actions). These are better suited to desktop.
4. **RBAC enforcement:** The "no mobile admin" policy is enforced by the RBAC system — not by device detection, which is bypassable.

If a compliance officer needs to act on an urgent oversight case from a mobile device, they use the `supervisor` role-limited view in the relevant division app, which provides read and review access but not full administrative control.

---

## Key Difference from Division Apps

| Feature | Division Apps | platform-web |
|---------|--------------|-------------|
| PWA / installable | Yes | No |
| Mobile build | Yes | No |
| Connect screen | Yes (any backend URL) | No (fixed to deployment) |
| User scope | End users of the division | Administrators only |
| Data scope | Own records (with RBAC) | All records (with RBAC) |
| Real-time updates | Polling | WebSocket (governance feed) |
