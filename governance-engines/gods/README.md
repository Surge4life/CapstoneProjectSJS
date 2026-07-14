# G.O.D.S Platform — Four-Division Integrated Economic Engine

**Good Orderly Directional Systems Holdings (Pty) Ltd (proposed)**
12 Pillars · IP Trust · COB · 250-year mandate

## What this is
Not four disconnected service stubs — the **integrated institution** running a
full compounding cycle. It models the closed capital loop that makes G.O.D.S
self-reinforcing, and proves at runtime that the loop closes and the 12
Constitutional Pillars hold on every action.

## Run it
```bash
npx tsc --target ES2020 --module commonjs --skipLibCheck --types node --outDir dist gods-platform.ts
node dist/gods-platform.js      # 12-month closed-loop simulation
```

## The closed loop
```
        ┌──────────────────────────────────────────────┐
        │                                              │
        ▼                                              │
   ┌─────────┐    workers     ┌──────────┐  profit  ┌──────────┐
   │ S.E.T.H.S│ ────────────▶ │    T.S   │ ───────▶ │          │
   │  human   │               │ Industries│          │ M.A.D.I.B.A│
   │ capital  │               │ production│          │  capital  │
   └─────────┘               └──────────┘          │ recycler │
        ▲                     ┌──────────┐  SaaS   │          │
        │                     │   UDOC   │ ───────▶ │          │
        │   55% recycled      │governance│          └──────────┘
        └─────────────────────────────────────────────┘
```

1. **M.A.D.I.B.A** funds a **S.E.T.H.S** cohort (month 1 from DFI seed)
2. **S.E.T.H.S** trains + places workers (78% completion · 70% placement)
3. **T.S Industries** absorbs placed workers into production SPVs (energy, housing…)
4. **T.S** operating profit + **UDOC** SaaS revenue pool into **M.A.D.I.B.A**
5. **M.A.D.I.B.A** allocates: 20% DFI servicing · 15% reserve · 10% holdings · **55% recycled to S.E.T.H.S**
6. Next cohort is larger → the loop compounds

## Verified 12-month run (R350m DFI seed)
| Metric | Result |
|--------|--------|
| Cumulative workforce reintegrated | **22,470 placed workers** |
| TS monthly profit growth | R1.12m → **R13.49m** (SPVs keep producing) |
| Recycled-to-SETHS growth | R1.04m → **R7.84m** / month |
| Total recycled into human capital | **R53.3m** |
| DFI dependency | **broken by month 4** (loop self-sustains) |
| 12 Pillars clean, every cycle | **YES ✓** |

## Why the loop is closed (not a leaky pipe)
- SETHS output (workers) **is** TS's input — no external labour market dependency
- TS profit + UDOC SaaS pool in MADIBA — **no profit leaks to external extraction**
- MADIBA recycles 55% to SETHS — each cohort larger than the last
- UDOC governs every division's AI internally — **Pillar 8** enforced institution-wide
- Every division action passes the **12-Pillar gate** — **Pillar 7**: even the founder is removable

## Pillar enforcement (architectural, not aspirational)
Each division runs a `pillarGate()` on every action. Examples enforced in code:
- **P5 Governance First** — SETHS intake capped at funded capacity; TS deploys only at ≥50% utilisation
- **P4 Ethical Profitability** — TS margins gated 0 < m < 60% (profitable, not extractive)
- **P2 Contribution First** — MADIBA recycle % must exceed 50%
- **P10 Long-Horizon** — MADIBA reserve ≥ 10%; TS SPVs keep producing across months
- **P8 Human Primacy** — UDOC block rate > 0 (governance actually intervenes)

## Build order — COMPLETE
EVA ✅ → UDOC ✅ → **G.O.D.S ✅**

The EVA engine (`/eva`) is the scoring core. The UDOC orchestrator (`/udoc`)
is the non-bypassable governance pipeline that wraps it. This G.O.D.S platform
(`/gods`) is the institution that the UDOC division sits inside — the closed
economic loop that funds human reintegration and compounds it. GIS (`/gis`)
is the newer, institution-facing AI backbone superseding EVA per GBS-SETHS
v2.0 — it issues decisions via UDOC, drawing on EVA's scoring where relevant,
and is what actually governs S.E.T.H.S. participant journeys, franchise
nodes, and Skills Passports. See `governance-engines/gis/README.md`.
