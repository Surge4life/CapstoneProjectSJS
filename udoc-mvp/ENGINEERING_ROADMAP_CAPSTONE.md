# UDOC Capstone · Engineering Roadmap (Intent First)

**Updated:** 2026-07-31  
**Audience:** Assessor · future self · any collaborator reading the repo  
**Stance:** Code changes. Intent must be written first or the code means nothing.

This document records **why** the platform is shaped the way it is under **real constraints** (Render free, Neon ≤500MB, solo Capstone to March 2027). It is not a commercial success plan. Thousands of developers can out-code any free-tier stack. What this repository must prove is **known intention, honest limits, and a coherent governance product story**.

---

## 1. Primary value of this Capstone

| Valuable | Not the goal |
|----------|----------------|
| Documented architecture and decision intent | Beating the world on code novelty |
| Live governance loop under free-tier limits | Guaranteed commercial SaaS |
| Clear Internal vs Client package split | Infinite feature surface |
| Honest gap list (what is not claimed) | Marketing completeness |
| Reproducible smoke path | Silent overclaim |

**Rule:** Prefer a smaller system whose purpose is written down over a larger system whose purpose is only in the author’s head.

---

## 2. Constitutional stack (intent)

Only **UDOC** is the customer-facing operational product. Higher layers define behaviour; they are not separate paid apps in this Capstone environment.

```
G.O.D.S     Constitutional authority (intent / holdings)
   │
GBS         Constitutional framework (policy / franchise structure)
   │
GIS         Deterministic governance intelligence (corpus → rules)
   │
EVA         Evaluation + coordination (6-D, fail-closed)
   │
UDOC        Operational surfaces (Client / Internal / Citizen / Gateway)
```

- Country / university / enterprise difference = **corpus and configuration**, not a software rewrite.  
- GIS / GBS product depth = **after** UDOC Capstone bar is honest and live-verified.  
- See also: `EDR-001-udoc-only-deploy-layer.md`.

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

Aligned with external engineering review (Volume 4 style) **mapped onto this repo**, not a greenfield rewrite:

| Phase | Intent | Status in this repo |
|-------|--------|---------------------|
| **A. Honesty + smoke** | Prove live loop; freeze Capstone software claim | In progress (M7 operator) |
| **B. Intent artefacts** | Roadmap, EDRs, package story, gap list | This file + siblings |
| **C. Isolation proof** | Document + test that tenant A cannot read tenant B (when multi-tenant is claimed) | Documented gap; not yet proven |
| **D. Policy / corpus depth** | Stronger policy lifecycle docs + small corpus under 500MB rules | Partial (packs live) |
| **E. GIS under UDOC control** | Access control + approved open path — **not** parallel product | Deferred until A green |
| **F. GBS / holdings narrative** | Framework docs; no free-tier DB expansion | Deferred |
| **G. Open-source packaging story** | README · run · limits · honesty | Partial |
| **H. Capstone evidence pack** | Smoke record · screenshots · architecture pointers | After A |

Never start E before A is honest. Never treat F–G as Capstone blockers.

---

## 7. What “commercial SaaS” means here

Commercial SaaS readiness is **explicitly not** the Capstone success criterion.

- Documented in `UDOC_SAAS_READINESS_GAP.md`.  
- Architecture can be Capstone-ready while operations (MFA, proven isolation, backups, monitoring) are not pilot-ready.  
- Saying “not commercial SaaS” is a feature of honesty, not a failure of vision.

---

## 8. Documentation hierarchy for assessors

| Doc | Intent |
|-----|--------|
| `ENGINEERING_ROADMAP_CAPSTONE.md` (this file) | Why / order / freeze / constraints |
| `CAPSTONE_PACKAGE_STORY.md` | Demos → Internal vs Client channels |
| `UDOC_MVP_PACKAGE_MATRIX.md` | Package progress checklist |
| `UDOC_LIVE_ENVIRONMENTS.md` | What is actually hosted |
| `UDOC_SMOKE_PASS.md` · `P6_ASSESSOR_SIDE_BY_SIDE.md` | How to verify live |
| `UDOC_SAAS_READINESS_GAP.md` | What is not claimed |
| `UDOC_V93_DEMO67_PATENT_CONTROLS.md` | Patent/control map demos 6–7 |
| `EDR-001-*.md` | Single durable engineering decision |
| Engineering Canon `docs/` volumes | Long-form design law |

---

## 9. Commit discipline (intent in history)

- Prefer commits that **state intent** in the message (what decision, what limit).  
- Prefer updating these `.md` files when direction changes — before large code thrash.  
- Prefer fixing smoke failures over adding surfaces.  
- Prefer one coherent Capstone story over parallel unfinished products.

---

## 10. One-sentence position

**This Capstone documents a constrained, live UDOC governance platform whose intentions, limits, and package boundaries are written down so that code can change without the purpose disappearing.**
