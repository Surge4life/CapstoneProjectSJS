# UDOC EVA Engine — Complete Build

**Evaluating Valiant Algorithms** · 6-Dimensional Sovereign Risk Scoring
G.O.D.S Holdings (Pty) Ltd (proposed) · v9.3 → v10.0 (computational gaps completed)

## What this is
A single, self-contained, runnable EVA engine that consolidates the v9.3
`@udoc/eva-engine` and **completes the five computations** that were
previously pass-through inputs.

## Run it
```bash
npx tsc --target ES2020 --module commonjs --skipLibCheck --outDir dist eva-engine-complete.ts
node dist/eva-engine-complete.js          # runs the 4-scenario demo
```
Or import `EVAEngine` / `evaluateEVA` into your monorepo.

## The six dimensions (all computed, none assumed)
| Dim | Symbol | Formula |
|-----|--------|---------|
| Validity        | V  | correct / total |
| Confidence      | Cf | raw / (1 + ln(T+1)) |
| Risk            | R  | RiskTierMap[tier] |
| Compliance      | Co | Σ(wᵢ·MFCMᵢ)/Σwᵢ over **47 checks** |
| Stability       | S  | 1 − JSD(current‖baseline) |
| Societal Impact | I  | **H-OS-56** valence/entropy grid |

Aggregate: **SVS = w₁V + w₂Cf + w₃(1−R) + w₄Co + w₅S + w₆I**

## Five completed gaps (vs v9.3)
1. **CMAG ECS** — `ECS = Cooperation × Autonomy × Integrity × Fairness`,
   multi-agent votes aggregated with CONSENSUS / DISPUTE / ESCALATE_IGA arbitration.
2. **H-OS-56 societal impact** — 8 outcome-sectors × 7 severity-bands = 56 cells,
   benefit-weighted valence with entropy penalty and SAHRC harm-flag override.
3. **MFCM 47-check catalogue** — full enumeration: POPIA (1-10), SA NAIFP pillars
   (11-22), EU AI Act (23-32), security/PQC (33-40), lifecycle (41-47).
4. **Fairness (DI, SPD)** — derived from group confusion-matrix outcomes,
   not passed in as raw numbers.
5. **Temperature scaling** — wired into the main pipeline (was defined-but-unused).

## Hardware-equivalent BLOCK overrides
`BLOCK if R≥0.80 | Co<0.70 | DI<0.80 | JSD>0.40 | ECS<0.65 | |SPD|>0.05 | tier=UNACCEPTABLE | CMAG=ESCALATE_IGA`

## Profiles
- `SA_DEFAULT_COEFFICIENTS` (NAIFP-aligned)
- `MILITARY_COEFFICIENTS` (risk-dominant, wRisk=0.40)
- `HEALTHCARE_COEFFICIENTS` (compliance+societal dominant)
- Hot-reload validates Σwᵢ = 1.0 (±0.001)

## Next in the build order
EVA ✅ → **UDOC** (FSM + FPGA + sovereignty + StayChain + core orchestrator
integration) → **G.O.D.S** (four-division platform).

## Hardened layer (v10.0)
Adds tamper-evident sealed verdicts: `evaluateEVASealed()` returns the score plus an
HMAC seal over its canonical score vector; `verifyEVASeal()` confirms it in constant time
and detects any forgery. In production the key is TPM-injected and the seal becomes a
BLAKE3 keyed hash in the Rust/eBPF data plane. Run the file to see a sealed APPROVE and a
detected forgery.

**Superseded, not deleted, by GIS (`/gis`).** Per GBS-SETHS v2.0, the G.O.D.S. Intelligence
System is now the institution-facing AI backbone; EVA's 6-D scoring remains available as one
input a GIS decision can draw on. See `governance-engines/gis/README.md`.
