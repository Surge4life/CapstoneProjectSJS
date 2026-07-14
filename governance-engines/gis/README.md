# G.O.D.S. Intelligence System (GIS) — Reference Implementation

**Supersedes EVA** as the institutional AI backbone, per GBS-SETHS v2.0 and the GBS-SETHS Institutional
Readiness Package (Document 00 Part I §3; Document 06, GIS Architecture Specification). This is the
**canonical TypeScript reference** — the same pattern already established by `governance-engines/eva/` and
`governance-engines/udoc/`. The **live, deployed** implementation platform-core actually runs on Render is
`platform-core/app/services/gis_engine.py` (+ `cetcte_engine.py`, `gbs_engine.py`), which mirrors this
package's logic in-process, the same way `governance_bridge.py` already mirrors EVA/UDOC.

## What GIS does (Document 00 §3.1 — seven functions)
Digital Governor · Career Navigator · Digital Mentor · Compliance Verifier · Research & Intelligence
Engine · Outcome Auditor · Franchise Intelligence.

## Fail-closed, constitutionally (Pillar VIII — Human Primacy in AI)
In the absence of verified sovereign authorisation, GIS defaults to **BLOCK**. This package's
`gis.service.ts` implements the twelve-pillar check that decides APPROVE vs. BLOCK; `applyGovernanceGate()`
is an honestly-labelled dev-mode placeholder (`return true; // Auto-pass for development`) — the live,
actually-fail-closed behaviour is in the Python engine, not here. Do not treat this package's stub as
evidence of runtime governance behaviour.

## Relationship to EVA and UDOC
GIS does not replace UDOC's orchestration or audit role — GIS issues decisions **via** UDOC's sealed audit
infrastructure (this package's `udoc.service.ts` / the Python engine's `audit_writer.append_audit`). EVA's
6-D scoring engine remains available as one input a GIS decision can draw on; GIS is the newer, broader,
institution-facing layer sitting above it, not a deletion of it.

## Status when received into this repo (13 July 2026)
Uploaded as `gods-intelligence-system.zip`, standalone, not yet integrated. Two structural bugs were found
and fixed during integration:
1. `index.ts` imported `franchise.routes.ts` and `certification.routes.ts`, neither of which existed in
   the upload — the service would not have started. Both written to match the existing
   `participant.controller.ts`/`.routes.ts` pattern, backed by the `Certification` and
   `ComplianceViolation` Prisma models already defined in `schema.prisma`.
2. `src/config/constants.ts` had an unescaped apostrophe in a single-quoted string
   (`'...GBS-SETHS's obligation...'`), which broke the TypeScript compiler entirely. Found by running
   `npx tsc --noEmit` against the package's own strict `tsconfig.json`, not by inspection.

All `noUnusedLocals` / `noUnusedParameters` / `noImplicitAny` strictness violations already present in the
upload were also fixed — most mechanically, one (`cetcte.service.ts`'s unused `gisService` field) via a
genuine integration: stage advancement is now itself gated through a GIS governance decision, which is
what the field's presence already implied was intended.

`npx tsc --noEmit` exits 0 as of this integration. `npx prisma generate` requires network access this
sandbox does not have (binaries.prisma.sh is not in the allowed egress list) — run it in your own
environment or let Render's build step handle it; nothing in the schema itself is unverified by that gap.

## Running it standalone (for local development against this package directly)
```bash
cd governance-engines/gis
npm install
npx prisma generate
npx prisma migrate dev
npm run dev
```

## Build order
EVA ✅ → UDOC ✅ → G.O.D.S (economic closed-loop simulation) ✅ → **GIS ✅ (supersedes EVA, live in
platform-core)**
