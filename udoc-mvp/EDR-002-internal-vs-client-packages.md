# EDR-002 · Internal vs Client package split

**Status:** Accepted  
**Date:** 2026-07-31  
**Context:** CapstoneProjectSJS · role honesty · free-tier hosts · March 2027

## Problem

A single console that mixes staff kill-switch, cross-tenant admin, and tenant self-service blurs who the product is for. Assessors cannot tell whether UDOC is an internal tool, a client SaaS, or both. Demo Netlify apps already implied different roles; live hosts must not collapse them into one undifferentiated UI.

## Decision

**UDOC Capstone ships two primary packages plus public Citizen:**

| Package | Audience | Surfaces |
|---------|----------|----------|
| **Internal** | GODS staff · UDOC admins · operators | Admin Web/Desktop · Operator · Sentinel · Core `/portals` · Core `/admin` |
| **Client** | External / pilot tenants | Client Web/Desktop · App/Mobile · SaaS Portals · Sector (client-facing) |
| **Citizen** | Public (no login) | Client host `/citizen.html` |

**Hard rules**

- Client package **must not** present hardware plane, global kill-switch UI, or staff Access Control as product features.  
- Internal package **may** expose those controls; backend JWT remains authoritative.  
- Gateway routes by **role** into the correct package host.  
- Same Core API; different **intent and chrome**, not a second database.

## Alternatives considered

1. **One mega-PWA for everyone** — rejected (role confusion; assessor cannot grade package boundaries).  
2. **Separate Render service per role (24+)** — rejected (quota · Neon · operational cost).  
3. **Client-only Capstone, no staff path** — rejected (demos and constitutional `/admin` need a staff story).

## Consequences

- Desktop shells are split: `udoc-desktop` (Internal) vs `udoc-desktop-client` (Client).  
- `udoc-app` / mobile are **Client** builds (`UDOC_PACKAGE=client`, CAPS `hw: []`).  
- Documentation must list channels per package (`CAPSTONE_PACKAGE_STORY.md`).  
- New UI work must declare which package it belongs to before merge.

## Related

- `EDR-001-udoc-only-deploy-layer.md`  
- `CAPSTONE_PACKAGE_STORY.md`  
- `UDOC_MVP_PACKAGE_MATRIX.md`  
- `ENGINEERING_ROADMAP_CAPSTONE.md`  
