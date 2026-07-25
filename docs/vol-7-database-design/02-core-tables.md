# Chapter 02 — Core Tables

## IAM Schema — Identity and Access Management

### `iam.users`

The central user identity table. Every person who interacts with the G.O.D.S ecosystem has a record here.

```sql
CREATE TABLE iam.users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) NOT NULL UNIQUE,
    email_verified  BOOLEAN NOT NULL DEFAULT false,
    password_hash   VARCHAR(255) NOT NULL,  -- bcrypt, cost=12
    full_name       VARCHAR(255) NOT NULL,
    status          VARCHAR(50) NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'suspended', 'pending_verification', 'deactivated')),
    division        VARCHAR(50)
                    CHECK (division IN ('udoc', 'seths', 'madiba', 'ts', 'platform', NULL)),
    jurisdiction    VARCHAR(10) NOT NULL DEFAULT 'ZA',
    last_login      TIMESTAMPTZ,
    login_count     INTEGER NOT NULL DEFAULT 0,
    failed_logins   INTEGER NOT NULL DEFAULT 0,
    locked_until    TIMESTAMPTZ,
    tenant_id       UUID REFERENCES platform.tenants(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by      UUID REFERENCES iam.users(id),
    deleted_at      TIMESTAMPTZ,
    deleted_by      UUID REFERENCES iam.users(id),
    audit_ref_id    UUID REFERENCES audit.audit_refs(id)
);

CREATE UNIQUE INDEX users_email_active_idx ON iam.users(email) WHERE deleted_at IS NULL;
CREATE INDEX users_tenant_idx ON iam.users(tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX users_division_idx ON iam.users(division) WHERE deleted_at IS NULL;
```

---

### `iam.roles`

Defines the set of RBAC roles available in the system.

```sql
CREATE TABLE iam.roles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(100) NOT NULL UNIQUE,
    display_name    VARCHAR(255) NOT NULL,
    description     TEXT,
    division_scope  VARCHAR(50),  -- NULL = all divisions
    is_system_role  BOOLEAN NOT NULL DEFAULT false,  -- system roles cannot be deleted
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by      UUID REFERENCES iam.users(id)
);
```

### `iam.role_assignments`

Junction table linking users to roles.

```sql
CREATE TABLE iam.role_assignments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES iam.users(id),
    role_id         UUID NOT NULL REFERENCES iam.roles(id),
    assigned_by     UUID NOT NULL REFERENCES iam.users(id),
    assigned_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at      TIMESTAMPTZ,  -- NULL = no expiry
    revoked_at      TIMESTAMPTZ,
    revoked_by      UUID REFERENCES iam.users(id),
    revocation_reason TEXT,
    audit_ref_id    UUID REFERENCES audit.audit_refs(id),
    UNIQUE (user_id, role_id) WHERE revoked_at IS NULL
);
```

---

## Governance Schema

### `governance.model_registry`

Every AI model registered with the UDOC system.

```sql
CREATE TABLE governance.model_registry (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                        VARCHAR(255) NOT NULL,
    version                     VARCHAR(50),
    model_type                  VARCHAR(100) NOT NULL,
    operator_id                 UUID NOT NULL REFERENCES iam.users(id),
    tenant_id                   UUID NOT NULL REFERENCES platform.tenants(id),
    jurisdiction                VARCHAR(10) NOT NULL DEFAULT 'ZA',
    declared_purpose            TEXT NOT NULL,
    status                      VARCHAR(50) NOT NULL DEFAULT 'pending_review'
                                CHECK (status IN (
                                    'unregistered', 'pending_review', 'certified',
                                    'active', 'suspended', 'decommissioned'
                                )),
    certified_at                TIMESTAMPTZ,
    certified_by                UUID REFERENCES iam.users(id),
    deployed_at                 TIMESTAMPTZ,
    suspended_at                TIMESTAMPTZ,
    suspended_by                UUID REFERENCES iam.users(id),
    suspension_reason           TEXT,
    decommissioned_at           TIMESTAMPTZ,
    third_party_audit           BOOLEAN NOT NULL DEFAULT false,
    audit_report_url            TEXT,
    training_data_declaration   TEXT,
    affected_subjects           TEXT[] NOT NULL DEFAULT '{}',
    total_requests              BIGINT NOT NULL DEFAULT 0,
    approved_count              BIGINT NOT NULL DEFAULT 0,
    blocked_count               BIGINT NOT NULL DEFAULT 0,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by                  UUID REFERENCES iam.users(id),
    audit_ref_id                UUID REFERENCES audit.audit_refs(id)
);

CREATE INDEX model_registry_operator_idx ON governance.model_registry(operator_id);
CREATE INDEX model_registry_status_idx ON governance.model_registry(status);
CREATE INDEX model_registry_tenant_idx ON governance.model_registry(tenant_id);
```

