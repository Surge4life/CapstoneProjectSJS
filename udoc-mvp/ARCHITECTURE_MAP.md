# UDOC Capstone · Architecture map (one page)

**Date:** 2026-07-31  
**Intent:** Single diagram of what deploys and what only governs.  
**Detail:** `UDOC_LIVE_ENVIRONMENTS.md` · decisions: `EDR-001` · `EDR-002` · `EDR-003`

---

## Layer stack (intent)

```
                    G.O.D.S
            constitutional authority
                       │
                      GBS
            constitutional framework
                       │
                      GIS
         deterministic intelligence
              (UDOC-controlled)
                       │
                      EVA
           evaluate · coordinate
                       │
                   ★ UDOC ★
            operational product
         (only layer deployed to users)
```

Country / sector difference = **corpus + policy configuration**, not a fork of UDOC.

---

## Deployed Capstone shape

```
                         ┌──────────────────────┐
         Gateway SSO ───►│  platform-core (API)  │◄── Neon ≤500MB
                         │  auth · registry      │
   ┌─────────────────────│  decisions / EVA      │
   │                     │  policy · oversight   │
   │                     │  citizen · portals    │
   │                     │  /Sentinel /admin     │
   │                     └──────────────────────┘
   │
   ├── Client package ──► Client Web · Desktop Client · App/Mobile · SaaS Portals
   │                         └─ /citizen.html (public)
   │
   └── Internal package ► Admin Web · Desktop Internal · Operator
                              + Core /portals · /Sentinel · /admin
```

**Static hosts** = chrome and package identity.  
**Core + Neon** = state and governance logic.  
**Fail-closed** when demo seed / policy missing.

---

## Package boundary (summary)

| Package | May show | Must not show as product |
|---------|----------|---------------------------|
| **Client** | Models · Reports · Policy · EVA Govern · Tenancy · Citizen link | Kill-switch plane · staff Access Control · global jobs |
| **Internal** | Command · HITL · Kill-switch · Portals dual-path · Jobs · Constitutional admin | Claim that this *is* the tenant SaaS product |
| **Citizen** | Challenge · status · rights | Login requirement for basic rights UI |

---

## Capstone bar (reminder)

Internal path · Client path · Citizen · Gateway · **live biased = BLOCK** on Client + Sentinel.

Free-tier limits are **accepted** (`EDR-003`). Commercial SaaS is **not** the success criterion.
