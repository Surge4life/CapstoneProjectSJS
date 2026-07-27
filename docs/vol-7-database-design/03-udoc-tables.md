# Chapter 03 — UDOC Tables

## Schema: `udoc`

The UDOC schema stores all AI model registry data, operator records, edge node management, and governance agreements.

---

## Table: `udoc.ai_models`

The central registry of all AI models subject to G.O.D.S governance.

```sql
CREATE TABLE udoc.ai_models (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    operator_id         UUID NOT NULL REFERENCES iam.users(id),
    tenant_id           UUID NOT NULL REFERENCES platform.tenants(id),

    -- Model identity
    model_name          VARCHAR(200) NOT NULL,
    model_version       VARCHAR(50) NOT NULL,
    model_type          VARCHAR(50) NOT NULL,       -- classification | generation | regression | recommendation | other
    output_category     VARCHAR(50) NOT NULL,       -- matches EVA output_category expected values
    description         TEXT,
    model_hash          VARCHAR(64),               -- SHA-256 of model binary (if provided)

    -- Jurisdictional declaration
    declared_jurisdiction VARCHAR(10) NOT NULL DEFAULT 'ZA',
    cross_border_authorised BOOLEAN NOT NULL DEFAULT false,

    -- Registration state (FSM)
    status              VARCHAR(30) NOT NULL DEFAULT 'pending_review',
    -- pending_review | active | probationary | suspended | revoked | expired | decommissioned
    certified           BOOLEAN NOT NULL DEFAULT false,
    certification_id    UUID,                      -- GIS certification record
    certification_expires_at TIMESTAMPTZ,

    -- Probation fields
    probation_plan      TEXT,
    probation_expires_at TIMESTAMPTZ,

    -- Suspension fields
    suspension_reason   TEXT,
    suspended_at        TIMESTAMPTZ,
    suspended_by        UUID REFERENCES iam.users(id),

    -- Governance metrics (denormalised for performance)
    total_decisions     INTEGER NOT NULL DEFAULT 0,
    total_blocks        INTEGER NOT NULL DEFAULT 0,
    total_reviews       INTEGER NOT NULL DEFAULT 0,
    last_decision_at    TIMESTAMPTZ,
    governance_score_30d DECIMAL(5,2),             -- rolling 30-day average EVA overall

    -- Audit
    udoc_audit_ref_id   UUID NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by          UUID NOT NULL REFERENCES iam.users(id),
    updated_by          UUID NOT NULL REFERENCES iam.users(id),

    CONSTRAINT udoc_ai_models_status_check CHECK (
        status IN ('pending_review','active','probationary','suspended','revoked','expired','decommissioned')
    ),
    CONSTRAINT udoc_ai_models_type_check CHECK (
        model_type IN ('classification','generation','regression','recommendation','other')
    )
);

CREATE INDEX udoc_ai_models_operator_idx ON udoc.ai_models(operator_id);
CREATE INDEX udoc_ai_models_tenant_idx ON udoc.ai_models(tenant_id);
CREATE INDEX udoc_ai_models_status_idx ON udoc.ai_models(status);
CREATE INDEX udoc_ai_models_output_category_idx ON udoc.ai_models(output_category);
```

---

## Table: `udoc.model_fsm_events`

Immutable log of every FSM state transition.

```sql
CREATE TABLE udoc.model_fsm_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_id        UUID NOT NULL REFERENCES udoc.ai_models(id),
    from_state      VARCHAR(30) NOT NULL,
    action          VARCHAR(50) NOT NULL,
    to_state        VARCHAR(30) NOT NULL,
    actor_id        UUID NOT NULL REFERENCES iam.users(id),
    reason          TEXT NOT NULL,
    audit_ref_id    UUID NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX udoc_fsm_events_model_idx ON udoc.model_fsm_events(model_id, created_at DESC);
```

---

## Table: `udoc.conformance_scans`

Results of UDOC conformance scans run on registered models.

```sql
CREATE TABLE udoc.conformance_scans (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_id        UUID NOT NULL REFERENCES udoc.ai_models(id),
    scan_type       VARCHAR(30) NOT NULL DEFAULT 'initial',
    -- initial | periodic | triggered | pre_certification

    -- Results
    overall_result  VARCHAR(10) NOT NULL,          -- PASS | FAIL | WARNING
    bias_check      VARCHAR(10) NOT NULL,
    transparency_check VARCHAR(10) NOT NULL,
    jurisdiction_check VARCHAR(10) NOT NULL,
    documentation_check VARCHAR(10) NOT NULL,

    findings        JSONB NOT NULL DEFAULT '[]',   -- Array of finding objects
    recommendations TEXT,
    scanned_by      UUID NOT NULL REFERENCES iam.users(id),
    audit_ref_id    UUID NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## Table: `udoc.edge_nodes`

Registry of UDOC edge nodes (udoc-agent, udoc-edge, udoc-gateway instances).

```sql
CREATE TABLE udoc.edge_nodes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES platform.tenants(id),
    node_type       VARCHAR(20) NOT NULL,  -- agent | edge | gateway | station
    node_name       VARCHAR(100) NOT NULL,
    node_version    VARCHAR(20),
    
    -- Connectivity
    status          VARCHAR(20) NOT NULL DEFAULT 'offline',
    -- online | offline | degraded | revoked
    last_seen_at    TIMESTAMPTZ,
    ip_address      INET,
    
    -- Security
    certificate_fingerprint VARCHAR(64),
    certificate_expires_at  TIMESTAMPTZ,
    
    -- Sync state
    policy_version_synced INTEGER,
    last_sync_at    TIMESTAMPTZ,
    offline_decisions_pending INTEGER NOT NULL DEFAULT 0,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    registered_by   UUID NOT NULL REFERENCES iam.users(id),
    revoked_at      TIMESTAMPTZ,
    revoked_by      UUID REFERENCES iam.users(id)
);

CREATE INDEX udoc_edge_nodes_tenant_idx ON udoc.edge_nodes(tenant_id);
CREATE INDEX udoc_edge_nodes_status_idx ON udoc.edge_nodes(status);
```

---

## Table: `udoc.operator_agreements`

Signed governance agreements between operators and the platform.

```sql
CREATE TABLE udoc.operator_agreements (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    operator_id     UUID NOT NULL REFERENCES iam.users(id),
    agreement_type  VARCHAR(50) NOT NULL,  -- governance_terms | data_processing | franchise
    agreement_version VARCHAR(20) NOT NULL,
    signed_at       TIMESTAMPTZ NOT NULL,
    signed_by_name  VARCHAR(200) NOT NULL,
    signed_by_title VARCHAR(200),
    document_hash   VARCHAR(64) NOT NULL,  -- SHA-256 of agreement document
    audit_ref_id    UUID NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```
