# Chapter 09 — Edge Components

## The Four Edge Components

The edge layer is where the G.O.D.S governance system meets AI models in the wild. These four components are the attachment points — the technical implementations of the governance attachment that every governed AI model must have.

---

## udoc-agent

**Purpose:** Host-side governance attachment for AI models running on the same host.

**Location:** `udoc-agent/`

**What it does:**
- Runs as a local daemon alongside the governed AI model
- Intercepts AI requests via a local proxy (HTTP or Unix socket)
- Forwards governance payloads to `platform-core /decisions`
- Applies the decision: forward to model (APPROVE/REVIEW) or reject (ESCALATE/BLOCK)
- Buffers governance decisions in local SQLite for audit replay when offline
- Implements the fail-closed: if `platform-core` is unreachable, requests are held, not forwarded

**Configuration:**
```yaml
agent:
  model_id: "registered-model-uuid"
  governance_url: "https://platform-core.internal"
  listen_port: 8080
  upstream_port: 11434  # e.g., Ollama
  fail_closed: true
  buffer_size: 1000
  buffer_path: "/var/lib/udoc-agent/buffer.db"
```

**Audit:** Every governance request and decision is written to the local buffer and synced to the central audit chain when connectivity is available.

---

## udoc-gateway

**Purpose:** Protocol bridge for governed AI models that serve external traffic, with mTLS and lineage tagging.

**Location:** `udoc-gateway/`

**What it does:**
- Operates as a reverse proxy for governed AI APIs
- Adds mTLS to external connections that don't natively support it
- Tags every request with a `X-UDOC-Lineage` header containing a governance reference
- Handles signed relay for air-gapped deployments (sign the governance payload offline, relay when online)
- Rate limiting and DDoS protection at the governance boundary

**Deployment:** The gateway sits between the internet and the governed AI model. External clients connect to the gateway; the gateway connects to the model via mTLS.

```
External client ──HTTPS──► udoc-gateway ──mTLS──► AI model
                              │
                           governance payload
                              │
                           platform-core
```

---

## udoc-edge

**Purpose:** Autonomous local governance node that can operate without connection to `platform-core`.

**Location:** `udoc-edge/`

**What it does:**
- Mirrors the model registry and current PolicyPack from `platform-core`
- Runs a local governance engine (simplified EVA + GBS) for offline decisions
- Syncs decisions and audit records to `platform-core` when connectivity is restored
- Handles registry updates (including kill-switch suspensions) when online

**The offline governance guarantee:**
When `platform-core` is unreachable, the edge node does not stop governing. It applies the last-known governance rules from its local mirror. Offline decisions are marked `OFFLINE_GOVERNED` in the audit chain and are reviewed against the current rules when connectivity is restored.

If a model was suspended while the edge was offline, the suspension is applied as soon as the edge reconnects and the registry sync occurs. All requests processed while the model was suspended (from the perspective of `platform-core`) are flagged for review.

**Hardware target:** The edge component is designed to run on the UDOC hardware node specified in the hardware architecture (FPGA + HSM + NIC). In software emulation mode it runs in a standard Linux container.

---

## udoc-sidecar

**Purpose:** Governance event buffer for AI models in environments with intermittent connectivity.

**Location:** `udoc-sidecar/`

**What it does:**
- Runs as a sidecar container alongside the governed AI model (Kubernetes sidecar pattern)
- Buffers governance events locally when `platform-core` is unreachable
- Provides a local governance decision cache (short TTL — for repeated identical requests in offline windows)
- Replays buffered events to `platform-core` when connectivity is restored
- Preserves ordering of events for correct audit chain construction

**Difference from udoc-edge:**
The sidecar is simpler than the edge. It does not run a local governance engine — it only buffers. If the sidecar loses connectivity and the local cache is empty, it fails closed (no governance decisions = no forwarding). The edge runs a full offline governance engine.

Use the sidecar for: cloud environments with reliable connectivity but occasional outages.
Use the edge for: air-gapped or frequently-offline deployments.

---

## Component Selection Guide

| Deployment Scenario | Recommended Component |
|--------------------|----------------------|
| Cloud AI (same host) | `udoc-agent` |
| Cloud AI (external API) | `udoc-gateway` |
| Kubernetes workload | `udoc-sidecar` |
| On-premise, always connected | `udoc-agent` or `udoc-gateway` |
| On-premise, intermittent connectivity | `udoc-edge` |
| Air-gapped | `udoc-edge` |
| UDOC hardware node | `udoc-edge` (hardware mode) |

Multiple components can be used together. A common pattern: `udoc-gateway` (external boundary) + `udoc-agent` (internal model attachment) + `udoc-edge` (offline fallback).
