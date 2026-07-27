# Chapter 13 — Franchise Engine (GIS)

## Purpose

The Franchise Engine — implemented as the GIS (GBS-SETHS Intelligence & Franchise Layer) governance engine — manages the franchise and certification infrastructure of the G.O.D.S ecosystem. It governs how organisations become authorised G.O.D.S franchise operators, how certifications are issued and tracked, and how the franchise network is maintained.

---

## Location

- **Router:** `platform-core/app/routers/gis.py`
- **Service:** `platform-core/app/services/gis_engine.py`
- **Engine:** `governance-engines/gis/` — Node.js franchise governance engine

---

## What the Franchise Engine Manages

### 1. Franchise Registration

Organisations that want to operate a G.O.D.S instance as a franchised deployment must register through the franchise engine. A franchise operator:
- Has agreed to the G.O.D.S franchise governance standards
- Is accountable for operating the platform within constitutional bounds
- Can onboard clients (as tenants) within their franchise territory
- Reports to the G.O.D.S platform operator (Sashin J. Singh / G.O.D.S Holdings)

The franchise registration process:
1. Organisation submits franchise application (via the GIS portal)
2. G.O.D.S platform operator reviews the application
3. If approved: franchise agreement executed, franchise configuration provisioned
4. Franchise operator can begin onboarding clients as tenants

### 2. Certifications

The GIS engine issues and tracks certifications within the G.O.D.S ecosystem:

| Certification Type | Who Receives It | What It Certifies |
|-------------------|----------------|------------------|
| `AI_MODEL_GOVERNANCE` | AI operators | Their model has passed UDOC certification |
| `EMPLOYER_VERIFIED` | Employers | Employer identity and legal standing verified |
| `SKILLS_PROVIDER` | Training organisations | Authorised to issue G.O.D.S-recognised qualifications |
| `FRANCHISE_OPERATOR` | Franchise organisations | Authorised to operate a G.O.D.S franchise |
| `SETHS_CERTIFIED_LEARNER` | Learners | Completed a G.O.D.S-certified skills programme |

Certifications are versioned, time-limited, and revocable. A revoked certification is recorded in the audit chain and cannot be silently un-revoked.

### 3. Participant Registry

Every person, organisation, and AI model in the G.O.D.S ecosystem is a participant. The GIS engine maintains the participant registry — a cross-divisional record of participation status.

A participant's status in the registry determines what they can do across the ecosystem. A learner who is suspended from the SETHS division has their participant status updated, which affects their access across all connected G.O.D.S instances.

### 4. Pledge Management

Participants can make governance pledges — formal declarations of intent to operate within specific governance standards. Pledges are:
- Recorded in the audit chain
- Referenced in governance decisions (a participant who has pledged to a standard receives marginally different EVA scoring in relevant dimensions)
- Revocable (with an audit record of the revocation)

---

## GIS Engine Interface

The GIS engine (`governance-engines/gis/`) exposes a REST API consumed by `platform-core`:

```
GET  /gis/participants/{id}           — Get participant record
POST /gis/participants                — Register a new participant  
POST /gis/certifications/issue        — Issue a certification
POST /gis/certifications/{id}/revoke  — Revoke a certification
GET  /gis/franchises                  — List franchise operators
POST /gis/franchises                  — Register a franchise
GET  /gis/pledges/{participant_id}    — Get participant's pledges
POST /gis/pledges                     — Record a new pledge
```

All GIS operations are governance-path operations — they produce audit records via the standard `event_bus`.
