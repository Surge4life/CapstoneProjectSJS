# Chapter 03 — governance-engines

## What Lives Here

`governance-engines/` contains the four specialist engines that implement the G.O.D.S governance logic. These are separate processes — not modules within `platform-core`. They communicate with `platform-core` via HTTP APIs. This separation means:

- Engines can be updated independently of the backend
- Engines can be written in the most appropriate language for their task
- Engine failures are isolated (a crashed EVA engine does not crash `platform-core`)

---

## Directory Structure

```
governance-engines/
├── eva/          EVA 6-dimensional risk scoring (Python)
├── gis/          GBS-SETHS Intelligence & Franchise Layer (Node.js)
├── gods/         G.O.D.S Platform orchestrator (Node.js)
└── udoc/         UDOC Orchestrator — SVS + FSM + Enforce (Python)
```

---

## `eva/` — EVA Engine (Python)

**Responsibility:** 6-dimensional sovereign risk scoring for every governance request.

**Language:** Python 3.12  
**Framework:** FastAPI  
**Port:** 3002  

**Structure:**
```
eva/
├── main.py          FastAPI app factory
├── scorers/
│   ├── ec.py        Ethical Cooperation scorer
│   ├── si.py        Societal Impact scorer
│   ├── rc.py        Regulatory Compliance scorer
│   ├── fa.py        Fairness scorer
│   ├── cc.py        Confidence Calibration scorer
│   └── sc.py        Sovereignty Compliance scorer
├── aggregator.py    Score weighting and aggregation
├── models.py        Pydantic request/response models
└── requirements.txt
```

**Endpoint:**
```
POST /score
{
    "model_id": "uuid",
    "output_category": "classification",
    "declared_confidence": 0.87,
    "affecting_subjects": [...],
    "jurisdiction": "ZA",
    "operator_history": {...}
}
→ { "ec": 88, "si": 79, "rc": 91, "fa": 85, "cc": 76, "sc": 88, "overall": 82 }
```

**Performance target:** < 10ms per score  
**Scaling:** Stateless — run as many instances as needed

---

## `gis/` — GIS Engine (Node.js)

**Responsibility:** Franchise governance, certification management, participant registry, and pledge tracking.

**Language:** Node.js 20 + TypeScript  
**Framework:** Express  
**Port:** 3004  

**Structure:**
```
gis/
├── src/
│   ├── index.ts             Express app
│   ├── routes/
│   │   ├── certifications.ts
│   │   ├── franchises.ts
│   │   ├── participants.ts
│   │   └── pledges.ts
│   ├── services/
│   │   ├── certificationService.ts
│   │   └── participantService.ts
│   └── models/
│       └── types.ts
├── package.json
└── tsconfig.json
```

---

## `gods/` — G.O.D.S Intelligence Engine (Node.js)

**Responsibility:** Orchestrates the G.O.D.S Intelligence query pipeline — pre-check, corpus retrieval coordination, response synthesis, post-check.

**Language:** Node.js 20 + TypeScript  
**Framework:** Express  
**Port:** 3001  

The G.O.D.S engine calls into `platform-core` for corpus retrieval (OpenSearch is accessed via platform-core, not directly from this engine). It is the orchestration layer — it does not store data or manage persistence.

---

## `udoc/` — UDOC Orchestrator (Python)

**Responsibility:** Sovereignty verification (SVS), model state machine (FSM), and final enforcement decisions.

**Language:** Python 3.12  
**Framework:** FastAPI  
**Port:** 3003  

**Structure:**
```
udoc/
├── main.py
├── sovereignty.py   SVS — jurisdiction and consent verification
├── fsm.py           Finite State Machine — model lifecycle states
├── enforcer.py      Combines SVS + FSM to produce final enforcement
├── models.py
└── requirements.txt
```

**Endpoint:**
```
POST /enforce
{
    "model_id": "uuid",
    "model_status": "active",
    "jurisdiction": "ZA",
    "operator_id": "uuid",
    "eva_scores": { "overall": 82, ... },
    "policy_outcome": "APPROVE"
}
→ { "outcome": "APPROVE", "reasoning": "...", "sovereignty_verified": true }
```

---

## Engine Communication Pattern

```
platform-core
  → governance_bridge.py
    → POST eva/score        (synchronous, await result)
    → POST udoc/enforce     (synchronous, await result)
    → POST gods/orchestrate (synchronous for intelligence queries)
    → POST gis/*            (synchronous for certification ops)
```

All engine calls have:
- **Timeout:** 5 seconds maximum
- **Retry:** 2 retries with exponential backoff
- **Circuit breaker:** Opens after 5 consecutive failures in 30 seconds
- **Fallback on governance engines:** BLOCK — fail closed
- **Fallback on GIS/intelligence:** Error response, not BLOCK
