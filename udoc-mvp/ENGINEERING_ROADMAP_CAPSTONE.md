# UDOC Capstone · Engineering Roadmap (Intent First)

**Updated:** 2026-07-31  
**Audience:** Assessor · future self · any collaborator reading the repo  
**Stance:** Code changes. Intent must be written first or the code means nothing.

This document records **why** the platform is shaped the way it is under **real constraints** (Render free, Neon ≤500MB, solo Capstone to March 2027). It is not a commercial success plan. Thousands of developers can out-code any free-tier stack. What this repository must prove is **known intention, honest limits, and a coherent governance product story**.

Discipline list: `CAPSTONE_STOP_START_CONTINUE.md`.

---

## 1. Primary value of this Capstone

| Valuable | Not the goal |
|----------|----------------|
| Documented architecture and decision intent | Beating the world on code novelty |
| Live governance loop under free-tier limits | Guaranteed commercial SaaS |
| Clear Internal vs Client package split | Infinite feature surface |
| Honest gap list (what is not claimed) | Marketing completeness |
| Knowledge Substrate named and bounded (EDR-002) | “Docs grew, software didn’t” without purpose |
| Reproducible smoke path | Silent overclaim |

**Rule:** Prefer a smaller system whose purpose is written down over a larger system whose purpose is only in the author’s head.

---

## 2. Constitutional + knowledge stack (intent)

Only **UDOC** is the customer-facing operational product in this Capstone environment (EDR-001). Documentation and corpus are **Knowledge Substrate**, not passive by-products (EDR-002).

```
G.O.D.S              Constitutional authority (intent / holdings)
   │
GBS                  Constitutional framework (policy / franchise structure)
   │
Knowledge Substrate  Canon · policies · client corpus · EDRs (governed source material)
   │
Knowledge Compiler   Intent layer: structure → objects / graph (post-Capstone depth)
   │
GIS                  Deterministic governance intelligence (UDOC-controlled)
   │
EVA                  Evaluation + coordination / acquisition (6-D, fail-closed)
   │
UDOC                 Operational surfaces (Client / Internal / Citizen / Gateway)
   │
Owned agents         Organisation-scoped behaviour from owned knowledge (vision; not Capstone product claim)
```

- Country / university / enterprise difference = **corpus and configuration**, not a software rewrite.  
- Client interaction with company data / policy is the structured path toward **owned intelligence** (deterministic assistance under rules), not a claim of a finished private foundation model on free Neon.  
- GIS / GBS / full Knowledge Compiler product depth = **after** UDOC Capstone bar is honest and live-verified.

---

## 3. Hard environmental constraints (non-negotiable)

| Constraint | Implication |
|------------|-------------|
| Neon ≤ **500MB** | No unbounded registration; demo seed only; no large file corpora in DB |
| Render free · ~20 service cap | **No new services** for features that fit existing hosts |
| Auto-deploy from `main` | Prefer small, reversible commits; freeze working modules |
| Solo Capstone · March 2027 | Scope = documented UDOC MVP + evidence, not full GODS commercial stack |
| Pre-registration honesty | No company/trademark claims as live legal entities |

Every new module must answer: *Does this fit these limits without lying about capacity?*

---

## 4. Freeze list (do not rebuild)

Unless a **bug** or **assessor-blocking smoke failure** exists, leave these alone:

| Module | Status |
|--------|--------|
| Core auth (JWT / operator login) | Freeze |
| Registry + demo seed `model-001` | Freeze |
| EVA `POST /decisions` + 6-D + policy_enforced | Freeze |
| Policy packs activate path | Freeze |
| Citizen public `/citizen/*` | Freeze |
| 24 portals dual-path → OversightCase | Freeze |
| Package split (Internal Desktop/Web vs Client Desktop/Web/App/Mobile) | Freeze |
| Gateway role → host routing | Freeze |
| Sentinel Command / Smoke path | Freeze (fix fails only) |

**Do not** restart frameworks, rewrite auth for aesthetics, or add parallel Render services for the same UI.

---

## 5. Capstone bar (definition of “enough”)

Assessor-facing minimum:

