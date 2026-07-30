# UDOC v9.3 · Demos 6 & 7 · Patent Controls → Live Mapping

**Demo SoT:** https://capstoneprojectsjs.netlify.app  
**Slugs:** `#demo=udoc-platform-ui` (Demo 6) · `#demo=udoc-sovereign-console` (Demo 7)  
**Inventory:** `UDOC_DEMO_INVENTORY.md`  
**Date:** 2026-07-30

These two demos encode **v9.3 patent-facing operational controls** (user + infrastructure). They are the acceptance patterns for repetitive UDOC environments — not separate Render products.

---

## Demo 6 — `udoc-platform-ui` · Operational Control Platform v9.3

### Demo chrome (acceptance)

| Control surface | Intent (patent / ops) |
|-----------------|------------------------|
| Operations Dashboard | Runtime posture · system health · decision volume |
| Model Registry | Registered AI systems · risk tier · status |
| EVA Scoring | Multi-dimensional evaluate · composite · outcome |
| Sovereignty Control | Jurisdiction · localisation · transfer posture |
| StayChain™ (demo) | Tamper-evident decision chain (demo UI) |
| Hot-Reload | Policy / pack activation without full redeploy |
| MFCM cells | Multi-framework compliance matrix cells |

### Live mapping (current Capstone)

| Demo control | Live node | Live API / UI |
|--------------|-----------|---------------|
| Operations Dashboard | Client Dashboard · Sentinel Command | `/udoc/regulator/summary` · `/udoc/demo/ready` |
| Model Registry | Client AI Registry · Sentinel Registry | `/registry/models` |
| EVA Scoring | Client Govern · Sentinel Live Eval · Admin EVA Command · Sector Decisions | `POST /decisions` · scenario chips · **Full EVA batch** |
| Sovereignty Control | Client Sovereignty · Sentinel Sov | `/udoc/exchange` |
| StayChain™ | **Partial** — certificates + evidence + replay | `/decisions/certificates/{id}/verify` · `/udoc/decisions/{id}/evidence` · `/replay` |
| Hot-Reload | Policy Engine (Sentinel / Admin) | `/policy/active` · `/policy/packs` · `/policy/test` |
| MFCM cells | Client Compliance · Sector Frameworks | `/sector/frameworks` · `/compliance/sweep` · coverage bars |

**Honest gap:** StayChain full blockchain UI and full MFCM cell editor are **demo-complete / patent-described**; live is certificate + evidence + policy packs on Neon-light.

---

## Demo 7 — `udoc-sovereign-console` · Sovereign AI Governance Platform v9.3

### Demo chrome (acceptance)

| Control surface | Intent (patent / ops) |
|-----------------|------------------------|
| EVA Detail | 6-D bars · SVS · policy findings · seal |
| StayChain™ blockchain | Immutable audit presentation |
| SVS Monitor | Sovereignty / validity score strip |
| Kill-Switch | Emergency halt / control plane |
| Agent Registry | Systems under governance |

### Live mapping

| Demo control | Live node | Live API / UI |
|--------------|-----------|---------------|
| EVA Detail | Sentinel Live Evaluation · Client Govern | dimensions · composite · policy_enforced · cert |
| StayChain | Evidence / Replay panels | evidence + replay endpoints |
| SVS Monitor | Sentinel KPI strip after evaluate | `svs` field when returned |
| Kill-Switch | Admin **Kill-switch** nav (control view) | existing admin control surface |
| Agent Registry | AI Registry all surfaces | `/registry/models` · prefer `model-001` |

**Honest gap:** Full sovereign-console chrome and StayChain visualisation remain denser on Netlify; live concentrates on **deterministic EVA + policy-to-code + fail-closed** — the enforceable patent core on free hardware.

---

## Repetitive UDOC environment pattern (v9.3 → live)

Every UDOC deployment environment (pilot SaaS, in-house, future hardware node) should expose the **same control loop**:

```
1. Boot posture     → GET /udoc/demo/ready (or equivalent seed)
2. Register system  → registry (optional; seed model-001 OK)
3. Activate policy  → ACTIVE pack + enforced_rules > 0
4. Evaluate         → POST /decisions (Fair / Biased / High / Sov)
5. Assert           → biased = BLOCK · fair ≠ BLOCK · policy_enforced
6. Certify          → certificate_id + verify
7. Evidence         → evidence / replay
8. Human path       → oversight / portals dual-path / citizen challenge
```

**UI may differ by tier; the loop must not.** That is the patent-aligned “repetitive environment” rule for assessor and for future hardware upload.

---

## Infrastructure patent controls (software vs hardware)

| Control class | Software live (now) | Hardware / sovereign tier (Canon Vol X) |
|---------------|---------------------|------------------------------------------|
| Policy-to-code | Live packs + decisions | Same engines on UDOC node |
| Fail-closed | Missing model/policy blocks unsafe path | Same |
| Audit evidence | Neon rows + cert verify | WORM / stronger store post-seed |
| Kill-switch | Admin control surface | Physical + logical dual |
| Sovereignty | ZA exchange signals in EVA body | Air-gap + HSM (Tier 3) |
| StayChain | Cert + evidence chain | Full chain product |

Software bootloaders are valid on any functioning machine; **hardware product** is funding + deployment tier — not a reason to stop software valuation of the governance loop.

---

## Assessor check (demos 6 & 7)

| # | Check | Pass |
|---|--------|------|
| 1 | Open Netlify `#demo=udoc-platform-ui` | see ops/registry/EVA chrome |
| 2 | Open `#demo=udoc-sovereign-console` | see EVA detail / kill / registry |
| 3 | Live Sentinel + Client Govern | Full EVA batch · biased BLOCK |
| 4 | Live cert verify after evaluate | VALID |
| 5 | Live compliance / frameworks | sweep or framework cards |
| 6 | Live Admin kill-switch + HITL | nav present · Portals dual-path |

GIS/GBS structured product update remains **out of scope** until this loop is operator-green on live.
