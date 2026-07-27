# Chapter 08 — Event & Notification Tables

## Schema: `events`

The event tables capture the platform event bus messages that flow through Kafka. PostgreSQL stores the event log for queryable history; Kafka is the real-time transport.

---

## Table: `events.platform_events`

```sql
CREATE TABLE events.platform_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id        UUID NOT NULL UNIQUE,          -- Kafka message key
    event_type      VARCHAR(100) NOT NULL,
    -- e.g. governance.decision_created, seths.application_status_changed
    source_service  VARCHAR(50) NOT NULL,          -- Which service published this event
    
    tenant_id       UUID REFERENCES platform.tenants(id),
    user_id         UUID REFERENCES iam.users(id),  -- Actor (if applicable)
    resource_type   VARCHAR(50),
    resource_id     UUID,

    payload         JSONB NOT NULL DEFAULT '{}',   -- Full event payload
    
    -- Delivery tracking
    kafka_partition INTEGER,
    kafka_offset    BIGINT,
    published_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    consumed_at     TIMESTAMPTZ,                   -- When notification consumer processed it

    -- Retention
    retain_until    TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '90 days')
);

CREATE INDEX platform_events_type_idx ON events.platform_events(event_type, published_at DESC);
CREATE INDEX platform_events_resource_idx ON events.platform_events(resource_type, resource_id);
CREATE INDEX platform_events_tenant_idx ON events.platform_events(tenant_id, published_at DESC);

-- TTL enforcement (run nightly via cleanup job)
CREATE INDEX platform_events_retain_until_idx ON events.platform_events(retain_until);
```

---

## Table: `events.notifications`

In-app notifications for users.

```sql
CREATE TABLE events.notifications (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipient_id            UUID NOT NULL REFERENCES iam.users(id),
    tenant_id               UUID NOT NULL REFERENCES platform.tenants(id),

    notification_type       VARCHAR(100) NOT NULL,
    title                   VARCHAR(200) NOT NULL,
    body                    TEXT NOT NULL,
    action_url              VARCHAR(500),           -- Deep link

    priority                VARCHAR(20) NOT NULL DEFAULT 'standard',
    -- low | standard | high | critical

    -- Related resource
    related_resource_type   VARCHAR(50),
    related_resource_id     UUID,
    governance_ref_id       UUID,                  -- Link to governance event

    -- Delivery channels
    delivered_in_app        BOOLEAN NOT NULL DEFAULT false,
    delivered_email         BOOLEAN NOT NULL DEFAULT false,
    delivered_push          BOOLEAN NOT NULL DEFAULT false,

    -- Status
    read_at                 TIMESTAMPTZ,
    dismissed_at            TIMESTAMPTZ,

    -- Source event
    source_event_id         UUID REFERENCES events.platform_events(event_id),
    
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT notifications_priority_check CHECK (
        priority IN ('low', 'standard', 'high', 'critical')
    )
);

CREATE INDEX notifications_recipient_unread_idx
    ON events.notifications(recipient_id, created_at DESC)
    WHERE read_at IS NULL AND dismissed_at IS NULL;
CREATE INDEX notifications_tenant_idx ON events.notifications(tenant_id, created_at DESC);
```

---

## Table: `events.webhook_deliveries`

For operator integrations — webhook delivery tracking.

```sql
CREATE TABLE events.webhook_deliveries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    operator_id     UUID NOT NULL REFERENCES iam.users(id),
    webhook_url     VARCHAR(500) NOT NULL,
    event_type      VARCHAR(100) NOT NULL,
    payload         JSONB NOT NULL,
    
    -- Delivery result
    attempt_count   INTEGER NOT NULL DEFAULT 0,
    last_attempt_at TIMESTAMPTZ,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending | delivered | failed | abandoned
    http_status     INTEGER,
    response_body   TEXT,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    delivered_at    TIMESTAMPTZ,
    next_retry_at   TIMESTAMPTZ
);

CREATE INDEX webhook_deliveries_pending_idx
    ON events.webhook_deliveries(next_retry_at)
    WHERE status = 'pending';
```

---

## Schema: `platform` — Tenant Configuration

```sql
CREATE TABLE platform.tenants (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_name         VARCHAR(200) NOT NULL,
    tenant_code         VARCHAR(50) UNIQUE NOT NULL,
    plan_tier           VARCHAR(20) NOT NULL DEFAULT 'starter',
    -- starter | professional | enterprise | franchise
    
    -- Corpus limits
    corpus_doc_limit    INTEGER NOT NULL DEFAULT 1000,
    corpus_storage_gb   INTEGER NOT NULL DEFAULT 10,
    intelligence_queries_daily INTEGER NOT NULL DEFAULT 10000,
    
    -- Configuration
    default_jurisdiction VARCHAR(10) NOT NULL DEFAULT 'ZA',
    active_policy_pack_id UUID,                   -- Active policy pack for this tenant
    
    -- Platform corpus licensing
    licensed_knowledge_packs TEXT[] DEFAULT '{}',
    
    -- Status
    status              VARCHAR(20) NOT NULL DEFAULT 'active',
    -- active | suspended | cancelled
    
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```
