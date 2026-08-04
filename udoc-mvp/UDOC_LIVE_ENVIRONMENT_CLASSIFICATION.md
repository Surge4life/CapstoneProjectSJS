# UDOC Live Environment Classification

**Date:** 2026-08-04 · **Status:** Working register · Pre-registration Capstone  
**Full Word copy:** project artifacts `UDOC_Live_Environment_Classification.docx`

## Purpose

Classify every live UDOC-related environment: users, access, relevance, relations to UDOC / G.O.D.S, and what you can still do while GBS documents are completed offline.

## Master matrix

| Environment | Primary users | Access | UDOC role |
|-------------|---------------|--------|-----------|
| **gods-platform-core** | All systems | JWT · public citizen routes | API brain · Neon |
| **gods-udoc-client** | External clients | client@ · tenant_pk | Client SaaS package |
| **gods-udoc-admin** | UDOC / GODS staff | Staff · PWA SW | Internal controller |
| **gods-udoc-sector** | Sector operators | PUBLIC/PRIVATE | Sector console |
| **gods-udoc-operator** | Operators | Operator login | Smoke / demo ops |
| **gods-udoc-portals** | Client roles | admin/controller/cob/auditor/viewer | SaaS portals shell |
| **gods-udoc-gateway** | Everyone | Public links | Surface directory |
| **gods-udoc-web** | Staff intelligence | admin | G.O.D.S Intelligence UI |
| Core **/admin** | Constitutional staff | Platform admin | GODS governance |
| Core **/udoc-admin** | UDOC controllers | Staff | Internal entry on Core |
| Core **/Sentinel** | Operators · assessors | Auth for API | EVA Command Centre |
| Core **/portals** | 24-portal controllers | Auth · dual-path | Portal workspace |
| Core **/eif-ui** | Staff · MADIBA path | Auth nominate | EIF Diamond |
| Client **/citizen.html** | Public | No login | Citizen / AI Rights |

## Persona map

| Persona | Use | Must not |
|---------|-----|----------|
| External client | Client SaaS · Portals SaaS · Citizen | Admin, Core /admin, GODS web intel, other tenants’ KB |
| Citizen | `/citizen.html` + `/citizen/*` API | Staff consoles |
| UDOC staff | Admin · Sentinel · Sector · EIF | Treat Client KB as shared |
| GODS constitutional | Core `/admin` · GODS web · `/portals` | Client package as staff plane |
| Assessor | Gateway · Sentinel · Client Govern · Citizen | Expect commercial multi-region SaaS |

## Intelligence dual path

- **G.O.D.S Intelligence** (`gods-udoc-web` + Admin `/intel`): internal archive.
- **Company Knowledge** (Client): `tenant_pk` private rows only.
- Same deterministic retrieval family; different tables; no LLM controller.

## While waiting for GBS docs

1. Close Task 2 operator ticks (biased=BLOCK on surfaces 1–5).
2. Optional local permanent UI embeds (`LOCAL_UI_PERMANENT_EMBED.md`).
3. Short Client corpus extracts only (Neon ≤500MB).
4. EIF nominate audit + portal HITL on Core.
5. Keep Gateway links accurate; **no new Render services** unless quota allows.
6. **Do not** build full GBS/GIS runtime until Task 1 founder docs are complete.

## Constraints

Render free · cold starts · ~20 services · Neon ≤500MB · demo seed · auto-heal `/udoc/demo/ready` · GG54477 withdrawn · POPIA s71 + Constitution.

## Verified live (2026-08-04)

All hosts in the matrix returned HTTP 200 on probe, including Core health, Client, Admin, Sector, Gateway, Web, Portals, Operator, Sentinel, Portals HTML, EIF UI, Citizen page.