---

### `governance.decisions`

The record of every governance decision. This is the most important table in the system.

```sql
CREATE TABLE governance.decisions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_id        UUID NOT NULL REFERENCES governance.model_registry(id),
    operator_id     UUID NOT NULL REFERENCES iam.users(id),
    tenant_id       UUID NOT NULL REFERENCES platform.tenants(id),
    request_id      UUID NOT NULL UNIQUE,  -- idempotency key
    input_hash      VARCHAR(64) NOT NULL,  -- SHA-256 of the input
    output_hash     VARCHAR(64),           -- SHA-256 of the output (if APPROVE)
    output_category VARCHAR(100) NOT NULL,
    jurisdiction    VARCHAR(10) NOT NULL,
    
    -- EVA scores (stored for audit and analytics)
    eva_ec_score    DECIMAL(5,2),
    eva_si_score    DECIMAL(5,2),
    eva_rc_score    DECIMAL(5,2),
    eva_fa_score    DECIMAL(5,2),
    eva_cc_score    DECIMAL(5,2),
    eva_sc_score    DECIMAL(5,2),
    eva_overall     DECIMAL(5,2),
    
    -- Outcome
    outcome         VARCHAR(20) NOT NULL
                    CHECK (outcome IN ('APPROVE', 'REVIEW', 'ESCALATE', 'BLOCK', 'ERROR')),
    reasoning       TEXT NOT NULL,         -- human-readable explanation
    
    -- Cryptographic seal
    decision_seal   TEXT NOT NULL,         -- HMAC-SHA256(decision payload, HSM key)
    seal_algorithm  VARCHAR(50) NOT NULL DEFAULT 'HMAC-SHA256',
    
    -- Governance references
    policy_version  INTEGER NOT NULL,      -- GV version active at time of decision
    oversight_case_id UUID REFERENCES governance.oversight_cases(id),
    
    -- Timing
    governance_ms   INTEGER,               -- governance path latency in milliseconds
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_ref_id    UUID NOT NULL REFERENCES audit.audit_refs(id)
);

CREATE INDEX decisions_model_idx ON governance.decisions(model_id);
CREATE INDEX decisions_outcome_idx ON governance.decisions(outcome);
CREATE INDEX decisions_created_at_idx ON governance.decisions(created_at);
CREATE INDEX decisions_tenant_idx ON governance.decisions(tenant_id);
```

---

### `governance.oversight_cases`

Every BLOCK decision creates an oversight case. This table tracks the human review process.

```sql
CREATE TABLE governance.oversight_cases (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    decision_id         UUID NOT NULL REFERENCES governance.decisions(id),
    subject_id          UUID REFERENCES iam.users(id),  -- who was affected
    assigned_to         UUID REFERENCES iam.users(id),  -- reviewer
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),
    status              VARCHAR(50) NOT NULL DEFAULT 'open'
                        CHECK (status IN ('open', 'assigned', 'in_review', 'resolved', 'escalated')),
    priority            VARCHAR(20) NOT NULL DEFAULT 'standard'
                        CHECK (priority IN ('low', 'standard', 'high', 'critical')),
    review_deadline     TIMESTAMPTZ NOT NULL,
    resolution          VARCHAR(50)
                        CHECK (resolution IN ('CONFIRMED', 'OVERRIDDEN', 'ESCALATED', NULL)),
    resolution_reason   TEXT,
    resolution_evidence TEXT,
    resolved_at         TIMESTAMPTZ,
    resolved_by         UUID REFERENCES iam.users(id),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_ref_id        UUID NOT NULL REFERENCES audit.audit_refs(id)
);

CREATE INDEX oversight_cases_status_idx ON governance.oversight_cases(status);
CREATE INDEX oversight_cases_assigned_to_idx ON governance.oversight_cases(assigned_to);
CREATE INDEX oversight_cases_deadline_idx ON governance.oversight_cases(review_deadline)
    WHERE status NOT IN ('resolved', 'escalated');
```
