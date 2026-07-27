# Chapter 06 — TS Industries Tables

## Schema: `ts`

The TS schema stores industrial project pipeline data, sector registry, partner management, and government project office records.

---

## Table: `ts.sectors`

```sql
CREATE TABLE ts.sectors (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sector_code     VARCHAR(20) UNIQUE NOT NULL,
    sector_name     VARCHAR(100) NOT NULL,
    description     TEXT,

    -- Governance configuration for this sector
    eva_weight_rc_override DECIMAL(4,3),           -- Override RC weight for this sector
    eva_weight_si_override DECIMAL(4,3),           -- Override SI weight
    policy_pack_id  UUID,                          -- Sector-specific policy pack (optional)

    -- Regulatory context
    primary_legislation TEXT[],                    -- Acts governing this sector
    regulator       VARCHAR(100),                  -- Primary regulatory body

    active          BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed data
INSERT INTO ts.sectors (sector_code, sector_name, regulator) VALUES
    ('ENERGY', 'Energy', 'NERSA'),
    ('INFRASTRUCTURE', 'Infrastructure', 'CIDB'),
    ('MANUFACTURING', 'Manufacturing', 'DTI'),
    ('AGRICULTURE', 'Agriculture', 'DALRRD'),
    ('TECHNOLOGY', 'Technology', 'DCDT'),
    ('MINING', 'Mining', 'DMRE'),
    ('WATER', 'Water & Sanitation', 'DWS'),
    ('HEALTH', 'Healthcare Infrastructure', 'DOH'),
    ('EDUCATION', 'Education Infrastructure', 'DBE'),
    ('TRANSPORT', 'Transport', 'DOT');
```

---

## Table: `ts.projects`

```sql
CREATE TABLE ts.projects (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),
    submitted_by        UUID NOT NULL REFERENCES iam.users(id),

    -- Project identity
    project_name        VARCHAR(200) NOT NULL,
    project_code        VARCHAR(50) UNIQUE,
    sector_id           UUID NOT NULL REFERENCES ts.sectors(id),
    description         TEXT NOT NULL,

    -- Location
    province            VARCHAR(50) NOT NULL,
    municipality        VARCHAR(100),
    gps_coordinates     POINT,                    -- PostGIS for geo queries (optional)

    -- Project scale
    estimated_value     DECIMAL(20,2),
    currency            CHAR(3) NOT NULL DEFAULT 'ZAR',
    duration_months     INTEGER,
    job_creation_target INTEGER,

    -- Submission type
    submission_type     VARCHAR(30) NOT NULL,
    -- new_build | expansion | rehabilitation | maintenance | feasibility

    -- Status
    status              VARCHAR(30) NOT NULL DEFAULT 'submitted',
    -- submitted | under_review | approved | tendering | awarded | active | completed | suspended | cancelled

    -- Governance
    governance_outcome  VARCHAR(20),
    governance_decision_id UUID,
    compliance_review_required BOOLEAN NOT NULL DEFAULT false,
    compliance_review_status VARCHAR(20),

    -- Government project office
    gpo_reference       VARCHAR(100),             -- Government project office reference number
    project_type        VARCHAR(30),
    -- public_private_partnership | public_works | municipal_infrastructure | sez | other

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_ref_id        UUID NOT NULL
);

CREATE INDEX ts_projects_sector_idx ON ts.projects(sector_id);
CREATE INDEX ts_projects_status_idx ON ts.projects(status);
CREATE INDEX ts_projects_province_idx ON ts.projects(province);
CREATE INDEX ts_projects_submitted_by_idx ON ts.projects(submitted_by);
```

---

## Table: `ts.partners`

Build assistant partners — organisations that deliver project components.

```sql
CREATE TABLE ts.partners (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID REFERENCES iam.users(id),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),

    -- Entity identity
    company_name        VARCHAR(200) NOT NULL,
    registration_number VARCHAR(50),              -- CIPC number
    cidb_grading        VARCHAR(10),              -- CIDB contractor grading
    bee_level           INTEGER CHECK (bee_level BETWEEN 1 AND 8),

    -- Capabilities
    sector_capabilities UUID[],                   -- References to ts.sectors.id
    specialisations     TEXT[],
    max_project_value   DECIMAL(20,2),

    -- Verification
    verification_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    verified_at         TIMESTAMPTZ,
    verified_by         UUID REFERENCES iam.users(id),
    cidb_verified       BOOLEAN NOT NULL DEFAULT false,
    cipc_verified       BOOLEAN NOT NULL DEFAULT false,

    -- GIS certification
    certification_id    UUID,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_ref_id        UUID NOT NULL
);

CREATE INDEX ts_partners_sector_idx ON ts.partners USING GIN(sector_capabilities);
CREATE INDEX ts_partners_verification_idx ON ts.partners(verification_status);
```

---

## Table: `ts.project_partners`

Assignment of partners to projects.

```sql
CREATE TABLE ts.project_partners (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id          UUID NOT NULL REFERENCES ts.projects(id),
    partner_id          UUID NOT NULL REFERENCES ts.partners(id),
    role                VARCHAR(50) NOT NULL,
    -- lead_contractor | subcontractor | specialist | consultant | supplier
    scope_of_work       TEXT NOT NULL,
    contract_value      DECIMAL(20,2),
    assigned_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    assigned_by         UUID NOT NULL REFERENCES iam.users(id),
    governance_decision_id UUID,                  -- GBS governance of this assignment
    audit_ref_id        UUID NOT NULL,

    CONSTRAINT ts_project_partners_unique UNIQUE (project_id, partner_id, role)
);
```
