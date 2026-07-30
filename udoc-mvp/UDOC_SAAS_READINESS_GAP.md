# UDOC SaaS Readiness · Triple-Check (2026-07-30)

**Purpose:** Honest answer to: *Is UDOC ready for test clientele and paid/startup hosting, or what must land first?*  
**Sources:** Live Render/Neon stack · Netlify demos · Engineering Canon · external architecture review · Task 2 density work  
**Rule:** Do not expand GIS/GBS until UDOC operational bar below is met.

---

## Executive answer

| Milestone | Status |
|-----------|--------|
| **Architecture ready** | YES — Canon + engines + surfaces |
| **Developer / Capstone ready** | YES — runnable Core + demos + smoke path |
| **Assessor demo-parity ready** | **CONDITIONAL** — density in repo; **operator must still green P6 live** |
| **Pilot SaaS ready (friendly breakers)** | **NOT YET** — identity, tenancy proof, backups, monitoring |
| **Commercial SaaS ready** | **NO** |
| **Hardware product ready** | **NO** — architecture stronger than ops |

**Verdict matches the external review:** platform repository, not commercial SaaS. Overall ~**75–80%** of a production-grade *platform shape*; the remaining gap is **operational hardening**, not more product vision.

---

## A. What UDOC has (stop redesigning)

### Governance loop (live software)

- Deterministic EVA path: `POST /decisions` · 6-D · policy_enforced · fail-closed bias **BLOCK** design
- Demo seed: `model-001` + ACTIVE pack · `GET /udoc/demo/ready`
- Certificates + evidence/replay endpoints (StayChain *product* still partial)
- Policy activate / test / archive surfaces on Sentinel
- 12-pillar conformance presentation on Sentinel

### Surfaces (existing hosts only)

| Surface | Role |
|---------|------|
| Core API + `/Sentinel` + `/portals` + `/admin` | Runtime + EVA + dual-path portals + constitutional |
| Client (`udoc-public`) + `/citizen.html` | Tenant governance + public AI-Rights |
| Admin (`udoc-internal`) | Internal UDOC controller |
| Sector | PUBLIC/PRIVATE console |
| SaaS Portals | Role + sector filtered control forms |
| Gateway | Sign-on router |
| Operator | Workspace |

### Density (Task 2 engineering — 2026-07-30)

- Scenario chips + **Full EVA batch** on Client / Sentinel / Admin / Sector
- Portal dual-path → OversightCase on Neon (`PORTAL_LIVE_CORE.md`)
- Citizen public challenge/status on Core `/citizen/*`
- Gateway full surface link grid

**Still open:** Task 2 **close** only after **you** observe biased = BLOCK on live Client + Sentinel + Admin + Sector (`P6_ASSESSOR_SIDE_BY_SIDE.md`).

### Documentation maturity

Canon volumes I–XI exist as modular knowledge base. External review: freeze **Canon v1.0** — do **not** expand philosophy; implement from Canon. Optional later (ADR, domain model, event catalogue) only when a **real engineering problem** appears during hardening.

---

## B. What is still outstanding for UDOC (priority order)

Aligned with external review + Capstone constraints.

### P0 — Must pass before claiming “UDOC Capstone complete”

| Item | Why | Done when |
|------|-----|-----------|
| **Live P6 matrix** | Demo parity is operator fact, not commit SHA | Biased BLOCK on surfaces 1–5; smoke A+B+(C\|C2) |
| **Honesty freeze** | No overclaim StayChain/hardware/commercial | Valuation docs already point gaps |

### P1 — Before *any* external pilot org (test clientele)

| Item | Current state | Required |
|------|---------------|----------|
| **Identity** | Basic JWT login · seed admin · no MFA · no recovery · no invite flow | MFA · password reset · org invite · session revoke · API tokens |
| **Tenant isolation** | `tenant_id` / tenants/me exist; **not proven** cross-tenant hard isolation | Automated test: tenant A cannot read B’s models/decisions/cases |
| **Roles/permissions** | Role strings + portal base_role gates | Documented RBAC matrix enforced server-side on every write |
| **Backups + restore drill** | Neon free; no documented restore | Encrypted backup · restore-tested runbook · RPO/RTO numbers |
| **Monitoring** | `/health` only | Structured logs · error rate · latency · alert on 5xx / DB down |
| **Support path** | None | Who gets paged · how pilot reports bugs |

