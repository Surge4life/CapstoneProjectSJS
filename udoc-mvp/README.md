# udoc-mvp — Demo-to-Production Mapping (v9.3)

This folder tracks integration of the original interactive demos into production **package channels** (Internal staff vs Client tenant surfaces) and records **engineering intent** under free-tier limits.

**Capstone priority:** documented intention and honest constraints > competing on code novelty with the rest of the world. Code can change; unwritten purpose cannot be graded.

## Start here (assessor)

| Doc | Purpose |
|-----|---------|
| **`CAPSTONE_COVER_NOTE.md`** | One-page submission framing |
| **`ASSESSOR_READING_ORDER.md`** | 15-minute and 45-minute reading paths |
| **`GLOSSARY.md`** | Shared term meanings |
| **`ARCHITECTURE_MAP.md`** | One-page stack + deploy diagram |
| **`CAPSTONE_EVIDENCE_PACK.md`** | What constitutes submission evidence |
| **`LIMITATIONS_REGISTER.md`** | Known limits named explicitly |
| **`SUBMISSION_TIMELINE.md`** | Orientation to March 2027 |
| **`CANON_FREEZE_NOTICE.md`** | Do not expand philosophy instead of verifying live |
| **`ENGINEERING_ROADMAP_CAPSTONE.md`** | Freeze list · phases · Capstone bar |
| **`EDR-001` … `EDR-004`** | Deploy · packages · free-tier · demo-seed smoke |
| **`CAPSTONE_PACKAGE_STORY.md`** | Demos 1–7 → live channels |
| **`UDOC_MVP_PACKAGE_MATRIX.md`** | Package checklist |
| **`UDOC_SMOKE_PASS.md`** | Minimum live pass definition |
| **`SMOKE_EVIDENCE_TEMPLATE.md`** | Operator record for Task 2 close |
| **`P6_ASSESSOR_SIDE_BY_SIDE.md`** | Demo vs live per surface |
| `UDOC_SAAS_READINESS_GAP.md` | What is **not** claimed commercially |
| `UDOC_LIVE_ENVIRONMENTS.md` | Live hosts |

## Demo → Surface Mapping

| Original Demo | Target Production Surface | Status |
|---------------|---------------------------|--------|
| mvp-1 / mvp-2 | **Client** (+ Sector) | Core live |
| v7-eva / platform / sovereign | **Internal** + Sentinel + Client subset | Density wave |
| v7-platform Citizen | Client `/citizen.html` | Live public path |

## Tier / package ownership

- **Client package:** `udoc-public`, `udoc-portals`, `udoc-app`, `udoc-mobile`, `udoc-desktop-client`  
- **Internal package:** `udoc-internal`, `udoc-desktop`, `udoc-operator`, Core `/Sentinel` · `/portals` · `/admin`  
- **Gateway:** role → package host  
- **GIS / GBS depth:** after Task 2 live smoke green

## Session log

- Package + intent spine M10–M13 (2026-07-31)  
- **Limitations · timeline · Canon freeze** (2026-07-31)  
- **M7:** still operator live smoke (biased = BLOCK)
