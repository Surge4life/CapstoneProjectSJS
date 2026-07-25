# Chapter 04 — SETHS Tables

## Schema: `seths`

All SETHS division data lives in the `seths` schema. These tables manage the workforce lifecycle from learner registration through employment.

---

## `seths.learners`

The central record for every individual in the SETHS system.

```sql
CREATE TABLE seths.learners (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL UNIQUE REFERENCES iam.users(id),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),
    
    -- Personal (POPIA-protected — access requires declared basis)
    id_number           VARCHAR(13),        -- RSA ID number — encrypted at rest
    date_of_birth       DATE,
    nationality         VARCHAR(50),
    home_language       VARCHAR(50),
    
    -- Professional profile
    summary             TEXT,
    skills              TEXT[],
    nqf_level           SMALLINT CHECK (nqf_level BETWEEN 1 AND 10),
    years_experience    SMALLINT,
    location_province   VARCHAR(50),
    location_city       VARCHAR(100),
    remote_preference   VARCHAR(20) CHECK (remote_preference IN ('remote', 'hybrid', 'onsite', 'any')),
    
    -- Status
    status              VARCHAR(50) NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active', 'employed', 'inactive', 'suspended')),
    reintegration_flag  BOOLEAN NOT NULL DEFAULT false,
    cetcte_enrolled     BOOLEAN NOT NULL DEFAULT false,
    
    -- Timestamps
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ,
    audit_ref_id        UUID REFERENCES audit.audit_refs(id)
);

CREATE INDEX learners_tenant_idx ON seths.learners(tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX learners_nqf_level_idx ON seths.learners(nqf_level) WHERE deleted_at IS NULL;
CREATE INDEX learners_status_idx ON seths.learners(status) WHERE deleted_at IS NULL;
```

---

## `seths.employers`

Registered employers who post opportunities and hire learners.

```sql
CREATE TABLE seths.employers (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL UNIQUE REFERENCES iam.users(id),
    tenant_id               UUID NOT NULL REFERENCES platform.tenants(id),
    
    company_name            VARCHAR(255) NOT NULL,
    registration_number     VARCHAR(50),     -- CIPC registration number
    industry_sector         VARCHAR(100),
    company_size            VARCHAR(50) CHECK (company_size IN ('micro', 'small', 'medium', 'large', 'enterprise')),
    province                VARCHAR(50),
    
    -- BEE and Equity
    bee_level               SMALLINT CHECK (bee_level BETWEEN 1 AND 8),
    equity_plan_current     BOOLEAN NOT NULL DEFAULT false,
    equity_plan_url         TEXT,
    
    -- Verification
    verification_status     VARCHAR(50) NOT NULL DEFAULT 'pending'
                            CHECK (verification_status IN ('pending', 'verified', 'suspended')),
    verified_at             TIMESTAMPTZ,
    verified_by             UUID REFERENCES iam.users(id),
    
    -- Governance
    bias_score              DECIMAL(5,2),    -- Computed by bias engine, updated periodically
    elevated_scrutiny       BOOLEAN NOT NULL DEFAULT false,
    
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at              TIMESTAMPTZ,
    audit_ref_id            UUID REFERENCES audit.audit_refs(id)
);
```

---

## `seths.opportunities`

Job opportunities posted by verified employers.

