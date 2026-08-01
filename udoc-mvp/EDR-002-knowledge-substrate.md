# EDR-002 · Documentation and corpus are the Knowledge Substrate

**Status:** Accepted  
**Date:** 2026-07-31 · amended 2026-08-01  
**Context:** CapstoneProjectSJS · Intelligence path under free-tier limits · March 2027

## Problem

Traditional software reviews treat documentation as a by-product of code. In this architecture that framing is wrong: policies, manuals, regulations, SOPs, and client-uploaded company material are intended to become **governed source material** for organisation-specific intelligence — not passive README pages and not “chat over PDFs.”

Without naming that role, assessors conflate (a) **client LLMs**, (b) **UDOC deterministic governance**, and (c) **GODS Intelligence / GIS**.

## Decision

Treat the following as the **Knowledge Substrate** (Knowledge Layer), not as optional docs:

- Constitutional and engineering Canon (`docs/` volumes)
- Policy packs and legislation uploaded into UDOC
- Client / tenant corpus (text and, where capacity allows, documents)
- Intent records (EDRs, roadmap, package story, gap list)

**Three-layer split (mandatory):**

1. **Client operational AI** — agentic / generic / recursive models the client already runs. **Usage consumer** of UDOC only.  
2. **UDOC Governance Intelligence** — deterministic engines (policy-to-code, EVA, cert, HITL). **Primacy controller**.  
3. **GODS Intelligence / GIS** — Holdings substrate and constitutional GIS; **not** client-writable; **not** the same as “an LLM product.”

Detail: `CLIENT_GOVERNANCE_INTELLIGENCE.md`.

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
EVA (evaluation + workflow coordination)
        │
UDOC (Client & Internal surfaces · Primacy grants USAGE only)
        │
Organisation-scoped agents (owned knowledge) ── parallel, not controller
```

**Capstone slice (honest today):**

- Policy upload → compile rules → activate → EVA enforces (live).  
- Tenant corpus endpoints under Neon limits (text-first).  
- Grounded ask + citations — **no LLM required** in the governance path.  
- Full Compiler + personalised agent product + world-scale GODS AI = **post–Capstone intent**.

## Positioning

- Own and evolve intelligence from **own corpus**.  
- Deterministic governance where rules apply; **human primacy** on oversight.  
- UDOC **declines** generic/higher models as **controllers** of the system that regulates AI.  
- Capstone success ≠ “beat OpenAI.” Capstone success = **structured corpus → deterministic decision path under written constraints**.

## Alternatives considered

1. **Docs only for humans** — rejected; corpus is runtime feedstock.  
2. **Primary value = train a general LLM first** — deferred under free tier / timeline.  
3. **Prompt-only PDF chat as governance** — rejected; contradicts fail-closed intent.  
4. **Client model amends UDOC/GIS** — rejected; patent / primacy posture.

## Consequences

- Substrate that feeds policy/corpus/GIS is allowed; unscoped philosophy without a finished UDOC loop is not.  
- Neon ≤500MB binding.  
- GIS remains **UDOC-controlled** (EDR-001).  
- Enterprise Volume 4 Part 7 packaging stays future, not Capstone blocker.

## Related

- `CLIENT_GOVERNANCE_INTELLIGENCE.md`  
- `CLIENT_INTELLIGENCE.md`  
- `ENGINEERING_ROADMAP_CAPSTONE.md`  
- `EDR-001-udoc-only-deploy-layer.md`  
- `CAPSTONE_STOP_START_CONTINUE.md`  
