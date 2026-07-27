# Chapter 17 — Certification Engine

## Purpose

The Certification Engine issues, tracks, verifies, and revokes formal certifications within the G.O.D.S ecosystem. Certifications are cryptographically sealed governance artefacts — not just database records, but auditable evidence of achievement, compliance, or authorisation.

---

## Location

- **Router:** `platform-core/app/routers/gis.py` (certification routes)
- **Service:** `platform-core/app/services/gis_engine.py`
- **Engine:** `governance-engines/gis/`
- **Model:** Certification records managed in the GIS participant registry

---

## Certification Structure

Every G.O.D.S certification contains:

```json
{
  "certification_id": "uuid",
  "certification_type": "SETHS_CERTIFIED_LEARNER",
  "recipient": {
    "participant_id": "uuid",
    "name": "Firstname Lastname",
    "participant_type": "individual"
  },
  "issuer": {
    "entity": "G.O.D.S Holdings (Pty) Ltd (proposed)",
    "issued_by_id": "uuid",
    "issued_by_role": "compliance"
  },
  "programme": "National Certificate: IT Support NQF Level 5",
  "nqf_level": 5,
  "scope": "South Africa",
  "issued_at": "2025-03-15T09:00:00Z",
  "valid_until": "2028-03-14T23:59:59Z",
  "status": "active",
  "seal": "HMAC-SHA256:abc123...",
  "audit_ref_id": "uuid",
  "verification_url": "https://platform.gods.internal/verify/uuid"
}
```

The `seal` is computed over the certification content using the platform's HSM key. A verifier can check the seal against the public key to confirm the certification is genuine and unmodified.

---

## Certification Types in Detail

### `AI_MODEL_GOVERNANCE`

Issued to: AI operators  
Conditions: Model has completed UDOC registration review, conformance scans pass, compliance officer approves  
Validity: 12 months (renewable)  
Renewal: Requires a fresh conformance scan and compliance review  
Revocation trigger: Model suspended for governance violations

### `EMPLOYER_VERIFIED`

Issued to: Employers  
Conditions: CIPC registration verified, contact details confirmed, Employment Equity status declared  
Validity: 24 months  
Renewal: Requires re-verification of CIPC status and updated EE declaration  
Revocation trigger: CIPC deregistration, governance violations, non-compliance with bias remediation plans

### `SKILLS_PROVIDER`

Issued to: Training organisations, TVET colleges, universities  
Conditions: NQF registration (SAQA/QCTO), governance agreement executed, curriculum review  
Validity: 36 months  
Impact: Learners who complete programmes from certified skills providers receive `certified` level skill verification

### `SETHS_CERTIFIED_LEARNER`

Issued to: Individual learners  
Conditions: Completion of a G.O.D.S-certified programme from a certified skills provider, assessment results recorded  
Validity: Permanent (skills don't expire — but may be superseded by higher-level certifications)  
Impact: Learners with this certification are prioritised in the G.O.D.S opportunity matching engine

### `FRANCHISE_OPERATOR`

Issued to: Organisations operating G.O.D.S franchised deployments  
Conditions: Franchise agreement executed, governance audit passed, technical deployment verified  
Validity: 12 months  
Renewal: Annual governance audit

---

## Certification Verification API

Anyone can verify a G.O.D.S certification without authentication:

```
GET /verify/{certification_id}
```

**Response:**
```json
{
  "valid": true,
  "certification_id": "uuid",
  "certification_type": "EMPLOYER_VERIFIED",
  "recipient_name": "Acme Corp",
  "issued_at": "2025-01-01",
  "valid_until": "2027-01-01",
  "status": "active",
  "seal_verified": true
}
```

Or for revoked/expired:
```json
{
  "valid": false,
  "status": "revoked",
  "revoked_at": "2025-06-15",
  "revocation_reason": "CIPC deregistration confirmed"
}
```

This endpoint requires no authentication — it is the public verification interface. Importantly, it reveals only the certification status and public metadata. No PII beyond the recipient's name (which they consented to by accepting the certification).

---

## Revocation

Certification revocation is immediate and permanent:

1. Compliance officer triggers revocation with a documented reason
2. Certification status set to `revoked` in the database
3. Revocation recorded in the audit chain with officer identity and reason
4. Kafka event published — all edge nodes receive the revocation
5. Any governance decisions that relied on the certification status are flagged for review
6. Notification sent to the certificate holder

A revoked certification cannot be un-revoked. If the circumstances change, a new certification is issued. This maintains the permanent truth of the audit record.
