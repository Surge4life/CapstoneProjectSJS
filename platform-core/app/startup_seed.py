"""Capstone startup seeds — GLM intel under UDOC primacy (Neon-light)."""
from __future__ import annotations

def ensure_udoc_demo_seed():
    try:
        from app.db.session import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        try:
            db.execute(text("UPDATE ai_systems SET status='ACTIVE' WHERE model_id='model-001' OR id='model-001'"))
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()
    except Exception as e:
        print(f"[startup_seed] udoc demo: {e}")

def ensure_client_kb_demo_seed():
    pass

def ensure_division_staff_seed():
    pass

GLM_INTEL_SEED = [
  {
    "title": "GLM Definition \u2014 Deterministic HITL Governance Model",
    "category": "GOVERNANCE",
    "division": "GODS",
    "tags": "glm,udoc,not-llm,layer-b",
    "source": "00_INTEGRITY_MANIFEST_AND_STORY.md",
    "body": "GODS Language Model (GLM) = Deterministic Human-In-The-Loop Governance Model \u2014 NOT an LLM.\n\nLayer A \u2014 Client / optional generative assist: subordinate, never controller.\nLayer B \u2014 UDOC deterministic (policy, EVA, fail-closed, audit): YES controller.\nLayer C \u2014 GODS / GIS corpus: structured knowledge substrate; feeds B; does not override B.\n\nGeneric LLM fluency is not the controller. Structured corpus + rules + evaluation + audit are.\nAny local or cloud LLM may be steered by this governance model. It does not replace it.\n\nCapstone posture: process of thought \u2192 structured corpus \u2192 deterministic control plane.\nFull ~10GB GIS corpus remains on Drive for institutional-scale ingest when funding/hardware allow.\nThis seed is the integrity core only."
  },
  {
    "title": "GODS Intelligence Operating Method \u2014 Principle",
    "category": "INTELLIGENCE_METHOD",
    "division": "GODS",
    "tags": "method,pipeline,verify,hitl",
    "source": "GODS_INTELLIGENCE_OPERATING_METHOD.md",
    "body": "# G.O.D.S Intelligence Operating Method\n## Incorporating structured prompt discipline into deterministic GIS / GBS / UDOC intelligence\n\n**Status:** Capstone design incorporation \u2014 not a claim of commercial LLM product  \n**Authority:** UDOC deterministic primacy \u00b7 Layer B policy-to-code \u00b7 Layer C GODS/GIS corpus  \n**Date:** 2026-08-14  \n**Source stimulus:** Application of *Killer ChatGPT Prompts* (Hart-Davis) methodology to G.O.D.S \u2014 adapted away from product-specific 2023 ChatGPT features toward durable operating method.\n\n---\n\n## 1. Principle (non-negotiable)\n\n| Layer | Role | Controller? |\n|-------|------|-------------|\n| **A \u2014 Client models** | Usage / optional assist | No |\n| **B \u2014 UDOC deterministic** | Policy, EVA, fail-closed, audit | **Yes (primacy)** |\n| **C \u2014 GODS / GIS corpus** | Structured knowledge substrate | Feeds B; does not override B |\n\nGeneric LLM fluency is **not** the controller.  \nStructured corpus + rules + evaluation + audit **are**.\n\nThe book\u2019s durable contribution is **discipline**, not plugins or token limits:\n\n> structured input \u2192 constrained task \u2192 iterate \u2192 analyze \u2192 verify \u2192 controlled output\n\nThat maps directly onto UDOC\u2019s existing fail-closed, evidence, and HITL posture.\n\nFull method body and agent roles live in GODS_INTELLIGENCE_OPERATING_METHOD.md (Drive + udoc-mvp)."
  },
  {
    "title": "Doctrine \u2014 Human Primacy, AI Governance, Sovereign Control",
    "category": "GOVERNANCE",
    "division": "GODS",
    "tags": "doctrine,human-primacy,sovereignty,01",
    "source": "a-01_doctrine.txt",
    "body": "DOCTRINE ON HUMAN PRIMACY, AI GOVERNANCE, AND SOVEREIGN CONTROL\n\nA Constitutional Text for the Lawful Direction of Advanced Intelligence\n\nFor the G.O.D.S collection\n\nFOUNDER\u2019S INVOCATION\n\nTechnology does not become dangerous only when it grows powerful. It becomes dangerous when power grows faster than discipline, faster than governance, and faster than the moral courage required to restrain it.\n\nHuman primacy is non-negotiable. AI systems are instruments under lawful human direction. Sovereign control means jurisdiction, audit, fail-closed evaluation, and the right to refuse deployment that cannot be governed.\n\n[Full doctrine body on Drive GLM pilot / GIS corpus folder 01]"
  },
  {
    "title": "Founder Doctrine \u2014 Process of Thought",
    "category": "GOVERNANCE",
    "division": "GODS",
    "tags": "founder,doctrine,01",
    "source": "a-03_founder_doctrine.txt",
    "body": "G.O.D.S\n\nFOUNDER DOCTRINE\n\n& ORIGIN PAPER\n\nThe Origin, Philosophy, Personal Mandate, and Limits of the Founder \u2014 Sashin J. Singh\n\nSashin J. Singh \u2014 Founder & Architect | G.O.D.S Holdings | Johannesburg, 2026\n\nPART ONE \u2014 THE ORIGIN\n\nWhere This Started: 2016\n\nG.O.D.S did not begin as a business idea. It began as a response to a specific, observable failure \u2014 the failure of existing systems to reintegrate people after disruption, and the absence of a constitutional layer between capability and deployment.\n\nProcess of thought: observe failure \u2192 name governance gap \u2192 design control plane \u2192 bind to evidence and audit.\n\n[Full founder doctrine on Drive GLM pilot]"
  },
  {
    "title": "GODS Constitutional Governance Charter",
    "category": "GOVERNANCE",
    "division": "GODS",
    "tags": "constitution,charter,01",
    "source": "a-02_constitutional_charter.txt",
    "body": "G.O.D.S\n\nCONSTITUTIONAL GOVERNANCE CHARTER\n\n& MEMORANDUM OF INCORPORATION BLUEPRINT\n\nThe Legal Governance Architecture, Share Structure, MOI Blueprint, and Constitutional Constraints of G.O.D.S Holdings\n\nSashin J. Singh \u2014 Founder & Architect | G.O.D.S Holdings | Johannesburg, 2026 \u2014 DRAFT FOR LEGAL REVIEW\n\nPART ONE \u2014 THE CORPORATE ARCHITECTURE\n\nThe Five-Entity Structure\n\nG.O.D.S operates through a holdings + four-division model (SETHS, TS, MADIBA, UDOC-controlled surfaces) with GBS as constitutional standard, not a fifth operating division.\n\n[Full charter on Drive GLM pilot]"
  },
  {
    "title": "UDOC EVA Whitepaper \u2014 Evaluation Control Plane",
    "category": "UDOC",
    "division": "UDOC",
    "tags": "eva,udoc,fail-closed,05",
    "source": "e-10_eva_whitepaper.txt",
    "body": "01  EXECUTIVE SUMMARY\n\nEVA \u2014 Evaluating Valiant Algorithms \u2014 is the G.O.D.S UDOC AI decision governance and evaluation engine. EVA provides a structured, multi-dimensional framework for assessing the validity, reliability, risk, compliance, stability, and impact of AI systems operating within governed jurisdictions, with specific alignment to the South African Draft National AI Policy (GG No.54477).\n\nFail-closed posture: when evidence is insufficient or policy is violated, the default is BLOCK / escalate, not silent APPROVE.\n\nLive Capstone gate: fair scenario \u2192 APPROVE; biased scenario \u2192 BLOCK.\n\n[Full EVA whitepaper on Drive GLM pilot / folder 05]"
  },
  {
    "title": "UDOC Technical Whitepaper \u2014 Control Architecture",
    "category": "UDOC",
    "division": "UDOC",
    "tags": "udoc,technical,architecture,05",
    "source": "e-15_udoc_technical_whitepaper.txt",
    "body": "TABLE OF CONTENTS Full Technical Whitepaper v2.0\n\nSECTION 01\n\nEXECUTIVE SUMMARY Platform identity, mandate, and key technical metrics\n\nUDOC \u2014 Unified Digital Oversight & Coordination \u2014 is not a software product. It is sovereign digital governance infrastructure: the technical backbone allowing governments and regulated enterprises to govern AI systems, protect national data sovereignty, and generate auditable decision records.\n\nLayer B controller: policy-to-code, EVA, registry, audit, HITL. Layer A assist is optional and subordinate.\n\n[Full technical whitepaper on Drive GLM pilot]"
  },
  {
    "title": "GBS-SETHS Consolidated Super Framework",
    "category": "GBS",
    "division": "SETHS",
    "tags": "gbs,seths,framework,07",
    "source": "gbs_seths_00_super_framework.txt",
    "body": "G . O . D . S   H O L D I N G S\n\nGOOD ORDERLY DIRECTIONAL SYSTEMS  \u00b7  GBS-SETHS INSTITUTIONAL READINESS PACKAGE\n\nDOCUMENT 00 of 11 \u2014 CONSOLIDATED FOUNDATION OF 11\n\nGBS-SETHS\n\nGlobal Belief System \u00b7 Systematically Engineered Transfer of Human Systems\n\nCONSOLIDATED SUPER FRAMEWORK \u00b7 v3.0 \u00b7 MERGES v1.0 + v2.0 INTO ONE MASTER INSTITUTIONAL DOCUMENT\n\nVersion 3.0 \u00b7 July 2026\n\nGBS is the constitutional standard under which SETHS develops learners and hands off to TS. Capital remains not_deployed until governance gates clear.\n\n[Full super framework on Drive GLM pilot / folder 07]"
  },
  {
    "title": "GBS-SETHS GIS Architecture Specification",
    "category": "GBS",
    "division": "SETHS",
    "tags": "gis,architecture,gbs,07",
    "source": "gbs_seths_06_gis_architecture.txt",
    "body": "G . O . D . S   H O L D I N G S\n\nGOOD ORDERLY DIRECTIONAL SYSTEMS  \u00b7  GBS-SETHS INSTITUTIONAL READINESS PACKAGE\n\nDOCUMENT 06 of 11 OF 11\n\nGIS Architecture Specification\n\nThe G.O.D.S. Intelligence System \u2014 Full Technical Architecture, Including Geospatial Node Monitoring\n\nTECHNICAL SPECIFICATION \u00b7 THE LEVEL-6 AI BACKBONE, ITS SEVEN FUNCTIONS, AND ITS NODE-INTEGRITY MONITORING LAYER\n\nVersion 1.0\n\nGIS under UDOC: 12-pillar fail-closed operational in platform-core; nodes empty until funded scale. Corpus authority remains on Drive.\n\n[Full GIS architecture on Drive GLM pilot]"
  },
  {
    "title": "GBS-SETHS Institutional Constitution",
    "category": "GBS",
    "division": "SETHS",
    "tags": "gbs,constitution,07",
    "source": "gbs_seths_01_constitution.txt",
    "body": "G . O . D . S   H O L D I N G S\n\nGOOD ORDERLY DIRECTIONAL SYSTEMS  \u00b7  GBS-SETHS INSTITUTIONAL READINESS PACKAGE\n\nDOCUMENT 01 of 11 OF 11\n\nGBS-SETHS Institutional Constitution\n\nThe Master Authority Document\n\nCONSTITUTIONAL INSTRUMENT \u00b7 DEFINES THE BINDING GOVERNANCE ARCHITECTURE OF GBS-SETHS WITHIN G.O.D.S.\n\nVersion 1.0 \u00b7 July 2026 \u00b7 Companion to the GBS-SETHS Consolidated Super Framework\n\n[Full institutional constitution on Drive GLM pilot]"
  },
  {
    "title": "Smoke Evidence 2026-08-16 \u2014 EVA Gate PASS",
    "category": "CAPSTONE_EVIDENCE",
    "division": "GODS",
    "tags": "smoke,eva,fair,biased,12",
    "source": "SMOKE_EVIDENCE_2026-08-16.md",
    "body": "# Smoke Evidence \u00b7 2026-08-16\n\n**Operator / automation probe** \u00b7 Capstone free-tier stack  \n**Procedures:** ASSESSOR_ENVIRONMENTAL_PROCEDURES.md \u00a74  \n\n## Results\n\n| Check | Result |\n|-------|--------|\n| GET /health | **PASS** \u00b7 `status: ok` \u00b7 service GODS Platform Core \u00b7 environment production |\n| GET /udoc/demo/ready | **PASS** \u00b7 ready true (model-001 path) |\n| POST /decisions/batch fair+biased | **PASS** \u00b7 fair=APPROVE \u00b7 biased=BLOCK \u00b7 ERROR=0 |\n\n## Notes\n\n- Free Render cold start may delay first hit 30\u201360s  \n- Density freeze in effect (DENSITY_FREEZE.md)  \n- Full environmental path: ASSESSOR_ENVIRONMENTAL_PROCEDURES.md  \n\n## Hosts spot-check (HTTP)\n\n| Host | Code |\n|------|------|\n| gods-platform-internal | 200 |\n| gods-udoc-gateway | 200 |\n| gods-udoc-client | 200 |\n| gods-udoc-sector | 200 |\n| gods-udoc-admin | 200 |\n| gods-udoc-operator | 200 |\n| capstoneprojectsjs.netlify.app | 200 |\n\n---\n\n*Dated evidence for assessor pack \u00b7 not a guarantee of continuous uptime on free tier*"
  },
  {
    "title": "Limitations Register \u2014 Capstone Honesty Bounds",
    "category": "CAPSTONE_EVIDENCE",
    "division": "GODS",
    "tags": "limitations,honesty,neon,12",
    "source": "LIMITATIONS_REGISTER.md",
    "body": "# UDOC Capstone \u00b7 Limitations register\n\n**Purpose:** Explicit list of known limits so assessors do not have to infer gaps from silence.  \n**Updated:** 2026-08-14  \n**Stance:** Naming a limitation is integrity, not failure.\n\n---\n\n## Infrastructure\n\n| Limitation | Effect | Mitigation / honesty |\n|------------|--------|----------------------|\n| Neon \u2264500MB | Cannot treat DB as unbounded user/corpus store | Demo seed; no-registration smoke (`EDR-004`); gap doc |\n| Render free tier | Cold starts; service count cap | Existing hosts only; document wake behaviour |\n| No paid always-on SLA | Pilot SLAs not offered | Not claimed as commercial SaaS |\n| External Neon (Render Postgres expired) | Dependency on Neon availability | Core config; DR still weak (gap doc) |\n\n## Product / governance\n\n| Limitation | Effect | Mitigation / honesty |\n|------------|--------|----------------------|\n| Operator UI evidence not yet signed | API gates green; formal Task 2 close needs operator hard-refresh tick on Client + Sentinel | `SMOKE_EVIDENCE_TEMPLATE.md` |\n| Full ~10GB GIS corpus | Offline on Drive; Neon holds integrity seed only | Pilot slice + GLM seed; institutional ingest post-funding |\n\nHonesty bound: Capstone demonstrates the control plane and integrity core, not unbounded corpus scale on free tier."
  }
]

def ensure_glm_intel_seed():
    from app.db.session import SessionLocal
    from app.db.models import KnowledgeDoc
    from sqlalchemy import select
    from app.services import gods_intelligence as gi
    db = SessionLocal()
    try:
        existing = {(r or "").strip() for r in db.execute(select(KnowledgeDoc.title)).scalars().all()}
        added = 0
        for c in GLM_INTEL_SEED:
            title = c["title"]
            if title in existing:
                continue
            gi.ingest(db, title=title, source=c.get("source") or "glm_pilot",
                      category=c.get("category") or "GENERAL", division=c.get("division") or "GODS",
                      text=c.get("body") or "", added_by="startup_glm_seed",
                      tags=c.get("tags") or "glm,capstone")
            added += 1
            existing.add(title)
        print(f"[startup_seed] GLM intel: added={added} total_seed={len(GLM_INTEL_SEED)}")
    except Exception as e:
        print(f"[startup_seed] GLM intel error: {e}")
        try:
            db.rollback()
        except Exception:
            pass
    finally:
        db.close()
