# Client Governance Intelligence · Deterministic Path (not LLM)

**Updated:** 2026-08-01  
**Status:** Capstone intent + live substrate slice  
**Audience:** Assessors · Client package · GBS / GIS readers  
**Related:** `CLIENT_INTELLIGENCE.md` · `EDR-002-knowledge-substrate.md` · Canon Knowledge Substrate language

---

## 1. One sentence

**Client business corpus feeds deterministic UDOC governance engines.**  
Client agentic / generic / recursive **AI models are separate products**. They may **request usage** of UDOC decisions; they **never amend or control** the UDOC / GIS constitutional layer.

---

## 2. Three intelligences (do not merge)

| Layer | What it is | Who owns it | Amends UDOC / GIS? |
|-------|------------|-------------|--------------------|
| **A · Client operational models** | Client’s agentic, generic, recursive, or deployed foundation models used for business work | Client | **No** — may only call UDOC as a **usage consumer** |
| **B · UDOC Governance Intelligence** | Deterministic engines: policy-to-code, EVA 6-D, fail-closed decisions, certificates, HITL, portals | **UDOC under GODS constitutional control** | N/A — *is* the control surface |
| **C · GODS Intelligence (GIS substrate)** | Holdings-wide knowledge + GIS constitutional backbone for SETHS / MADIBA / TS / franchise | **GODS Holdings** | N/A — UDOC-controlled access; not a client LLM product |

**Patent posture (UDOC):**  
Generic or higher AI models are **declined as controllers** of the system that regulates AI. **Human primacy** and deterministic governance stay above any client model. UDOC does not outsource its own authority to the models it evaluates.

**GODS Intelligence is not** “UDOC deterministic engines renamed.”  
UDOC engines **execute** governance. GODS Intelligence is the **broader substrate** (corpus, pillars, GIS decision types, franchise/compliance) aimed at AI-TRANSITION and Holdings ecosystem continuity — documented as vision; Capstone ships the UDOC control loop + client private corpus slice under Neon limits.

---

## 3. Reference flow (corpus → engines → surfaces)

```
                    CLIENT BUSINESS CORPUS
              (upload / text ingest · tenant_pk)
                            │
                            ▼
              Knowledge Substrate (tenant-private)
              classify · version · authority · cite
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
     DETERMINISTIC ENGINES          CLIENT AI MODELS (A)
     (UDOC / GBS-aligned)           agentic · generic · recursive
              │                           │
              │                     may request:
              │                     evaluate · status · cert verify
              │                           │
              ▼                           ▼
     ┌────────────────────────────────────────────┐
     │     UDOC PRIMACY CONTROLLER                │
     │  grants USAGE only · never amendment       │
     │  of engine code, rules, GIS, or platform   │
     └────────────────────────────────────────────┘
                            │
         policy-to-code · EVA · seal · HITL · portals
                            │
                            ▼
              Client UDOC surfaces (Govern / Registry / …)
                            │
                            ▼
              GODS constitutional layer (GIS / divisions)
              — UDOC-controlled access · not client-writable
```

As the **client expands the corpus**, the **reference material** available to grounded ask and to future Knowledge Compiler objects expands. That is **substrate growth**, not automatic “training of a foundation model” on free Neon. Capstone honesty: retrieval-grounded + rule engines today; full Compiler + continuous learning stack = documented intent.

---

## 4. Engines attached to corpus (deterministic)

These are the **governance engines** that may **reference** client or platform corpus / policy — not LLMs:

| Engine / module | Role relative to corpus |
|-----------------|-------------------------|
| **Policy-to-code** | Legislation / policy packs → compiled rules → ACTIVE enforcement on decisions |
| **EVA 6-D** | Validity · Confidence · Risk · Compliance · Stability · Impact — sealed verdict |
| **Client knowledge retrieval** | Tenant-only grounded ask + citations from `ClientKBDoc` |
| **Registry + status** | Models under client control for *registration*; status suspend/block via governance |
| **HITL / Oversight** | BLOCK opens human cases — human primacy |
| **Certificates** | Evidence objects for every decision path |
| **Sector frameworks** | PUBLIC / PRIVATE instrument sets cited on record |
| **GIS (platform)** | Constitutional pillar-gated decisions for Holdings / SETHS path — **UDOC-gated**, not client-owned |
| **GBS alignment** | Franchise / cohort / institutional docs as **reference substrate** for GODS — not client LLM weights |

