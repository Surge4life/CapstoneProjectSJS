# Chapter 05 — MADIBA Tables

## Schema: `madiba`

The MADIBA schema stores all capital investment pipeline data, project records, milestone tracking, and investor management.

---

## Table: `madiba.investors`

```sql
CREATE TABLE madiba.investors (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES iam.users(id),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),

    -- Entity identity
    entity_name         VARCHAR(200) NOT NULL,
    entity_type         VARCHAR(50) NOT NULL,
    -- sovereign_fund | institutional | private_equity | development_finance | corporate | individual
    registration_number VARCHAR(50),
    jurisdiction        VARCHAR(10) NOT NULL DEFAULT 'ZA',

    -- Investment profile
    investment_mandate  TEXT,                      -- What sectors/geographies they invest in
    minimum_ticket_size DECIMAL(20,2),             -- Minimum investment in ZAR
    maximum_ticket_size DECIMAL(20,2),
    preferred_sectors   TEXT[],                    -- Array of sector codes

    -- Verification
    verification_status VARCHAR(20) NOT NULL DEFAULT 'unverified',
    verified_at         TIMESTAMPTZ,
    verified_by         UUID REFERENCES iam.users(id),
    kyc_completed       BOOLEAN NOT NULL DEFAULT false,
    aml_checked         BOOLEAN NOT NULL DEFAULT false,

    -- GIS certification
    certification_id    UUID,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by          UUID NOT NULL REFERENCES iam.users(id),
    audit_ref_id        UUID NOT NULL
);
```

---

## Table: `madiba.projects`

```sql
CREATE TABLE madiba.projects (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),
    submitted_by        UUID NOT NULL REFERENCES iam.users(id),

    -- Project identity
    project_name        VARCHAR(200) NOT NULL,
    project_code        VARCHAR(50) UNIQUE,
    description         TEXT NOT NULL,
    sector              VARCHAR(50) NOT NULL,
    province            VARCHAR(50),
    municipality        VARCHAR(100),

    -- Capital requirements
    capital_required    DECIMAL(20,2) NOT NULL,
    capital_currency    CHAR(3) NOT NULL DEFAULT 'ZAR',
    capital_committed   DECIMAL(20,2) NOT NULL DEFAULT 0,
    capital_deployed    DECIMAL(20,2) NOT NULL DEFAULT 0,

    -- Project lifecycle
    status              VARCHAR(30) NOT NULL DEFAULT 'submitted',
    -- submitted | under_review | approved | funded | active | completed | suspended | cancelled
    target_start_date   DATE,
    target_end_date     DATE,
    actual_start_date   DATE,
    actual_end_date     DATE,

    -- Governance
    governance_outcome  VARCHAR(20),              -- From GBS path on submission
    last_governance_decision_id UUID,
    compliance_flags    JSONB DEFAULT '[]',

    -- Impact metrics
    jobs_projected      INTEGER,
    jobs_actual         INTEGER,
    beneficiary_count   INTEGER,
    sdg_alignment       TEXT[],                   -- UN SDG goals this project supports

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_ref_id        UUID NOT NULL
);

CREATE INDEX madiba_projects_status_idx ON madiba.projects(status);
CREATE INDEX madiba_projects_sector_idx ON madiba.projects(sector);
CREATE INDEX madiba_projects_tenant_idx ON madiba.projects(tenant_id);
```

---

## Table: `madiba.milestones`

```sql
CREATE TABLE madiba.milestones (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id          UUID NOT NULL REFERENCES madiba.projects(id),
    milestone_name      VARCHAR(200) NOT NULL,
    description         TEXT,
    sequence_number     INTEGER NOT NULL,

    -- Completion criteria
    completion_criteria TEXT NOT NULL,
    evidence_required   BOOLEAN NOT NULL DEFAULT true,

    -- Status
    status              VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending | in_progress | completed | missed | deferred
    target_date         DATE NOT NULL,
    completed_at        TIMESTAMPTZ,
    completed_by        UUID REFERENCES iam.users(id),

    -- Evidence
    evidence_document_id UUID,                    -- Reference to document store
    evidence_notes      TEXT,

    -- Capital release (milestone-based disbursement)
    capital_release_amount DECIMAL(20,2),         -- Capital released on completion
    capital_released    BOOLEAN NOT NULL DEFAULT false,
    capital_released_at TIMESTAMPTZ,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_ref_id        UUID NOT NULL
);

CREATE INDEX madiba_milestones_project_idx ON madiba.milestones(project_id, sequence_number);
CREATE INDEX madiba_milestones_status_idx ON madiba.milestones(status);
CREATE INDEX madiba_milestones_target_date_idx ON madiba.milestones(target_date);
```

---

## Table: `madiba.capital_allocations`

Records of capital assignments from investors to projects.

```sql
CREATE TABLE madiba.capital_allocations (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id          UUID NOT NULL REFERENCES madiba.projects(id),
    investor_id         UUID NOT NULL REFERENCES madiba.investors(id),
    
    amount              DECIMAL(20,2) NOT NULL,
    currency            CHAR(3) NOT NULL DEFAULT 'ZAR',
    allocation_type     VARCHAR(30) NOT NULL,
    -- equity | debt | grant | blended_finance | guarantee

    -- Governance
    governance_decision_id UUID,
    governance_outcome  VARCHAR(20) NOT NULL,

    -- Disbursement
    disbursement_schedule JSONB,                  -- Array of {date, amount} objects
    amount_disbursed    DECIMAL(20,2) NOT NULL DEFAULT 0,

    status              VARCHAR(20) NOT NULL DEFAULT 'committed',
    -- committed | active | completed | cancelled
    committed_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    activated_at        TIMESTAMPTZ,
    completed_at        TIMESTAMPTZ,
    
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_ref_id        UUID NOT NULL
);

CREATE INDEX madiba_allocations_project_idx ON madiba.capital_allocations(project_id);
CREATE INDEX madiba_allocations_investor_idx ON madiba.capital_allocations(investor_id);
```
