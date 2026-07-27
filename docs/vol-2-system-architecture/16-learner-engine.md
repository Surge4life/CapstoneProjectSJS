# Chapter 16 — Learner Engine

## Purpose

The Learner Engine manages the complete lifecycle of an individual learner within the SETHS division — from initial registration through skills development, opportunity discovery, application, employment, and ongoing career tracking.

---

## Location

- **Router:** `platform-core/app/routers/seths.py` (learner routes)
- **Router:** `platform-core/app/routers/portals_student.py`
- **Service:** `platform-core/app/services/cetcte_engine.py` (reintegration)
- **Frontend:** `seths-app`, `portals-web` (student portal)
- **Mobile:** `seths-mobile`

---

## Learner Profile Architecture

A learner's profile is composed of several layers:

```
Learner (core identity, POPIA-protected)
  ├── Skills Profile (self-declared + verified)
  ├── Education Record (NQF levels, institutions, years)
  ├── Document Vault (CV, certificates — SHA-256 sealed)
  ├── Application History (all applications, outcomes)
  ├── Employment History (roles held via SETHS)
  ├── CETCTE Record (if reintegration programme participant)
  └── Governance Record (decisions affecting this learner)
```

---

## POPIA Compliance in the Learner Engine

Learner data is the most sensitive data in the G.O.D.S ecosystem. POPIA compliance is enforced at every layer:

**Lawful processing basis:** Every processing operation on learner data is tagged with its POPIA basis:
- `consent` — learner has actively consented (used for most data)
- `contract` — processing necessary for the employment application contract
- `legal_obligation` — processing required by law (Employment Equity Act reporting)
- `legitimate_interest` — with balancing test documented in the privacy policy

**Data minimisation:** Only data necessary for the declared purpose is collected. The `id_number` field, for example, is only required if the learner has consented to identity verification.

**Right to access:** Every learner can request a complete export of all data held about them via `GET /seths/learners/{id}/data-export`. The export is generated within 24 hours and delivered as a JSON file. The export request is recorded in the audit chain.

**Right to erasure:** A learner can request deletion of their account. This triggers a soft-delete with a 30-day retention period (to allow pending applications to resolve). After 30 days, personal data is anonymised — the learner record is retained for governance analytics but all PII is replaced with pseudonymous identifiers.

---

## Skills Profile

The skills profile is built from three sources:

1. **Self-declared:** The learner adds skills directly
2. **Verified:** Skills confirmed by a qualification certificate (the document engine verifies the document; the NQF level is extracted and tagged to relevant skills)
3. **Earned:** Skills acquired through G.O.D.S-certified programmes (issued by the Certification Engine)

Skills have a `verification_level`:
- `declared` — learner says they have this skill
- `evidenced` — supporting document uploaded and sealed
- `certified` — G.O.D.S-certified programme completion record

Opportunity matching prioritises `certified` > `evidenced` > `declared` skills.

---

## Opportunity Matching

The learner engine uses G.O.D.S Intelligence to produce opportunity recommendations:

```python
async def get_recommendations(learner_id: UUID) -> list[OpportunityMatch]:
    learner = await db.get_learner_with_profile(learner_id)

    # Construct the matching query for G.O.D.S Intelligence
    query = build_matching_query(learner)

    # Retrieve similar opportunities from the corpus
    # (Active opportunities are indexed in OpenSearch)
    matches = await intelligence.find_similar_opportunities(
        skills=learner.skills,
        nqf_level=learner.nqf_level,
        location=learner.location_province,
        remote_preference=learner.remote_preference
    )

    # GBS check on the match results
    # (Ensures the matching didn't produce biased recommendations)
    governed_matches = await gbs.validate_matches(matches, learner)

    return governed_matches[:10]  # Top 10 recommendations
```

---

## CETCTE Reintegration Support

Learners flagged as `cetcte_enrolled` receive additional services:

- **Anonymised matching:** Their application is presented to employers without identity information in the initial stage. Employers see a skills and experience profile only. Identity disclosure happens only when the employer actively requests to proceed.
- **Support plan:** A structured reintegration support plan is created and tracked
- **Elevated GBS scrutiny:** EVA fairness and societal impact thresholds are elevated for decisions affecting CETCTE participants
- **Progress tracking:** Regular check-ins and milestone recording

The CETCTE approach is designed around evidence that anonymous application significantly reduces discrimination in hiring for individuals with certain backgrounds. The constitutional framework (Human Primacy) ensures this anonymity is maintained until the participant gives consent for disclosure.
