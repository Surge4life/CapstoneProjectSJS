# Portal live dual-path (Neon-light) — COMPLETE

**Surface:** `GET/POST /portal/{key}` on platform-core  
**UI:** `/portals` · no new Render services · OversightCase only

## Model

| Mode | Portals | Behaviour |
|------|---------|-----------|
| **oversight** | HITL, Regulator, InfoReg, SAHRC, Case Manager, Welfare, SARS, COB, Border, DHA, Service Delivery, Municipal, Justice, NPA, Health, SETHS, Employer, MADIBA, Insurance, DCDT Policy, Super Admin | Every control **opens** `COB-` case unless Target is existing `COB-…` **and** control is a resolve verb |
| **audit** | AI Owner, Private Compliance | Audit row only; Target = model id |
| **citizen_ui** | CITIZEN | Full AI-Rights UI · public `/citizen/*` |

## Resolve controls (Target = `COB-…`)

Approve AI Decision · Override · Release · Close Case · Close Matter · Publish Finding · Disburse · Withdraw Case · Archive Case · Resolve · Close Feedback · Release Hold · Approve Payout · Certify

## Verify (after Core redeploy)

1. `/portals` sign in as admin
2. **Border** → Flag Traveler (target `model-001`) → terminal `live → case_ref`
3. **Health** → Triage Patient → new case on Neon panel
4. **HITL** → click `COB-…` → Override → state **OVERRIDDEN**
5. **AI Owner** → Monitor Drift → `live → audit` (no OversightCase)
6. **Citizen** → full Challenge / Status UI (no control headings)

Neon ≤500MB · no new user registration · no new Render services.
