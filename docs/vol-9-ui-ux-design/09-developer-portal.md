# Chapter 09 — Developer / UDOC Portal

## Overview

The UDOC developer portal is the interface for AI operators — organisations and individuals who register AI models with the G.O.D.S governance system, submit governance requests, and monitor their models' governance record.

---

## Who Uses This Portal?

- **AI development teams** integrating their models with G.O.D.S governance
- **SaaS clients** using G.O.D.S as their AI governance layer
- **Enterprise operators** managing their AI governance programme
- **Compliance engineers** monitoring their AI systems' governance performance

---

## Design Philosophy for Developers

Developers expect professional, information-dense interfaces with:
- Good developer ergonomics (keyboard navigation, copy-to-clipboard everywhere)
- Code examples inline (API calls, webhook payloads)
- Technical detail accessible (not hidden behind "learn more" links)
- JSON/structured data views alongside human-readable summaries
- Clear status indicators with explicit state machine visibility

---

## Information Architecture

```
UDOC Operator Portal
├── Dashboard
│   ├── Live governance decision feed (real-time)
│   ├── Outcome distribution (last 24h)
│   ├── Average EVA scores trend
│   ├── Open oversight cases
│   └── System status (governance engine health)
│
├── Model Registry
│   ├── All registered models + status
│   ├── Register new model
│   ├── Model detail
│   │   ├── Model metadata
│   │   ├── FSM state timeline
│   │   ├── Conformance scan history
│   │   ├── Governance record (all decisions for this model)
│   │   ├── EVA score trends (per dimension)
│   │   └── Actions: request certification / request review / decommission
│   └── Certifications (model certification badges)
│
├── Governance Requests
│   ├── All governance decisions (searchable, filterable)
│   ├── Decision inspector
│   │   ├── Full EVA scores (hex radar chart)
│   │   ├── Policy rule that fired
│   │   ├── Reasoning text
│   │   ├── HMAC seal + verification
│   │   └── Raw decision JSON (copy button)
│   └── Resubmit (for REVIEW outcomes after providing more context)
│
├── Oversight Cases
│   ├── Open cases (for my models)
│   ├── Case detail
│   └── Provide additional evidence
│
├── Edge Nodes
│   ├── Registered edge nodes + online status
│   ├── Node detail (sync status, offline decisions pending)
│   └── Revoke a node
│
├── API
│   ├── API key management
│   ├── Webhook configuration
│   ├── API usage statistics
│   └── Interactive API explorer (Swagger UI embed)
│
└── Account
    ├── Operator profile
    ├── Governance agreement status
    ├── Team members and roles
    └── Billing (SaaS clients)
```

---

## The Decision Inspector

The Decision Inspector is the most frequently used view for operators:

```
┌─────────────────────────────────────────────────────────────┐
│ Decision #d7c3e... │ BLOCK │ 2025-01-15 10:30:41 UTC        │
├────────────────────────────────────────────────────────────┤
│ MODEL: GPT-Employment-Classifier v2.1 │ Request: req-abc123  │
├────────────────────────────────────────────────────────────┤
│ EVA SCORES                                                   │
│  EC  ████████████████████░░░░  88  Ethical Cooperation      │
│  SI  ████████████████░░░░░░░░  79  Societal Impact          │
│  RC  █████████████████████░░░  91  Regulatory Compliance    │
│  FA  ████████░░░░░░░░░░░░░░░░  38  Fairness  ⚠ BELOW FLOOR  │
│  CC  ████████████████░░░░░░░░  77  Confidence Calibration   │
│  SC  █████████████████████░░░  89  Sovereignty Compliance   │
│                                                              │
│  Overall: 74  │  Policy: Hard block — FA < 40               │
├────────────────────────────────────────────────────────────┤
│ REASONING                                                    │
│ Fairness score (38) falls below the constitutional minimum  │
│ (40). This action is blocked. The decision analysis         │
│ indicates risk of unfair treatment of affected individuals. │
├────────────────────────────────────────────────────────────┤
│ AUDIT SEAL: HMAC-SHA256:a3f8... [Verify] [Copy]            │
│ AUDIT REF: aud-8b21c...                                     │
│ OVERSIGHT CASE: case-93d7... [View]                        │
├────────────────────────────────────────────────────────────┤
│ [Copy as JSON]  [Download PDF]  [Challenge Decision]       │
└────────────────────────────────────────────────────────────┘
```

The FA dimension is highlighted in red with the ⚠ indicator when a hard-block threshold was the cause of the BLOCK outcome.

---

## Live Decision Feed

The dashboard shows a live feed of governance decisions, updated via WebSocket:

```
● 10:31:42  GPT-Employment v2.1        APPROVE  ↗  0.034s
● 10:31:38  GPT-Employment v2.1        REVIEW   ⏳  0.041s
● 10:31:35  GPT-Employment v2.1        APPROVE  ↗  0.031s
● 10:31:31  RiskScorer-v1              BLOCK    ✗  0.038s
```

Colour-coded by outcome, with latency shown. Click any row to open the Decision Inspector.
