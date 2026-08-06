# Divisions pre-seed density note

**2026-08-06**

## Live recovery

`/divisions` temporarily uses an **emergency loader** that injects the last densified UI from commit `ed1171f9` (cross-links + SETHS/TS/MADIBA/UDOC density).

## Pre-seed densify (built, pending permanent embed)

Full pre-seed HTML (guided path chips, overview KPIs, honest empty states, enrol→place→SPV→assign→allocate) is ready in project artifacts:

- `artifacts/divisions_PRESEED_DENSITY.html` (~34KB)

### Guided path (when permanently embedded)

1. Enrol SETHS  
2. Advance to PLACED (×2)  
3. Deploy SPV  
4. Assign worker  
5. MADIBA allocate (demo ledger ≠ AUM)

### Honesty

Zeros OK · MADIBA ledger ≠ AUM · capital not_deployed · Sovereign-Verified designed_not_built

### Operator action

If you can `git push` from a local machine, replace `platform-core/static/divisions.html` with `artifacts/divisions_PRESEED_DENSITY.html` and remove the emergency loader.

Meanwhile the loader keeps the demo usable for pre-seed conversations.
