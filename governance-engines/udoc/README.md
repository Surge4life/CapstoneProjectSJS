# UDOC Orchestration Pipeline — Complete Build

**Unified Digital Oversight & Coordination** · Core Orchestration Engine (AEEF)
G.O.D.S Holdings (Pty) Ltd (proposed) · v9.3 → v10.0

## What this is
The non-bypassable governance flow (Claim 1) that ties the five UDOC
subsystems into **one auditable pipeline**. Every AI model request runs
this exact sequence — there is no path around it.

```
EVA (6D score) → Sovereignty (SVS=min) → FSM (14-stage) →
FPGA (opcode enforcement) → StayChain (immutable BFT audit)
```

## Run it
```bash
npx tsc --target ES2020 --module commonjs --skipLibCheck --types node --outDir dist udoc-orchestrator.ts
node dist/udoc-orchestrator.js     # runs 6 governance scenarios + StayChain audit
```

## The pipeline (UDOCOrchestrator.process)
1. **S0 INIT** — `G_ATTEST` bitstream verification
2. **S1 VERIFY** — model registry lookup + `G_SOV_VERIFY` sovereignty check
3. **S2 EVALUATE** — EVA 6-D decision is the heart of the flow
4. Branch on EVA decision:
   - **BLOCK** → S11 FAIL_CLOSED + `G_LOCK` (HSM-NVRAM persist), model status → BLOCKED
   - **REVIEW/ESCALATE** → S7 ESCALATE + `G_ESCALATE` (IGA bundle)
   - **RESTRICT** → S3 → S6 RESTRICT (`G_RESTRICT`) → S4 EXECUTE
   - **APPROVE** → S3 AUTHORISE → S4 EXECUTE
5. **S5 MONITOR** → **S10 AUDIT_FINALISE** (`G_AUDIT`) → **S0** (`G_SYNC`)
6. Every request commits a **StayChain block** (BFT: 3/3 ZA witnesses GP·WC·KZN)

## Sovereignty override
If `SVS = min(BGP, traceroute, DNSSEC, storage) < 1.0` with a CRITICAL
violation, the pipeline forces **G_HALT** (relay OPEN) and fail-closes —
*regardless of a clean EVA score*. Sovereignty is non-negotiable.

## Verified behaviour (demo scenarios)
| Scenario | EVA | SVS | Final state | Decision | Hardware |
|----------|-----|-----|-------------|----------|----------|
| Healthy model | APPROVE | 1.0 | S0 (cycle complete) | APPROVE | relay closed |
| Biased model | BLOCK | 1.0 | S11 FAIL_CLOSED | BLOCK | G_LOCK |
| Sovereignty breach | APPROVE | 0.4 | S11 FAIL_CLOSED | BLOCK | relay OPEN (G_HALT) |
| Elevated risk | REVIEW | 1.0 | S7 ESCALATE | ESCALATE | G_ESCALATE |
| Medium risk | RESTRICT | 1.0 | S0 (restricted cycle) | RESTRICT | G_RESTRICT |
| BFT 2/3 witnesses | APPROVE | 1.0 | S0 | APPROVE | chain not advanced |

StayChain integrity verified VALID across all committed blocks.

## Subsystems (mirror the v9.3 @udoc packages)
- `SovereigntyVerificationSystem` — SVS = min(); CONTINUE/MONITOR/ISOLATE/HALT
- `FPGAEnforcementLayer` — 9 opcodes (G_HALT…G_SYNC), relay + G_LOCK NVRAM state
- `GovernanceFSM` — 14-stage deterministic transition table, fail-closed, G_LOCK guard
- `StayChain` — SHA-3-256 Merkle, Dilithium + SPHINCS+ sigs, 3/3 BFT quorum
- `ModelRegistry` — model lifecycle + status
- `UDOCOrchestrator.process()` — the non-bypassable flow

## Build order
EVA ✅ → UDOC ✅ → **G.O.D.S** (four-division platform — next).

## Hardened sovereign layer (v10.0)
Adds `CryptoEnclave` (HMAC-signed governance tokens, constant-time state verification) and
`HardenedOrchestrator` (cryptographic state-hash chaining, request freezing, fail-closed on
tamper). The demo issues a signed APPROVE token and shows a tamper attempt failing closed.
Production path: re-implemented in Rust (#![no_std]) → eBPF/XDP kernel enforcement → FPGA
fail-closed interrupts, per the UDOC Sovereign Data Plane spec. State rule:
Σ(n+1) = H(Σ(n) ‖ F_EVA(x) ‖ K_SOV).

GIS (`/gis`) issues its decisions *via* this orchestrator, not around it — GIS is a new
decision-origin layer, not a second audit/orchestration path. See
`governance-engines/gis/README.md`.
