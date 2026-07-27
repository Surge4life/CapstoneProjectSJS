# Chapter 06 — Hybrid Cloud Architecture

## What Is Hybrid Cloud for G.O.D.S?

A hybrid cloud deployment runs some G.O.D.S components in public cloud and others on-premises or in a private cloud. This is appropriate when:

- Certain data must remain on-premises (regulatory residency requirement) while other data can be cloud-hosted
- The organisation already has significant on-premises investment (existing databases, network infrastructure) but wants cloud elasticity for compute
- Business continuity requires both cloud and on-premises operation (either can serve while the other is degraded)

---

## Hybrid Split Patterns

### Pattern A: Data On-Premises, Compute in Cloud

```
On-Premises:
  - PostgreSQL (learner PII, governance records)
  - Cassandra (audit chain)
  - Object storage (documents)

Cloud (Render / Kubernetes hosted):
  - platform-core
  - governance-engines
  - Redis (cache, sessions)
  - OpenSearch (corpus — no PII stored here)
  - Monitoring stack
```

**Connection:** platform-core connects to on-premises databases via a dedicated VPN tunnel (WireGuard or site-to-site IPSec). Database credentials are managed by Vault (on-premises).

**Benefit:** Compute scales with demand; sensitive data never leaves the organisation's network.

**Latency consideration:** Cross-network database calls add latency. Typical VPN latency: 5–15ms. Add to governance path budget — total target remains < 50ms, so on-premises DB latency is acceptable.

---

### Pattern B: Geo-Distributed Sovereignty

For organisations with operations in multiple jurisdictions:

```
SA Node (Johannesburg):
  - All ZA-jurisdiction governance decisions
  - ZA learner and employer data
  - ZA audit chain partition

EU Node (Frankfurt):
  - EU-jurisdiction governance decisions
  - EU subject data
  - EU audit chain partition

Central Orchestrator (cloud):
  - Cross-jurisdiction routing
  - Aggregate analytics (no PII)
  - Policy synchronisation (same PolicyPack deployed everywhere)
  - Central model registry (UDOC)
```

**Sovereignty enforcement:** A governance request tagged with jurisdiction=ZA is always routed to the SA node, regardless of where the request originates. The UDOC Sovereignty Verification System (SVS) enforces this.

---

### Pattern C: Edge + Cloud

For deployments with field operations (e.g., SETHS career advisors visiting communities):

```
Cloud:
  - Primary platform-core
  - Full database stack
  - Intelligence corpus

Edge (at each field office):
  - udoc-edge node
  - Local PolicyPack copy
  - Offline decision queue
  - Sync to cloud when connectivity available
```

---

## VPN Configuration for Hybrid

```yaml
# WireGuard configuration (infra/vpn/wg0.conf)
[Interface]
PrivateKey = <generated — stored in Vault, never in repository>
Address = 10.100.0.1/24
ListenPort = 51820

[Peer]
# On-premises data centre
PublicKey = <on-premises WG public key>
AllowedIPs = 10.200.0.0/24     # On-premises database network
Endpoint = on-premises-gw.example.com:51820
PersistentKeepalive = 25
```

The WireGuard configuration is in `infra/vpn/`. Private keys are never committed to the repository — they are managed in Vault and injected as Kubernetes secrets at deployment time.

---

## Hybrid Monitoring

In hybrid deployments, monitoring is centralised:

```
On-premises Prometheus (scrapes on-premises services)
        ↓
Prometheus federation (sends aggregate metrics to cloud Prometheus)
        ↓
Central Grafana (shows hybrid infrastructure on unified dashboards)
        ↓
Alertmanager (routes alerts regardless of which node raised them)
```

Alert channels (Slack, PagerDuty) receive alerts from both on-premises and cloud components. Alerts include a `node` label so the on-call engineer knows which environment to investigate.
