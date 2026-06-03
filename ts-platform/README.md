# TS Platform (standalone, React + Vite + recharts)
Dedicated division platform for **TS — Production SPVs**, wired to platform-core's
division API **and** the UDOC data-record-and-analytics layer (`/analytics/TS/*`).

## Run
```bash
npm install
npm run dev      # http://localhost:5173 (proxies /api → platform-core :8000)
npm run build    # production bundle in dist/ (verified clean)
```
Login: admin@gods.za / admin123 (after platform-core seed.py).

## What it shows (all live from UDOC analytics)
- Division KPIs (computed by UDOC analytics_engine from recorded events)
- Time-series / portfolio charts (recharts)
- The UDOC event-record feed — every division action is recorded by UDOC for audit & analytics

Branding: GODS navy/gold with a division accent. Data recorded & governed by UDOC.