```sql
CREATE TABLE seths.opportunities (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employer_id         UUID NOT NULL REFERENCES seths.employers(id),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),
    
    title               VARCHAR(255) NOT NULL,
    description         TEXT NOT NULL,
    requirements        TEXT,
    
    -- Requirements
    min_nqf_level       SMALLINT CHECK (min_nqf_level BETWEEN 1 AND 10),
    max_nqf_level       SMALLINT CHECK (max_nqf_level BETWEEN 1 AND 10),
    required_skills     TEXT[],
    min_experience_years SMALLINT,
    
    -- Location and terms
    province            VARCHAR(50),
    city                VARCHAR(100),
    work_arrangement    VARCHAR(20) CHECK (work_arrangement IN ('remote', 'hybrid', 'onsite')),
    contract_type       VARCHAR(50) CHECK (contract_type IN ('permanent', 'fixed_term', 'contract', 'internship')),
    salary_min          INTEGER,    -- ZAR per month
    salary_max          INTEGER,
    
    -- Status
    status              VARCHAR(50) NOT NULL DEFAULT 'draft'
                        CHECK (status IN ('draft', 'active', 'closed', 'filled', 'withdrawn')),
    published_at        TIMESTAMPTZ,
    closing_date        DATE,
    filled_at           TIMESTAMPTZ,
    
    -- GBS governance
    gbs_review_flag     BOOLEAN NOT NULL DEFAULT false,
    gbs_review_notes    TEXT,
    
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ,
    audit_ref_id        UUID REFERENCES audit.audit_refs(id)
);

CREATE INDEX opportunities_status_idx ON seths.opportunities(status, closing_date)
    WHERE deleted_at IS NULL;
CREATE INDEX opportunities_nqf_idx ON seths.opportunities(min_nqf_level, max_nqf_level)
    WHERE status = 'active' AND deleted_at IS NULL;
```

---

## `seths.applications`

Applications linking learners to opportunities.

```sql
CREATE TABLE seths.applications (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id          UUID NOT NULL REFERENCES seths.learners(id),
    opportunity_id      UUID NOT NULL REFERENCES seths.opportunities(id),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),
    
    status              VARCHAR(50) NOT NULL DEFAULT 'submitted'
                        CHECK (status IN (
                            'submitted', 'under_review', 'shortlisted',
                            'offered', 'accepted', 'rejected', 'withdrawn'
                        )),
    cover_letter        TEXT,
    
    -- Governance linkage
    shortlist_decision_id   UUID REFERENCES governance.decisions(id),
    rejection_decision_id   UUID REFERENCES governance.decisions(id),
    offer_decision_id       UUID REFERENCES governance.decisions(id),
    
    -- Timestamps
    submitted_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reviewed_at         TIMESTAMPTZ,
    shortlisted_at      TIMESTAMPTZ,
    offered_at          TIMESTAMPTZ,
    decided_at          TIMESTAMPTZ,
    
    -- Rejection
    rejection_reason    VARCHAR(100),
    rejection_detail    TEXT,
    
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_ref_id        UUID NOT NULL REFERENCES audit.audit_refs(id),
    
    UNIQUE (learner_id, opportunity_id)
);
```

---

## `seths.documents`

Documents uploaded by learners (CVs, qualifications, supporting documents).

```sql
CREATE TABLE seths.documents (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id          UUID NOT NULL REFERENCES seths.learners(id),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),
    
    document_type       VARCHAR(50) NOT NULL
                        CHECK (document_type IN ('cv', 'qualification', 'id_document', 'reference', 'portfolio', 'other')),
    file_name           VARCHAR(255) NOT NULL,
    file_size_bytes     INTEGER NOT NULL,
    mime_type           VARCHAR(100) NOT NULL,
    
    -- Storage
    storage_key         VARCHAR(500) NOT NULL UNIQUE, -- S3 key
    storage_bucket      VARCHAR(100) NOT NULL,
    
    -- Integrity
    sha256_hash         VARCHAR(64) NOT NULL,   -- SHA-256 of file content
    
    -- UDOC linkage
    udoc_audit_ref_id   UUID REFERENCES audit.audit_refs(id),  -- Sealed to audit chain
    
    -- Metadata
    nqf_level           SMALLINT,       -- If a qualification document
    institution         VARCHAR(255),   -- Issuing institution
    year_obtained       SMALLINT,
    
    uploaded_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ,
    audit_ref_id        UUID REFERENCES audit.audit_refs(id)
);
```
