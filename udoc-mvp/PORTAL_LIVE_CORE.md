# Portal live dual-path (Neon-light)

**Surface:** `GET/POST /portal/{key}` on platform-core  
**UI:** `/portals` · no new Render services

## OversightCase writers (open / resolve via Target = COB-…)

| Portal key | Open controls | Resolve controls (Target = case_ref) |
|------------|---------------|--------------------------------------|
| HITL_REVIEW | Flag for Training; others if no COB- target | Approve AI Decision · Override · Release |
| REGULATOR | Start Audit · Review Submission · Impose Penalty · Issue Directive | — |
| INFO_REGULATOR | Open Investigation · Issue PAIA Notice · Assess Breach | Close Case |
| CONSTITUTIONAL_OVERSIGHT | Constitutional Review · Issue Opinion · Refer to Court | Close Matter |
| SAHRC | Log Complaint · Start Investigation · Schedule Hearing | Publish Finding |
| CASE_MANAGER | Open Case · Assign Worker · Update Status | Close Case |
| WELFARE | Approve Grant · Verify Beneficiary · Investigate Fraud | Disburse |
| SARS | Initiate Audit · Verify Return · Issue Assessment | Close Case |

## Audit-only (no OversightCase row)

| Portal key | Behaviour |
|------------|-----------|
| AI_OWNER | Audit + model target (prefer model-001) |
| PRIVATE_COMPLIANCE | Audit + model/subject target |

## Citizen

Full AI-Rights UI (not control headings) · public `/citizen/*` · also Client `/citizen.html`

## Verify

1. Sign in `/portals`
2. Open **SAHRC** → Execute **Log Complaint** (target `model-001`) → terminal `live → case_ref`
3. Open **HITL Review** → click case_ref → **Override** → state OVERRIDDEN
4. Neon ≤500MB · no new user registration
