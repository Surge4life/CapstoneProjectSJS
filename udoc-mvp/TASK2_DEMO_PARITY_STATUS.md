# Task 2 status — DEMO PARITY (2026-07-29)

## Source of truth
- `docs/ENGINEERING_CANON.md` + Vols I–XI
- Netlify demos · `UDOC_DEMO_INVENTORY.md`
- `P6_ASSESSOR_SIDE_BY_SIDE.md` · `UDOC_SMOKE_PASS.md`

## Phase progress

| Phase | Focus | Status | Commit(s) |
|-------|--------|--------|-----------|
| **P1** | Sentinel | Hardened | `5b5757c` |
| **P2** | Client + smoke + cert verify | Densified | `2122670`, `49fc4d1` |
| **P3** | Admin (SW v3) | Densified | `747e25f` |
| **P5** | Citizen | Linked | `b45e733` |
| **P6** | Assessor matrix | Checklist live | `7bff621` |

## P2 latest (`49fc4d1`)
After Govern EVA:
- **Verify cert** → `GET /decisions/certificates/{id}/verify`
- **Evidence** → `GET /udoc/decisions/{id}/evidence`
- Decisions table → Verify jumps to Govern

## Close rule
Live green on `P6_ASSESSOR_SIDE_BY_SIDE.md` + `UDOC_SMOKE_PASS.md`.  
**Task 1** only after Task 2 pass.