**Removed from the UDOC Governance Intelligence process flow:**  
- Client personal agentic model as **decision authority**  
- Generic public LLM as **rule author or override**  
- Recursive self-modifying model as **controller of UDOC / GIS**

Those may exist **beside** UDOC as **Layer A**. They talk **to** UDOC through approved APIs. They do not sit **inside** the Primacy controller.

---

## 5. UDOC Primacy controller — usage only

### Client (human)

- Uploads corpus · activates **their** policy packs (where tenancy allows) · runs Govern / Sentinel · reviews HITL.  
- Cannot rewrite Core engine code, platform policy seed, or GIS constitutional gates via Client SaaS.

### Client AI model (Layer A)

Allowed (usage):

- `POST /decisions` (evaluate under active rules)  
- Read registry / certificates / own knowledge ask  
- Receive BLOCK / APPROVE / REVIEW — **obey or escalate to human**

Denied (amendment / control):

- Change platform ACTIVE rule packs that govern all tenants  
- Disable Human Primacy / Pillar guards  
- Write GIS franchise / constitutional tables  
- Elevate itself to operator over UDOC  
- “Fine-tune away” disparate-impact or sovereignty blocks

**Designation path:**  
Client designates a model in **Registry** → that model is a **subject of regulation**.  
UDOC remains the **regulator interface**. Approval of *business outcomes* is client-side; approval of *whether the AI may act under policy* is UDOC.

---

## 6. GODS Intelligence vs UDOC engines

| | UDOC deterministic engines | GODS Intelligence |
|--|---------------------------|-------------------|
| Primary job | Regulate AI decisions (EVA, policy, cert, HITL) | Holdings knowledge + GIS institutional backbone |
| Client corpus | Private tenant KB for grounded ops | Not mixed into `gi_knowledge_docs` |
| Internal corpus | Staff `/intel` separate | GODS internal data room |
| AI-TRANSITION role | Shows governance works before scale | Long-horizon trustworthy substrate for ecosystem |
| Capstone bar | Live smoke: fair ≠ BLOCK, biased = BLOCK + private KB | Documented engines + limits; not commercial super-AI claim |

World-scale “super AI” language stays **aspirational product narrative**, not a Capstone completion criterion. Capstone value = **intent known, control loop live, corpus isolation real, primacy explicit**.

---

## 7. Capstone / Neon honesty

- Neon ≤500MB → text-first corpus, no bulk media training farm.  
- No claim that each client receives a fine-tuned foundation model on free tier.  
- Deterministic path is the **patent-aligned** story: rules + evidence + human primacy.  
- Live APIs: `/client/knowledge/*`, `/decisions`, policy packs, Sentinel smoke.  
- GIS / GBS depth after Task 2 operator smoke green (project priority lock).

---

## 8. Implementation map (repo)

| Concern | Location |
|---------|----------|
| Client private KB | `platform-core/app/routers/client_knowledge.py` · `services/client_knowledge.py` |
| Human primacy guard on ask | `guardrail_check` in client knowledge service |
| EVA + policy | `governance_bridge.py` · `policy_engine.py` · `routers/decisions.py` |
| GIS | `services/gis_engine.py` · `routers/gis.py` |
| Client UI | Client Web **Company Knowledge** · package `client` |
| Isolation EDR | `EDR-002-knowledge-substrate.md` |

---

## 9. Assessor one-liner

> Client Intelligence in this Capstone is a **tenant-private corpus + deterministic UDOC engines**. Client LLMs are **out of band**. UDOC grants **usage**, not control. GODS Intelligence is the **Holdings substrate**, not a rename of EVA.
