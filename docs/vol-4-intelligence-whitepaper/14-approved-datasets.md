# Chapter 14 — Approved Datasets

## What Are Approved Datasets?

Approved datasets are the curated set of knowledge sources that G.O.D.S has evaluated and deemed appropriate for use in the corpus. They are not the only sources that can be added — institutions can add their own documents. But the approved datasets list represents sources that have been reviewed for:

- Copyright suitability
- Evidence quality and reliability
- Jurisdiction relevance
- Political and institutional neutrality

---

## Core Approved Datasets (Platform Corpus)

These datasets are maintained by G.O.D.S Holdings in the platform corpus and are available to licensed tenants.

### South African Legislative Corpus

| Source | Format | Coverage | Update Frequency |
|--------|--------|---------|-----------------|
| Government Gazette | PDF → Text | All gazettes from 2010 | Weekly |
| Acts of Parliament | PDF → Text | All acts + amendments | On new act/amendment |
| Regulations | PDF → Text | All regulation gazettes | Weekly |
| Constitutional Court judgments | PDF → Text | All published judgments | Bi-weekly |

**Copyright status:** South African government publications are generally available for reproduction under the South African Government's open access policy. Citations are required.

### Employment and Labour Corpus

| Source | Coverage | Tier |
|--------|---------|------|
| Employment Equity Act and amendments | Complete | 1 |
| Labour Relations Act and amendments | Complete | 1 |
| Basic Conditions of Employment Act | Complete | 1 |
| CCMA guidelines and awards (selected) | Selected | 2 |
| Department of Employment and Labour guidance | Complete | 2 |

### Education and Qualifications Corpus

| Source | Coverage | Tier |
|--------|---------|------|
| NQF Act and regulations | Complete | 1 |
| SAQA framework documents | Complete | 1 |
| QCTO qualification standards (selected) | Selected NQF levels | 2 |
| DHET policy documents | Selected | 2 |

### POPIA and Data Governance

| Source | Coverage | Tier |
|--------|---------|------|
| Protection of Personal Information Act (POPIA) | Complete | 1 |
| Information Regulator guidance notes | Complete | 2 |
| POPIA regulations | Complete | 1 |

---

## Institution-Specific Approved Datasets

Institutions can designate their own approved datasets — curated sets of documents that are pre-cleared for corpus inclusion by the institution's compliance and legal teams.

An approved dataset has:
- A name and description
- A designated maintainer (the person responsible for keeping it current)
- A copyright clearance record
- A review schedule
- An expiry date (after which the dataset is flagged for re-review)

---

## Prohibited Content in the Corpus

Some content types are prohibited from the G.O.D.S corpus regardless of copyright status:

| Prohibited | Reason |
|-----------|--------|
| Extremist content | Constitutional fairness limit |
| Content that discriminates on protected characteristics | Constitutional fairness limit |
| Misinformation (demonstrably false factual claims) | Evidence hierarchy integrity |
| Confidential third-party information | Privacy and legal |
| Personal health information of identifiable individuals | POPIA special information |
| Biometric data | POPIA special information |
| Sexual content | Inappropriate for institutional use |

The prohibition is enforced by:
1. Corpus manager review (manual check on upload)
2. Automated content scanning (for known prohibited categories)
3. Corpus audits (periodic review of existing content)

Any document found to violate the prohibited content rules after upload is immediately archived (not deleted — the audit record of the prohibition violation is retained) and an incident report is created.

---

## Dataset Freshness

Governance is time-sensitive. A corpus built on outdated legislation gives outdated answers. The platform tracks dataset freshness:

- Each approved dataset has a `last_verified` date
- Datasets older than their scheduled review date are flagged as `STALE`
- Queries that rely primarily on stale datasets receive a freshness warning in the response
- Corpus managers receive weekly freshness reports

**Freshness warning in response:**
> "Note: Some sources used in this response may be out of date. The [Employment and Labour Corpus] was last verified [date]. Please verify against the current legislation before making decisions."
