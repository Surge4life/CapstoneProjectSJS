# Session 13 — GIS Access Control + Approved Open-Source Path

**Date:** 2026-07-28  
**Focus:** UDOC control over G.O.D.S Intelligence / GIS engines, data-sharing, storage and processing. Approved path for open-source / external access.

## 1. Principle (locked)

- **G.O.D.S Holdings** retains ownership of Intelligence.
- **UDOC** is the sole governance control plane for:
  - Deterministic engines (gis_engine, gbs_engine, cetcte_engine, etc.)
  - Intelligence databases and storage
  - Data-sharing and processing access
  - Audit of every access and decision involving GIS outputs

No direct external or division path to GIS Intelligence bypasses UDOC.

## 2. Current live state (platform-core)

| Component | Location / Status |
|-----------|-------------------|
| gis_engine.py | platform-core — live |
| gbs_engine.py | platform-core — live |
| cetcte_engine.py | platform-core — live |
| /gis routes | Present |
| Fail-closed 12-pillar GIS | Operational |
| Multi-tenant + RBAC | Enforced at UDOC layer |

## 3. Access control model

### Internal (UDOC / GODS staff)
- Role + profile scoped (admin, exec, gov, operator, auditor, etc.)
- RBAC matrix already live (`/rbac/me`, `/rbac/matrix`)
- Intelligence tab on udoc-internal is the staff entry point
- All engine calls and data access audited via StayChain

### External clients
- **No raw GIS engine access**
- Clients receive only UDOC-governed outputs (EVA verdicts, certificates, sector frameworks, compliance status)
- Knowledge bases remain tenant-isolated
- API keys scoped to tenant; cannot invoke GIS engines directly

### Divisions (SETHS, TS, MADIBA, GBS Franchise)
- Future division portals must authenticate through UDOC
- GIS-derived insights only via UDOC-mediated APIs
- Data-sharing policies enforced by UDOC Policy-to-Code / COB

## 4. Approved open-source path (post-registration)

1. **Scope**: Read-only, audited views of approved GIS Intelligence artefacts (schemas, pillar definitions, non-sensitive reference data).
2. **Gate**: UDOC access control + explicit approval (admin / COB).
3. **Delivery**: Separate public or partner repository / package under dual-license or non-commercial academic clause until entity registration complete.
4. **Never open**: Live decision data, tenant data, signing keys, full engine internals that would allow bypass of UDOC governance.
5. **Honesty**: Any public release carries the same pre-registration / GG54477 / POPIA footing.

## 5. Implementation checklist (Session 13)

| Item | Status |
|------|--------|
| Document UDOC-as-control-plane principle | This file |
| Confirm engines live under platform-core | Yes |
| External clients blocked from raw GIS | By design (no public GIS endpoints for clients) |
| Staff Intelligence surface | Live on udoc-internal |
| Open-source policy sketch | Section 4 above |
| Code hardening of GIS routes (scope checks) | Incremental — next polish if needed |

## 6. Next
Session 14 — Cross-consistency + final production readiness (honesty pass, render.yaml, proof update).
