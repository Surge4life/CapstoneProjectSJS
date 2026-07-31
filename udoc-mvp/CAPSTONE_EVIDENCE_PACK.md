# Capstone evidence pack · outline

**Purpose:** What an assessor (or future self) should be able to find to prove the Capstone is a **documented, constrained, live** UDOC system — not a marketing deck.  
**Date:** 2026-07-31  
**Rule:** Intent documents + dated smoke evidence > volume of uncommitted code.

---

## Pack contents (checklist)

### A. Intent and decisions (required)

| Item | Location | Present? |
|------|----------|----------|
| Cover note | `CAPSTONE_COVER_NOTE.md` | Yes |
| Glossary | `GLOSSARY.md` | Yes |
| Engineering roadmap + freeze list | `ENGINEERING_ROADMAP_CAPSTONE.md` | Yes |
| UDOC-only deploy layer | `EDR-001-udoc-only-deploy-layer.md` | Yes |
| Internal vs Client packages | `EDR-002-internal-vs-client-packages.md` | Yes |
| Free-tier constraints | `EDR-003-free-tier-constraints.md` | Yes |
| Demo seed / no-registration smoke | `EDR-004-demo-seed-no-registration-smoke.md` | Yes |
| Package story (demos → channels) | `CAPSTONE_PACKAGE_STORY.md` | Yes |
| Assessor reading order | `ASSESSOR_READING_ORDER.md` | Yes |
| SaaS / commercial non-claim | `UDOC_SAAS_READINESS_GAP.md` | Yes |

### B. Live environment honesty (required)

| Item | Location |
|------|----------|
| Host and routing map | `UDOC_LIVE_ENVIRONMENTS.md` |
| Architecture one-pager | `ARCHITECTURE_MAP.md` |
| Package matrix | `UDOC_MVP_PACKAGE_MATRIX.md` |

### C. Verification (required for Task 2 close)

| Item | Location |
|------|----------|
| Smoke pass definition | `UDOC_SMOKE_PASS.md` |
| Side-by-side demo vs live | `P6_ASSESSOR_SIDE_BY_SIDE.md` |
| **Filled** evidence form (dated) | `SMOKE_EVIDENCE_TEMPLATE.md` → copy when run |

### D. Optional depth (when time allows)

| Item | Location |
|------|----------|
| Demos 6–7 patent/control map | `UDOC_V93_DEMO67_PATENT_CONTROLS.md` |
| Portal dual-path | `PORTAL_LIVE_CORE.md` |
| Engineering Canon volumes | `docs/` |
| Screenshots of live BLOCK / Citizen / Gateway | Capstone submission folder (operator-produced) |

---

## How to use before submission

1. Walk `ASSESSOR_READING_ORDER.md` once yourself.  
2. Run live smoke; complete evidence template; keep a copy with date.  
3. Do not expand GIS/GBS claims beyond what roadmap and gap docs allow.  
4. Prefer updating an EDR when a decision changes — before rewriting large code.

---

## Explicit non-evidence

- Commit count alone  
- Unverified "parity" claims without biased = BLOCK live  
- Commercial readiness language  
- Hardware appliance claims without ops evidence  
