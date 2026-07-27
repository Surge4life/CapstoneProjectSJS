# Session 12 — Sales Packaging + Client Onboarding

**Date:** 2026-07-28  
**Focus:** External client sales structure and onboarding flows for production-ready UDOC deployments.

## 1. Sales packaging (External Tier 1)

### Recommended SaaS tiers (aligned to existing /tenants/tiers)

| Tier | Target | Included | Limits (illustrative) |
|------|--------|----------|------------------------|
| **Starter** | Small teams / pilot | 1 sector assignment, basic EVA, certificate volume low, knowledge base | Limited models / certs / month |
| **Professional** | Mid-size organisations | Full sector frameworks, higher cert volume, API keys, priority support | Higher model + decision quotas |
| **Sovereign** | Regulated / public-sector / enterprise | Full PUBLIC or PRIVATE differentiation, dedicated oversight, custom frameworks, audit export | Highest quotas + dedicated support path |

All tiers remain **UDOC-ONLY** interfaces. No direct GODS Intelligence exposure.

### What is already live
- `/tenants` + `/tenants/tiers` endpoints
- Sector assignment (PUBLIC / PRIVATE / GENERAL) via admin
- Plan & API Keys view on udoc-public Settings
- Multi-tenant isolation + knowledge base per tenant

## 2. Client onboarding flow (recommended)

1. **Gateway / SSO** → role routes to Client console (udoc-public)
2. **Tenant creation** (admin or self-serve bootstrap) → assign sector + tier
3. **First login** → Dashboard shows sector-specific tagline + frameworks
4. **Govern path** → Register first AI system → Run EVA → Verify certificate
5. **Compliance** → View frameworks in force for the assigned sector
6. **Settings** → Generate API keys for programmatic access

## 3. Sales-facing artefacts (to produce / maintain)

- One-pager: “UDOC Client Governance Platform — tiers & sector fit”
- Onboarding checklist (sector choice, risk tier, first model, first certificate)
- Demo credentials rotation note (pre-public)
- Honesty footer on every client surface (already present)

## 4. Implementation status

| Item | Status |
|------|--------|
| Tier data model + API | Live |
| Sector assignment | Live (admin) |
| Client Settings / API keys | Live |
| Self-serve onboarding UI polish | Incremental (Session 12 documents the flow) |
| Sales packaging docs | This file + future one-pagers |

## 5. Next
Session 13 — GIS access control + approved open-source path for Intelligence storage/processing under UDOC governance.
