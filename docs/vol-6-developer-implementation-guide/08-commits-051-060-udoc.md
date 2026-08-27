# Chapter 08 — Commits 051–060: UDOC Division & Edge

## Overview

This batch completes the UDOC division — the operator-facing AI governance tooling, model registry, edge node management, and SaaS operator features.

---

## Commit 051: `[DB] MIGRATE: Add UDOC model registry tables`

**What:**
- `udoc.ai_models` — registered AI models
- `udoc.model_versions` — version history for each model
- `udoc.conformance_scans` — conformance scan results
- `udoc.model_fsm_events` — FSM state transition history
- `udoc.operator_agreements` — signed governance agreements

---

## Commit 052: `[CORE] ADD: Model registry service`

**What:**
- `register_model()` — new model registration → triggers UDOC FSM → `pending_review`
- `approve_registration()` — compliance officer approval → FSM to `active`
- `get_model()` — model record with full FSM history
- `list_models()` — operator-scoped or admin-scoped listing
- `run_conformance_scan()` — triggers conformance evaluation engine

---

## Commit 053: `[CORE] ADD: UDOC governance operations — certify, suspend, revoke`

**What:**
- `certify_model()` — certification issuance + GIS certification record
- `suspend_model()` — FSM transition to `suspended`, audit record, operator notification
- `lift_suspension()` — FSM to `active`, audit record
- `revoke_model()` — permanent FSM to `revoked`, operator notification, GIS certification invalidated
- `place_on_probation()` / `lift_probation()` — probationary state management

---

## Commit 054: `[UI] ADD: UDOC web application — model registry and governance`

**What:** `udoc-app/` complete implementation:
- Connect screen + login
- Model registry: register, view status, FSM history
- Decision inspector: drill into governance decisions with EVA breakdowns
- Oversight cases: manage open cases
- Edge node status: view connected edge nodes
- Analytics: governance metrics dashboard

---

## Commit 055: `[CORE] ADD: Edge node management service`

**What:**
- `register_edge_node()` — new edge node registration
- `heartbeat()` — edge node check-in (updates `last_seen_at`, syncs config)
- `sync_governance_config()` — push PolicyPack updates to edge nodes
- `get_edge_status()` — status of all edge nodes
- `revoke_edge_node()` — invalidate an edge node's credentials

---

## Commit 056: `[CORE] ADD: udoc-agent — host-side governance attachment`

**What:** `udoc-agent/` implementation:
- Attaches to the host AI system's event stream
- Intercepts model outputs and submits to `platform-core` governance path
- Buffer + retry for transient connectivity issues
- Local deny list (cached blocked model IDs for instant local enforcement)

---

## Commit 057: `[CORE] ADD: udoc-gateway — mTLS relay`

**What:** `udoc-gateway/` implementation:
- Protocol bridge between edge nodes and platform-core
- mTLS termination (edge nodes present client certificates)
- Rate limiting per edge node
- Governance request queuing (handles burst traffic)

---

## Commit 058: `[CORE] ADD: udoc-edge — autonomous offline governance node`

**What:** `udoc-edge/` implementation:
- Maintains local copy of PolicyPack and suspended model list
- Processes governance requests locally when offline
- Sync mechanism: when connectivity restores, uploads buffered decisions to platform-core
- Conflict resolution: offline decisions are recorded as `offline_decision: true`; platform reviews them on sync

---

## Commit 059: `[CORE] ADD: UDOC SaaS operator portal`

**What:** `udoc-operator/` and `udoc-public/` implementations:
- SaaS operator self-service: register, manage models, view billing
- Public verification endpoint: `GET /verify/{certification_id}`
- API key management for programmatic governance submission

---

## Commit 060: `[TEST] ADD: UDOC end-to-end integration tests`

**What:**
- Model registration → conformance → approval flow
- Full FSM traversal tests (all valid transitions)
- Edge node sync and offline operation
- Governance path with registered vs unregistered models
- Operator RBAC enforcement

`tests/test_udoc_integration.py` — 35 test cases
