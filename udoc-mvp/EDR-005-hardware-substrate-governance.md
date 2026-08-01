# EDR-005 · Hardware substrate is required for full UDOC governance (software alone is advisory)

**Status:** Accepted  
**Date:** 2026-08-01  
**Context:** CapstoneProjectSJS · UDOC whitepaper / patent posture · free-tier test environment

## Problem

Observers often treat UDOC as “another dashboard + model API.” In that reading, EVA is a **reporter**: scores, logs, certificates, recommendations. The patent and technical package claim something stronger: **governance** — the ability to **enforce** (block, isolate, throttle, attest, open HITL, cut a path) where computation and data movement actually occur.

Pure software policy on commodity cloud can be observed, patched, hot-swapped, or inverted by privileged access, supply-chain compromise, or control of the same host it is meant to govern. Without a **hardware (or hardware-enforced) substrate** under UDOC / attested control, the same logic **cannot reliably compel** outcomes at the node, enclave, or client-cloud boundary.

## Decision

Treat the following as a **design invariant**:

1. **Software layer** (policy-to-code, EVA 6-D, audit, certs, Client/Internal surfaces, portals) implements **decision logic, evidence, and control-plane APIs**.  
2. **Hardware / infrastructure layer** (purpose-built or tightly coupled nodes, TEEs, measured boot, remote attestation, physical or cryptographically enforced isolation, control over client-cloud execution paths) is what converts those decisions into **non-bypassable governance actions**.  
3. **Without that substrate**, EVA and UDOC in deployment are correctly described as **working-environment / Capstone software**: logic, telemetry, fail-closed *application* behaviour — **not** a claim of silicon-enforced governance on arbitrary hosts.  
4. Capstone **intentionally** runs the **software bootloaders and governance loop** on Render + Neon so intention, audit path, and biased=BLOCK behaviour are **inspectable**. Full-stack hardware-in-the-loop validation is **post-Capstone / patent implementation** depth.

```
Whitepaper / patent claim
        │
        ├─ Software: decide · seal · evidence · HITL · Primacy APIs
        │
        └─ Hardware substrate: enforce at node / enclave / fabric / client-cloud path
                    │
                    ▼
           EVA as governance engine (compel)

Capstone free-tier test environment (this repo live)
        │
        └─ Software only on shared cloud + Neon
                    │
                    ▼
           EVA as decision + evidence engine (demonstrate logic;
           application-level fail-closed; not silicon-rooted compulsion)
```

## Practical implications

| Concern | Software-only (Capstone live) | Full UDOC package (patent target) |
|---------|-------------------------------|-----------------------------------|
| BLOCK decision | Recorded, certified, HITL case opened | Same **plus** enforceable isolation / path control at substrate |
| Adversary with host privilege | Can attack application tier | Must defeat attestation / hardware roots / physical controls |
| Client cloud models | API usage under Primacy (usage only) | Usage **and** node-level policy propagation where deployed |
| Testing | Logic, smoke, corpus isolation, packages | Attestation, non-bypassable effect, compromise resistance |

## Capstone validation (what we *do* prove here)

- Decision trees and policy-to-code fire correctly (e.g. biased → **BLOCK**).  
- Evidence objects and audit path exist.  
- Human primacy and client/internal isolation are explicit in software.  
- Intent is documented so hardware phase has a fixed software law to bind to.

## Capstone non-claims (what we *do not* prove here)

- Measured boot / remote attestation of Render free instances.  
- Non-bypassable model isolation against a compromised cloud hypervisor.  
- Physical intervention or custom silicon under UDOC custody.  
- That software-only EVA “is already” the full patent governance engine in the hardware sense.

## Alternatives considered

1. **Claim full governance on any cloud VM** — rejected; contradicts systems-security reality and patent invariant.  
2. **Delay all software until hardware is funded** — rejected for Capstone; generational base needs an auditable software track record first (`GENERATIONAL_GOVERNANCE_INTELLIGENCE.md`).  
3. **Treat hardware as optional polish** — rejected; hardware is **foundational** for the *governance engine* claim, optional only for *logic demonstration*.

## Consequences

- Marketing and assessor text must separate **Capstone software proof** from **full-stack governance claim**.  
- Test plans: software smoke now; hardware-in-the-loop / node-in-the-loop later.  
- Client Intelligence and GODS corpus remain software substrates; they do not replace hardware roots of trust.  
- Related: EDR-001 (UDOC deploy layer), EDR-003 (free-tier limits), patent/control maps in `UDOC_V93_DEMO67_PATENT_CONTROLS.md`.

## Related

- `GENERATIONAL_GOVERNANCE_INTELLIGENCE.md`  
- `CLIENT_GOVERNANCE_INTELLIGENCE.md`  
- `CAPSTONE_COVER_NOTE.md`  
- `LIMITATIONS_REGISTER.md`  
- Engineering Canon infrastructure volumes under `docs/`  