### P2 — Before leaving free hosting for paid startup stack

| Item | Required |
|------|----------|
| **Paid always-on compute** | Core no cold-start for pilot SLAs |
| **Production DB tier** | Neon paid or equivalent · migrations versioned · rollback · retention |
| **DR** | Documented recover-from-scratch if Render gone (repo + DB backup + env map) |
| **Security sprint** | Threat model · dependency audit · rate limits · secrets rotation · CORS/CSP review |
| **Schema + index review** | Decision/oversight growth under pilot load |
| **Legal/ops** | Pre-registration honesty · POPIA processing notice · DPA template for pilots |

### P3 — Hardware functional setup (Carnarvon / node)

| Item | Status |
|------|--------|
| Hardware bring-up dirs | Architecture present |
| Self-test · sensors · UPS · failover runbooks | **Not operational** |
| Software loop on node | Same Core bootloaders — **valid** once infra exists |

**Do not** block Capstone software valuation on hardware. **Do** block “UDOC appliance product” claims until P3 ops exist.

### Explicitly defer (reviewer agrees)

- GIS Intelligence product depth  
- GBS franchise runtime  
- Recursive AI  
- New Canon volumes for ADR/domain/events **unless** implementation forces them  

---

## C. SaaS readiness scorecard (repo + live, not marketing)

| Area | Score | Note |
|------|------:|------|
| Documentation | 9–10 | Canon modular; freeze v1 |
| Repository structure | 9 | Platform shape |
| Governance model / EVA | 9 | Deterministic philosophy live |
| UDOC UI density vs demos | 7–8 | Much improved; P6 live still required |
| Backend structure | 8 | Core routers + engines |
| Security readiness | 5–6 | Basic auth; MFA/isolation unproven |
| Multi-tenancy | 5 | Fields exist; isolation unproven |
| Operations / monitoring | 5 | Health only |
| Disaster recovery | 4–5 | Not restore-tested |
| Production infrastructure | 5–6 | Free tier limits |
| Hardware integration | 6–7 | Docs > ops |
| **Commercial SaaS** | **~5–6** | Not ready |
| **Friendly pilot** | **~6** | After P1 |

---

## D. Recommended sequence (executable)

```
1. YOU: walk UDOC_SMOKE_PASS + P6 live → report fails
2. Fix only failed live surfaces (Task 2 close)
3. Freeze UDOC Capstone software bar
4. P1 identity + tenant isolation tests (still can stay on free/Neon while coding)
5. Backup/restore + minimal monitoring
6. 3–5 breaker pilot orgs (no revenue target)
7. Fix what pilots break → freeze UDOC v1.0 product
8. Then paid hosting + GIS/GBS/Intelligence on top
```

**Question every new module must answer:** *Which Canon document does this implement?*  
If none — do not add it yet.

---

## E. Direct answers

**Is UDOC SaaS-ready for test clientele today?**  
No. Capstone/demo and internal operator use: yes (after live P6 green). External orgs: only after P1 identity + tenancy proof + backup story.

**Is it hardware-functional ready?**  
No. Software bootloaders are portable; appliance ops are not.

**What work before leaving free hosting?**  
P0 live matrix + P1 identity/tenancy/backups/monitoring minimum; then paid Core + DB with restore drill. Not more features.

**GIS/GBS next?**  
Only after UDOC Stage 1–4 above. UDOC is the platform underneath.

---

## F. Related files

- `UDOC_LIVE_ENVIRONMENTS.md` — hosts & routing  
- `UDOC_SMOKE_PASS.md` · `P6_ASSESSOR_SIDE_BY_SIDE.md`  
- `UDOC_V93_DEMO67_PATENT_CONTROLS.md` — demos 6–7 gaps  
- `TASK2_DEMO_PARITY_STATUS.md`  
- `docs/vol-10-infrastructure/13-render-deployment.md` — free-tier honesty  
