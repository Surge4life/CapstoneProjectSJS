# GODS Platform Web (React 18 + Vite + TS)
Six branded consoles wired to platform-core, in one SPA.

## Run
```bash
npm install
npm run dev      # http://localhost:5173 (proxies /api → http://localhost:8000)
npm run build    # production bundle in dist/  (verified clean)
```
Login: admin@gods.za / admin123 (after running platform-core seed.py).

## Consoles
- **GODS Admin** — cross-system status + closed-loop snapshot
- **UDOC Governance (public)** — live EVA decision path (APPROVE/BLOCK/breach), model registry
- **UDOC Audit (internal)** — hash-chain verification, Merkle root, audit records
- **SETHS** — workforce metrics + cohort enrolment
- **MADIBA** — capital recycling cycles
- **TS Industries** — production SPV portfolio

Branding: navy #060E1C / gold #C9A84C per GODS Brand Manual.
The public vs internal split (D6/D7) is enforced by role on the backend; this SPA surfaces
both for admins. Separate public-only and internal-only builds are produced in packaging (Phase F).