1. **Internal path** — staff Admin / Sentinel / Portals / Core `/admin`  
2. **Client path** — tenant Models · Reports · Policy · Govern (no staff kill-switch plane)  
3. **Citizen** — public AI-Rights surface, no login  
4. **Gateway** — role routes to the correct package  
5. **Live smoke** — health + `/udoc/demo/ready` + **biased = BLOCK** on Client Govern and Sentinel  

Task 2 remains open until item 5 is **operator-verified live**. Commits do not close it.

Package map: `UDOC_MVP_PACKAGE_MATRIX.md` · `CAPSTONE_PACKAGE_STORY.md`.

---

## 6. Phased work after the bar (intent order)

| Phase | Intent | Status in this repo |
|-------|--------|---------------------|
| **A. Honesty + smoke** | Prove live loop; freeze Capstone software claim | In progress (M7 operator) |
| **B. Intent artefacts** | Roadmap, EDRs, package story, stop/start/continue | This file + siblings |
| **C. Isolation proof** | Document + test tenant A cannot read tenant B when multi-tenant is claimed | Documented gap |
| **D. Policy / corpus as substrate** | Policy lifecycle + small corpus under 500MB; name substrate in UI/docs | Partial (packs + intel paths live) |
| **E. GIS under UDOC control** | Access control + approved open path — not parallel product | Deferred until A green |
| **F. Knowledge Compiler depth** | Structure corpus → objects for deterministic use | Intent only (EDR-002) |
| **G. GBS / holdings narrative** | Framework docs; no free-tier DB expansion | Deferred |
| **H. Open-source packaging story** | README · run · limits · honesty | Partial |
| **I. Capstone evidence pack** | Smoke record · screenshots · architecture pointers | After A |
| **J. Enterprise packaging** | SSO, connectors, hierarchical orgs, support ops | **Out of Capstone** (Volume 4 Part 7 reference only) |

Never start E–G before A is honest. Never treat J as a Capstone blocker.

---

## 7. What “commercial / Enterprise” means here

Commercial and Enterprise readiness are **explicitly not** Capstone success criteria.

- Documented in `UDOC_SAAS_READINESS_GAP.md`.  
- Volume 4 Part 7 (Enterprise Edition) is a **future packaging reference**, not a build order for free Neon.  
- Architecture can be Capstone-ready while operations (MFA, proven isolation, backups, monitoring) are not pilot-ready.  
- Saying “not commercial SaaS” is honesty, not a failure of vision.

---

## 8. Documentation hierarchy for assessors

| Doc | Intent |
|-----|--------|
| `ENGINEERING_ROADMAP_CAPSTONE.md` (this file) | Why / order / freeze / constraints |
| `CAPSTONE_STOP_START_CONTINUE.md` | Discipline |
| `CAPSTONE_PACKAGE_STORY.md` | Demos → Internal vs Client channels |
| `UDOC_MVP_PACKAGE_MATRIX.md` | Package progress checklist |
| `UDOC_LIVE_ENVIRONMENTS.md` | What is actually hosted |
| `UDOC_SMOKE_PASS.md` · `P6_ASSESSOR_SIDE_BY_SIDE.md` | How to verify live |
| `UDOC_SAAS_READINESS_GAP.md` | What is not claimed |
| `UDOC_V93_DEMO67_PATENT_CONTROLS.md` | Patent/control map demos 6–7 |
| `EDR-001-*.md` | UDOC-only deploy layer |
| `EDR-002-*.md` | Knowledge Substrate |
| Engineering Canon `docs/` volumes | Long-form design law (substrate) |

---

## 9. Commit discipline (intent in history)

- Prefer commits that **state intent** in the message (what decision, what limit).  
- Prefer updating these `.md` files when direction changes — before large code thrash.  
- Prefer fixing smoke failures over adding surfaces.  
- Prefer one coherent Capstone story over parallel unfinished products.  
- Prefer substrate that feeds policy/corpus over unscoped philosophy pages.

---

## 10. One-sentence position

**This Capstone documents a constrained, live UDOC governance platform — with a named Knowledge Substrate and written limits — so that code can change without the purpose disappearing, and without claiming Enterprise or commercial certainty.**
