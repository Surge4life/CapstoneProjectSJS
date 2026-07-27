# Chapter 07 — Government Portal

## Overview

The government portal provides government bodies, regulators, and oversight authorities with read-only access to governance records relevant to their mandate. It is designed for regulatory inspection — not operational use.

---

## Who Uses the Government Portal?

- **Labour inspectors** reviewing employment equity compliance
- **Data regulators** (Information Regulator) reviewing POPIA compliance
- **National AI governance bodies** reviewing AI model compliance
- **Auditor-General** performing performance audits
- **Parliamentary oversight committees** reviewing AI governance metrics

The government portal is accessed via `platform-web` for provisioned government users, or via a dedicated `portals-web` government view for self-provisioned access (requires verification).

---

## Design Principles for Government Users

Government portal users are not typical software users. Many are:
- Senior officials who use software infrequently
- Legal professionals comfortable with documents, not dashboards
- Technical staff who expect professional, austere interfaces

Design principles:
1. **Document-first** — data is presented in document form, not dashboards. Inspectors want to read records, not navigate charts.
2. **Audit trail prominence** — the audit trail reference is always visible. Every record shows its audit reference.
3. **Export by default** — inspectors need to take records with them. Export to PDF/CSV is available on every view.
4. **Plain language** — technical governance terminology is explained inline.
5. **No manipulation** — the government portal is read-only. Nothing can be changed.

---

## Information Architecture

```
Government Portal
├── Overview
│   └── Summary statistics for the inspection period
│
├── Governance Records
│   ├── Decision registry (searchable, filterable)
│   ├── Decision detail view (with full audit trail)
│   └── Export decisions (PDF or CSV)
│
├── Oversight Cases
│   ├── Resolved cases (searchable)
│   ├── SLA compliance metrics
│   └── Export oversight cases
│
├── AI Model Registry
│   ├── Registered models (by operator, status, sector)
│   ├── Model detail (registration, FSM history, governance record)
│   ├── Suspended/revoked models
│   └── Export model registry
│
├── Employment Equity (Labour Inspectors Only)
│   ├── Employment equity metrics by employer
│   ├── Employer bias score trends
│   ├── Sector-level equity analysis
│   └── Export for EEA compliance review
│
├── POPIA Compliance (Information Regulator Only)
│   ├── Data processing activities register
│   ├── Data subject access request log
│   ├── Consent register summary
│   ├── Cross-border data flow register
│   └── Retention policy compliance
│
└── Audit Chain
    ├── Chain integrity status
    ├── Merkle root verification
    └── Specific record lookup (by audit_ref_id)
```

---

## Access Provisioning

Government access is provisioned differently from regular tenant access:

1. Government body requests access (through formal channel — letter, email)
2. G.O.D.S platform operator verifies the request
3. A time-limited `external_auditor` role is assigned (maximum 12 months)
4. Government user receives credentials with strict 2FA requirement
5. Access scope is set: which tenant(s), which data categories, which date range
6. All government portal access is logged with `GDPR.GOVERNMENT_ACCESS` event type

Government users cannot create, modify, or delete any records. Their read access is logged. This ensures full accountability for what was accessed and when.

---

## The Audit Certificate

At the end of a regulatory inspection, the government portal can generate an **Audit Certificate** — a signed PDF confirming:

- What data was accessed
- The date range of the inspection
- That the audit chain integrity was verified for the inspection period
- The Merkle root signature for the period
- The platform version at time of inspection

This certificate is HMAC-sealed and can be independently verified against the audit chain.
