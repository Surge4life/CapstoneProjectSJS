# udoc-mvp — Demo-to-Production Mapping (v9.3)

This folder tracks integration of the original interactive demos into production **package channels** (Internal staff vs Client tenant surfaces) and records **engineering intent** under free-tier limits.

**Capstone priority:** documented intention and honest constraints > competing on code novelty with the rest of the world. Code can change; unwritten purpose cannot be graded.

## Start here

| Doc | Purpose |
|-----|---------|
| **`ENGINEERING_ROADMAP_CAPSTONE.md`** | Freeze list · phases · constraints · Capstone bar |
| **`EDR-001-udoc-only-deploy-layer.md`** | Why only UDOC is the deploy product layer |
| **`CAPSTONE_PACKAGE_STORY.md`** | Demos 1–7 → Internal vs Client |
| **`UDOC_MVP_PACKAGE_MATRIX.md`** | Package checklist (M1–M10) |
| `UDOC_SAAS_READINESS_GAP.md` | What is **not** claimed commercially |
| `UDOC_LIVE_ENVIRONMENTS.md` | Live hosts |
| `UDOC_SMOKE_PASS.md` · `P6_ASSESSOR_SIDE_BY_SIDE.md` | Verify live |

## Demo → Surface Mapping

| Original Demo | Target Production Surface | Status |
|---------------|---------------------------|--------|
| mvp-1 International Standards Dashboard | **Client** Web / App / Desktop Client | Core live + Session 9 |
| mvp-2 Multi-Framework Compliance Engine | **Client** + Sector | Core live + Session 9 |
| v5-sa SA-Aligned Architecture Lineage | **Internal** + Client sov strip | Session 10 |
| v7-platform Full Platform | **Split** Internal + Client + Citizen + Portals | Density wave |
| v7-eva EVA Engine | Sentinel + Client Govern | Live 6-dim + certs |
| udoc-platform-ui Operational Control | **Internal** Admin (Client subset) | Session 11 |
| udoc-sovereign-console | **Internal** Admin + Sentinel | Session 11 |

## Tier / package ownership

- **Client package:** `udoc-public`, `udoc-portals`, `udoc-app`, `udoc-mobile`, `udoc-desktop-client`  
- **Internal package:** `udoc-internal`, `udoc-desktop`, `udoc-operator`, Core `/Sentinel` · `/portals` · `/admin`  
- **Gateway:** role → package host  
- **GIS / GBS / GODS product depth:** after Task 2 live smoke green (see roadmap)

## Session log

- Sessions 1–5: Core density  
- Sessions 8–14: ecosystem blueprint (historical; Task 2 reopened for demo parity honesty)  
- Density + portals dual-path + package split (2026-07-28 → 07-31)  
- **M10:** Engineering roadmap + EDR-001 — intent documented before further expansion  
- **M7:** still operator live smoke (biased = BLOCK)
