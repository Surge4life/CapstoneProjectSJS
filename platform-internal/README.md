# G.O.D.S Platform Internal — Staff Work Environment (network-locked)
The INTERNAL face of the ecosystem: a browser console where staff *operate* each division.
Network-locked — served only inside the governance network, talks to platform-core's internal bind.

## Consoles (full staff work environments)
- **Holdings Overview** — cross-division status + closed-loop snapshot
- **SETHS Ops** — cohort enrolment + programme management
- **MADIBA Ops** — capital allocation cycles + investor pipeline staff review/advance
- **TS Industries Ops** — project submission screening + SPV deployment
- **UDOC Governance** — run decisions, manage oversight cases (Pillar VIII), audit chain, sovereignty posture
  (this console is INTERNAL-ONLY and never exposed at the external edge)

## Run
```bash
npm install && npm run dev      # dev: proxies /api → localhost:8000
npm run build                   # production bundle (verified clean)
```
Login: staff credentials (admin@gods.za / admin123 in dev).

## Network-locked deployment (per topology)
In production this console + platform-core bind to the INTERNAL interface only:
```bash
uvicorn app.main:app --host 10.0.0.10 --port 8000     # internal NIC, no public route
```
External apps never reach this; they go through the UDOC gateway edge (infra/edge/nginx.conf),
which allow-lists only external-safe paths. See 00_NETWORK_TOPOLOGY.md.

## Internal vs external (the model)
| | Internal (this) | External (apps) |
|---|---|---|
| SETHS | SethsOps console | seths-app (.apk) |
| MADIBA | MadibaOps console | madiba-app (.apk) |
| TS | TSOps console | ts-app (.apk) |
| UDOC | UDOCGov console (internal-only) | udoc-app (.apk, client control) |
| G.O.D.S | this + platform-web | password-gated web |
