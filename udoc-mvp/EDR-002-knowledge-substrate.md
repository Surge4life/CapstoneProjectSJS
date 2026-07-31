# EDR-002 · Documentation and corpus are the Knowledge Substrate

**Status:** Accepted  
**Date:** 2026-07-31  
**Context:** CapstoneProjectSJS · Intelligence path under free-tier limits · March 2027

## Problem

Traditional software reviews treat documentation as a by-product of code. In this architecture that framing is wrong: policies, manuals, regulations, SOPs, and client-uploaded company material are intended to become **governed source material** for organisation-specific intelligence — not passive README pages and not “chat over PDFs.”

Without naming that role, assessors and collaborators will under-value the written corpus and over-value speculative model training claims.

## Decision

Treat the following as the **Knowledge Substrate** (Knowledge Layer), not as optional docs:

- Constitutional and engineering Canon (`docs/` volumes)
- Policy packs and legislation uploaded into UDOC
- Client / tenant corpus (text and, where capacity allows, documents)
- Intent records (EDRs, roadmap, package story, gap list)

**Pipeline intent (full vision):**

```
Human knowledge (policies, SOPs, law, company data)
        │
Knowledge Engineering (classify · version · authority · metadata)
        │
Knowledge Compiler (structure → objects / graph)
        │
GIS (deterministic governance intelligence / rule execution)
        │
EVA (evaluation + acquisition / workflow coordination)
        │
UDOC (Client & Internal surfaces)
        │
Organisation- or user-scoped agents (owned knowledge, not rented LLM-only behaviour)
```

**Capstone slice of that vision (what is honest today):**

- Policy upload → compile rules → activate → EVA enforces on decisions (live path exists).
- Tenant Intelligence / corpus endpoints exist under Neon size limits (text-first; no unbounded file hoarding).
- Client package can point at **own** data for deterministic assistance — not a claim of a finished custom foundation model product.
- Full Knowledge Compiler + personalised agent product = **post–Capstone / post–smoke** work, documented as intent now so code later has a target.

## Positioning (what is differentiated)

Stronger claim than “another chatbot”:

- People and organisations should **own and evolve their own intelligence** from their own corpus.
- Deterministic governance where rules apply; human primacy on oversight.
- Avoid positioning Capstone success as “beat OpenAI.” Position it as **structured, governed knowledge → deterministic decision path under written constraints**.

## Alternatives considered

1. **Docs are only for humans reading the repo** — rejected; corpus is runtime feedstock for policy and intelligence paths.  
2. **Primary value = train a better general LLM first** — deferred; free tier and Capstone timeline cannot honestly host that as the main deliverable.  
3. **Skip structure and rely on prompt-only PDF chat** — rejected; contradicts fail-closed / deterministic governance intent.

## Consequences

- When documentation grows, ask: *is this becoming substrate or is it unscoped philosophy?* Substrate that feeds policy/corpus/GIS is allowed; endless redesign without a finished UDOC loop is not.  
- Neon ≤500MB remains binding: large Drive-scale corpora stay **out of** the free DB; client text upload and curated packs are the Capstone pattern.  
- GIS remains **UDOC-controlled** (EDR-001); Knowledge Compiler is an intent layer, not a new Render service in this phase.  
- Enterprise multi-tenant hierarchy, SSO, connectors, sovereign national deploy (Volume 4 Part 7) stay **future packaging**, not Capstone blockers.

## Related

- `ENGINEERING_ROADMAP_CAPSTONE.md`  
- `EDR-001-udoc-only-deploy-layer.md`  
- `CAPSTONE_STOP_START_CONTINUE.md`  
- Client Intelligence notes in live Client / `udoc-app` tenancy · intel surfaces  
