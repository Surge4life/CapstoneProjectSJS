# Chapter 04 — UDOC Engine

## Purpose

UDOC — Universal Declaration of Operations Compliance — is the AI governance registration and enforcement layer. The UDOC Engine manages the lifecycle of every AI model that operates within the G.O.D.S ecosystem: registration, certification, live monitoring, suspension, resumption, and decommissioning.

---

## Location

- **Router:** `platform-core/app/routers/udoc_engine.py`
- **Router:** `platform-core/app/routers/registry.py`
- **Router:** `platform-core/app/routers/decisions.py`
- **Orchestrator:** `governance-engines/udoc/`
- **Attachment components:** `udoc-agent/`, `udoc-gateway/`, `udoc-edge/`, `udoc-sidecar/`

---

## The UDOC Model Lifecycle

```
UNREGISTERED
    ↓ register()
PENDING_REVIEW
    ↓ certify() [compliance officer action]
CERTIFIED
    ↓ deploy()
ACTIVE ←──────────────────────────┐
    ↓ suspend() [kill-switch]      │
SUSPENDED                          │
    ↓ resume()                     │
ACTIVE ────────────────────────────┘
    ↓ decommission()
DECOMMISSIONED [terminal — cannot be reactivated]
```

Every state transition is recorded in the audit chain with the acting user's identity and the reason for the transition.

---

## Model Registration

### POST /registry/models

Registers a new AI model for governance oversight.

**Required fields:**
```json
{
  "name": "Credit Assessment Model v2",
  "model_type": "classification",
  "operator_id": "uuid",
  "jurisdiction": "ZA",
  "declared_purpose": "string — plain language description of what the model does",
  "affected_subjects": ["individual", "employment"],
  "training_data_declaration": "string",
  "third_party_audit": false,
  "audit_report_url": null
}
```

**On registration:**
1. Model assigned a unique `model_id`
2. UDOC audit record created
3. Initial GBS compliance scan queued (conformance router)
4. Status set to `PENDING_REVIEW`
5. Notification sent to compliance officer(s)

---

## The Live Kill-Switch

The UDOC kill-switch is the most consequential capability in the governance arsenal. It allows an authorised operator to immediately suspend all outputs from a registered AI model.

### POST /registry/models/{model_id}/suspend

**Required RBAC:** `operator` (own models) or `gods_admin` (any model)

**Request:**
```json
{
  "reason": "string — required, plain language",
  "immediate_effect": true,
  "notify_subjects": true
}
```

**Effect:**
1. Model status set to `SUSPENDED` immediately
2. All `udoc-edge` nodes notified via Kafka (model suspension event)
3. Each edge node caches the suspension — model is blocked even offline
4. Audit record created with: acting user, timestamp, reason, affected request count
5. If `notify_subjects: true`, notification queue populated for all subjects with pending decisions from this model

**Latency target:** Model suspension propagated to all edge nodes within 30 seconds.

---

## The UDOC Orchestrator

The UDOC Orchestrator (`governance-engines/udoc/`) coordinates the sovereignty→FSM enforcement flow. It is responsible for:

1. **Sovereignty verification (SVS):** Does the model operator have the sovereignty declaration required for this action in this jurisdiction?
2. **Finite State Machine (FSM):** What is the current governance state of this model? Is the requested action permitted in this state?
3. **Enforcement:** Apply the EVA score + GBS rules to the specific action being requested

The orchestrator is called by the `governance_bridge` service for every governance request. It never serves external API traffic directly.

---

## UDOC SaaS Mode

UDOC can be deployed as a governance-as-a-service offering. External AI operators register their models via the UDOC SaaS API and receive governance coverage without deploying their own G.O.D.S instance.

In SaaS mode:
- The operator's models are registered in the G.O.D.S model registry
- Governance requests are proxied through the G.O.D.S deployment
- The operator receives governance dashboards via the `udoc-app` portal
- The operator pays per governance request (metered via the `saas` router)
- The operator's data is tenant-isolated (no cross-tenant data access)

SaaS mode is managed via the `saas` and `tenants` routers in `platform-core`.
