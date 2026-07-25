# Chapter 01 — Architecture Overview & Service Map

## The G.O.D.S System at a Glance

The G.O.D.S ecosystem is a distributed governance platform. Its architecture is designed around one invariant: **the governance path is always the critical path**. Every other performance and design decision is made in service of this invariant.

---

## Service Map

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
│  udoc-app  seths-app  madiba-app  ts-app  platform-web  portals-web  │
│  (React PWAs + Capacitor mobile + desktop wrappers)                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ HTTPS / REST API
┌──────────────────────────▼──────────────────────────────────────────┐
│                      platform-core (FastAPI)                         │
│                                                                      │
│  auth    admin   rbac   registry   decisions   compliance            │
│  seths   madiba  ts     udoc_engine intelligence audit               │
│  bias    conformance sovereignty   policy      analytics             │
│  documents portals_* client_knowledge gis       enclave              │
│                                                                      │
│  Services: governance_bridge  gbs_engine  gods_intelligence          │
│            audit_writer       event_bus   key_service                │
│            document_store     rbac_svc    policy_engine              │
│            gis_engine         analytics_engine                       │
└──────────┬──────────────────────────┬───────────────────────────────┘
           │                          │
    ┌──────▼──────┐          ┌────────▼────────┐
    │ governance- │          │   Data Layer    │
    │   engines   │          │                 │
    │             │          │ PostgreSQL       │
    │  EVA        │          │ Kafka           │
    │  GIS        │          │ Cassandra/WORM  │
    │  UDOC orch  │          │ OpenSearch      │
    │  G.O.D.S    │          │ Redis           │
    └─────────────┘          │ Object Storage  │
                             └─────────────────┘
┌─────────────────────────────────────────────────────────────────────┐
│                         EDGE LAYER                                   │
│  udoc-agent   udoc-gateway   udoc-edge   udoc-sidecar               │
│  (AI attachment, protocol bridge, autonomous node, event buffer)     │
└─────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────┐
│                       HARDWARE LAYER                                 │
│  hw-bringup: boot → selftest → init → platform-core.service         │
│  FPGA (enforcement) + HSM/TPM (keys) + NIC (sovereignty hook)       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Request Lifecycle: Standard Governance Path

This sequence shows what happens when a governed AI model receives a request.

```
1. AI client sends request to governed model
2. udoc-agent intercepts (pre-request hook)
3. agent sends governance request to platform-core /decisions
4. /decisions calls governance_bridge service
5. governance_bridge calls EVA engine → 6-D score
6. governance_bridge calls GBS runtime → constitutional check
7. governance_bridge calls UDOC orchestrator → SVS→FSM→enforce
8. Decision produced: {APPROVE | REVIEW | ESCALATE | BLOCK}
9. Decision sealed: HMAC + Dilithium-reference
10. Decision written to PostgreSQL (DecisionRecord)
11. Decision published to Kafka (event_bus)
12. Kafka consumer (audit_writer) writes to Cassandra/WORM
13. audit_writer computes running Merkle root
14. Decision response returned to udoc-agent
15. If APPROVE/REVIEW: agent forwards request to model
16. If ESCALATE/BLOCK: agent returns governance error to AI client
17. If BLOCK: OversightCase created automatically
```

Target latency for steps 3–14: **sub-50 milliseconds**.

---

## Technology Stack Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend framework | FastAPI | 0.110+ |
| Python runtime | Python | 3.12+ |
| ORM | SQLAlchemy | 2.0+ |
| Data validation | Pydantic | v2 |
| Task scheduling | APScheduler | 3.x |
| Primary database | PostgreSQL | 15+ |
| Event streaming | Apache Kafka | 3.x |
| Audit storage | Apache Cassandra | 4.x |
| Search | OpenSearch | 2.x |
| Cache / session | Redis | 7.x |
| Frontend framework | React | 18+ |
| Frontend build | Vite | 5+ |
| PWA | vite-plugin-pwa | Latest |
| Mobile | Capacitor | 5+ |
| Infrastructure | Docker + Kubernetes | Latest stable |
| Cloud deployment | Render (current) | N/A |
| Governance engines | Node.js (gods/gis) + Python (eva/udoc) | 20+ / 3.12+ |
