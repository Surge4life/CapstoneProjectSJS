# Chapter 05 — Franchise Portal

## Overview

The franchise portal is the interface for G.O.D.S franchise operators — organisations that operate licensed G.O.D.S deployments. Franchise operators manage their client onboarding, oversee their deployment's governance health, and report to the G.O.D.S platform operator.

---

## Who Uses the Franchise Portal?

A franchise operator is an organisation that has signed a G.O.D.S franchise agreement and operates their own G.O.D.S deployment (cloud or on-premises) for their clients. Examples:
- A professional services firm offering G.O.D.S governance as a service to their clients
- A government department deploying G.O.D.S for national AI governance
- A regional provider in a specific sector (e.g., healthcare AI governance)

The franchise portal is accessible from `platform-internal` (restricted to users with `franchise_operator` role).

---

## Information Architecture

```
Franchise Portal
├── Dashboard
│   ├── Active tenants overview
│   ├── Governance health across tenants (aggregate)
│   ├── Certification status (franchise operator certification)
│   └── Compliance obligations status
│
├── Tenant Management
│   ├── Active tenants list
│   ├── Onboard new tenant
│   ├── Tenant detail
│   │   ├── Tenant configuration
│   │   ├── Governance metrics (for this tenant)
│   │   ├── Compliance issues (if any)
│   │   └── Billing status
│   └── Off-board tenant
│
├── Governance Oversight
│   ├── Cross-tenant oversight case queue
│   ├── Governance report by tenant
│   └── Escalations requiring franchise-level attention
│
├── Certifications
│   ├── Franchise operator certification status + expiry
│   ├── Tenant certifications issued
│   └── Pending certification renewals
│
├── Reporting
│   ├── Quarterly franchise governance report
│   ├── Platform usage report
│   └── Export for G.O.D.S platform operator review
│
└── Settings
    ├── Franchise configuration
    ├── Governance customisation (within franchise bounds)
    └── Billing and usage
```

---

## Tenant Onboarding Flow

```
1. Franchise operator initiates tenant creation
   ├── Enter company name, tenant code, plan tier
   └── Confirm franchise governance terms apply
          ↓
2. G.O.D.S platform validates the request
   (Franchise must have capacity on their licence)
          ↓
3. Tenant provisioned
   ├── Database schemas created
   ├── Default PolicyPack assigned
   ├── Admin user invitation sent
   └── GIS registration created
          ↓
4. Client admin receives onboarding email
   ├── Sets up their admin account
   └── Proceeds with corpus setup and model registration
```

---

## Governance Aggregation View

The franchise operator sees aggregate governance health across all their tenants:

```
┌────────────────────────────────────────────────────────┐
│ Franchise Governance Health — January 2025             │
├──────────────┬─────────┬─────────┬─────────────────────┤
│ Tenant       │Decisions│BlockRate│ Compliance Status    │
├──────────────┼─────────┼─────────┼─────────────────────┤
│ Acme Corp    │  2,847  │  5.1%   │ ✓ Healthy            │
│ Beta Holdings│    891  │  8.9%   │ ⚠ Review needed      │
│ Gamma Gov    │  5,432  │  4.2%   │ ✓ Healthy            │
│ Delta AI     │    234  │  14.7%  │ ✗ Compliance alert   │
└──────────────┴─────────┴─────────┴─────────────────────┘
```

A high block rate or compliance alert triggers a notification to the franchise operator. They have a responsibility under the franchise agreement to escalate persistent compliance issues to the G.O.D.S platform operator.

---

## Franchise Accountability Model

The franchise portal reflects the accountability hierarchy:

- **G.O.D.S platform operator** → sets constitutional rules (non-negotiable)
- **Franchise operator** → manages tenants, ensures compliance, cannot override constitutional rules
- **Tenant** → operates their G.O.D.S instance within franchise and constitutional bounds

The franchise portal enforces this hierarchy: franchise operators see their tenants' governance health but cannot access individual user data or override governance decisions. They can escalate compliance issues to the G.O.D.S platform operator but cannot resolve them unilaterally.
