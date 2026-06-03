# Governance Engines (TypeScript, hardened)
The three reference engines, ported from capstone-source, verified running.

- **eva/** — EVA 6-D scoring + tamper-evident sealed verdicts (`evaluateEVASealed`/`verifyEVASeal`)
- **udoc/** — UDOC orchestrator + `HardenedOrchestrator` (signed tokens, state-chain, fail-closed)
- **gods/** — four-division closed-loop economic engine (SETHS→TS→UDOC→MADIBA)

## Run (each prints a verified demo)
```bash
node eva/eva-engine-complete.js
node udoc/udoc-orchestrator.js
node gods/gods-platform.js
```

## Relationship to platform-core
`platform-core/app/services/governance_bridge.py` is the in-process Python implementation of
the same EVA 6-D + sovereignty logic, used on the synchronous sub-50ms decision path. These TS
engines are the canonical reference and the source for the policy-to-silicon HLS path
(TS → Rust `#![no_std]` → eBPF/XDP → FPGA) described in the UDOC Sovereign Data Plane spec.
The Python bridge and these engines agree on thresholds (risk≥0.8 block, DI<0.8, |SPD|>0.05, etc).
