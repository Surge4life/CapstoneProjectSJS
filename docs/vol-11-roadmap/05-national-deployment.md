# Chapter 05 — National Deployment (Year 5–10)

## What National Deployment Means

National deployment means G.O.D.S is operating as the governance infrastructure for AI in South Africa — not as a startup product, but as foundational digital infrastructure at the scale of the country's AI activity.

This is an ambitious claim. It requires:
1. Proven track record from Pilot and Regional phases
2. Formal regulatory recognition
3. National government partnership (or at minimum, endorsement)
4. Technical infrastructure that can serve national-scale load
5. A governance framework that has been tested and refined over years

---

## Target Milestones for National Deployment

### Year 5 Entry Criteria

Before national deployment can begin, the following must be true:
- G.O.D.S Holdings is formally registered and capitalised
- Regional expansion is operational in at least 4 provinces
- Pilot compliance audit shows zero material findings
- Formal MOU with at least one government department (DOEL, DSAC, or DTPS)
- POPIA compliance endorsement from Information Regulator

---

## National Infrastructure Requirements

A national deployment at scale requires infrastructure beyond the current Render deployment:

| Component | Pilot/Regional | National Scale |
|-----------|---------------|---------------|
| Daily governance decisions | 10,000–100,000 | 1,000,000+ |
| Concurrent users | 100–500 | 10,000+ |
| Data residency | Render cloud | SA-hosted (SITA or private DC) |
| Disaster recovery | Single region | Multi-region SA |
| Cassandra nodes | 3 | 9 (3 per DC, 3 DCs) |
| platform-core pods | 3–5 | 20–50 |

At national scale, cloud-only deployment may no longer be appropriate. The Department of Communications requires government data to be stored in South Africa — not in international cloud regions. Options:
- SA-based cloud providers (AWS af-south-1, Azure South Africa North)
- Government data centres (SITA cloud)
- G.O.D.S-operated private infrastructure

---

## National Use Cases by Division

### SETHS at National Scale

- National employment equity database — real-time tracking of EEA compliance across all registered employers
- NQF integration — direct integration with SAQA for qualification verification
- Government employment (DPSA) — governance of AI in civil service hiring
- TVET college integration — direct pathway from qualification completion to opportunity matching
- Statistics SA reporting — employment equity metrics contributed to national labour market data

### UDOC at National Scale

- National AI model registry — all AI systems operating in South Africa registered
- Sector-specific governance — financial, healthcare, criminal justice each with appropriate standards
- Cross-border governance — AI systems operating across SADC region subject to sovereignty verification
- National AI incident reporting — governance failures reported to national oversight body

### TS Industries at National Scale

- Integration with the National Infrastructure Plan — G.O.D.S as the governance layer for infrastructure AI
- Public-private partnership governance — AI in PPP procurement and management
- Special Economic Zones — AI governance for SEZ development projects

---

## Government Partnership Structure

The national deployment model requires a formal government partnership:

```
G.O.D.S Holdings (Pty) Ltd (platform operator)
    ↓ Service Level Agreement
National Government Partner
(e.g., Department of Employment and Labour for SETHS;
 Department of Communications for UDOC)
    ↓
Government deploys G.O.D.S as national AI governance infrastructure
    ↓
Other departments and agencies are tenants
```

The government retains sovereignty over the governance data. G.O.D.S Holdings operates the platform but cannot access government data without authorisation. The audit chain is under joint custody: G.O.D.S Holdings operates it, but the government partner holds a mirrored copy.

---

## National Policy Framework

By Year 8, the G.O.D.S constitutional framework should be influential on national AI policy:

- The EVA framework as a reference model for AI governance assessment
- The GBS Runtime as a model for how governance automation should work
- The UDOC model registry as the foundation for a National AI Register
- The SETHS employment equity monitoring as the technical layer for EEA enforcement

These are aspirations, not guarantees. But a platform that has governed millions of AI decisions over 5 years has earned the credibility to inform policy.
