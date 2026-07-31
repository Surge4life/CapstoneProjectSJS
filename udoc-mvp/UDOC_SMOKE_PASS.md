# UDOC Smoke Pass · minimum live checklist

**SoT for close:** operator completes `SMOKE_EVIDENCE_TEMPLATE.md` against **live** Render hosts.  
**Detail matrix:** `P6_ASSESSOR_SIDE_BY_SIDE.md`  
**Constraints:** Neon ≤500MB · existing operator only · no new registration required for pass.

---

## Pass definition (minimum)

| ID | Check | Pass when |
|----|-------|-----------|
| A1 | `GET /health` | 200 / healthy |
| A2 | `GET /udoc/demo/ready` | ready (model-001 + ACTIVE demo pack) |
| B1 | Sentinel Fair (or healthy) EVA | decision **≠ BLOCK** |
| B2 | Sentinel **Biased** EVA | decision **= BLOCK** |
| C1 | Client Govern Fair | **≠ BLOCK** |
| C2 | Client Govern **Biased** | **= BLOCK** |

**Task 2 close:** A1 + A2 + B2 + C2 all green on live hosts (hard-refresh).  
Citizen + Gateway + package split are Capstone completeness items; biased BLOCK is the governance honesty gate.

---

## Hosts

| Surface | URL |
|---------|-----|
| Core | https://gods-platform-core.onrender.com |
| Sentinel | https://gods-platform-core.onrender.com/Sentinel |
| Client | https://gods-udoc-client.onrender.com |
| Citizen | https://gods-udoc-client.onrender.com/citizen.html |
| Gateway | https://gods-udoc-gateway.onrender.com |
| Admin | https://gods-udoc-admin.onrender.com |

---

## Fail conditions

- Mock / simulated scores instead of live `POST /decisions`  
- Biased path does not BLOCK  
- Smoke requires creating a new user on free Neon  
- New Render service invented for the same surface  

---

## After pass

1. File evidence via `SMOKE_EVIDENCE_TEMPLATE.md`  
2. Mark Task 2 closed in project notes (operator fact)  
3. Only then prioritise GIS/GBS depth or commercial pilot hardening (`UDOC_SAAS_READINESS_GAP.md`)
