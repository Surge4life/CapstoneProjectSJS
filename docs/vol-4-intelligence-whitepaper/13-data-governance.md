# Chapter 13 — Data Governance

## Intelligence System Data Governance

The G.O.D.S Intelligence system processes several categories of data, each with distinct governance requirements. This chapter documents the data governance framework for the intelligence system.

---

## Data Categories

### Category 1: Corpus Documents (Institutional Knowledge)

**Nature:** Documents uploaded by the institution to power the intelligence system.  
**POPIA basis:** Legitimate interest (knowledge management); consent where documents contain personal data.  
**Retention:** Indefinite — documents are never automatically deleted. Archiving is manual and audited.  
**Access:** Tier-based access control; always tenant-scoped.  
**Transfer:** Cannot be transferred outside the institution without explicit authorisation.  
**Subject rights:** If a corpus document contains personal data about an identifiable individual, that individual has POPIA subject rights over that data.

### Category 2: Query Records (User Queries and Responses)

**Nature:** Records of what users asked and what the system answered.  
**POPIA basis:** Contract (service delivery); legitimate interest (auditability).  
**Retention:** 3 years in queryable PostgreSQL; permanent in Cassandra audit chain.  
**Access:** User (own queries), compliance officers (all), external auditors (read-only).  
**Subject rights:** Users can request access to their own query records under POPIA Section 23. They cannot request deletion (audit chain immutability overrides erasure for governance records).

### Category 3: Calibration Data (User Feedback)

**Nature:** Thumbs up/down ratings on intelligence responses, linked to query records.  
**POPIA basis:** Consent (user actively provides the rating).  
**Retention:** 3 years.  
**Access:** Internal analytics only; never shared with external services.  
**Subject rights:** Standard access and erasure rights apply (except the query record it references, which is immutable).

### Category 4: External Consultation Records

**Nature:** Records of external AI service consultations (not the original query — the sanitised version).  
**POPIA basis:** Legitimate interest (service improvement, accountability).  
**Retention:** 3 years.  
**Special requirement:** The external service consulted must be disclosed to users at the time of consultation and in the privacy policy.

---

## Data Minimisation in Intelligence

The intelligence system applies data minimisation:

- Query text is stored in full (required for auditability)
- Query hash is computed (for integrity verification without re-reading content)
- Personal data within queries is flagged in audit metadata but the query text is retained as-is
- Embedding computations use the document text, not any linked personal data
- External consultation sanitises PII before transmission

---

## POPIA Subject Access Requests

A user can submit a POPIA Section 23 information request to access data the system holds about them. The standard response for intelligence data includes:

1. All query records for the user (from the queryable database)
2. All feedback records for the user
3. Confirmation that query records also exist in the immutable audit chain
4. An explanation of why audit chain records cannot be deleted

Processing time: 30 days from receipt of the request (POPIA requirement).

The request is handled via the data export endpoint:
```
POST /privacy/subject-access-request
Authorization: Bearer <user_token>
{
    "data_categories": ["intelligence_queries", "feedback"]
}
```

---

## Cross-Border Data Governance

G.O.D.S Intelligence, like all parts of the platform, is subject to jurisdictional sovereignty rules. Specifically:

- **Corpus documents** may not be transmitted to another jurisdiction without a cross-border authorisation record
- **Query records** are subject to the same data residency requirements as other operational data
- **External consultation** is treated as a potential cross-border data flow — the external service's data residency must be declared and a cross-border authorisation created

If a deployment is configured as South Africa-jurisdiction, consulting an external service hosted in the EU triggers a cross-border data flow authorisation requirement. This is evaluated automatically when external consultation is configured and must be resolved before external consultation is enabled.
