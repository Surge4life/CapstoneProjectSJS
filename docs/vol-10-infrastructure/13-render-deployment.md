# Chapter 13 — Render Deployment (Current Capstone Production)

## Current production environment (honest)

The Capstone UDOC stack runs on **Render free** web services + **external Neon Postgres (≤500MB)**.  
Render’s free Postgres was expired; `DATABASE_URL` points at Neon (manual env, not `fromDatabase` in blueprint).

Source of truth for service list: repository root `render.yaml`.  
Human map for assessors: `udoc-mvp/UDOC_LIVE_ENVIRONMENTS.md`.

This is **Tier 1 (cloud pilot)** in the Volume X tier model — not Tier 3 sovereign hardware.

---

## Active services (UDOC-relevant)

| Service | Runtime | Root | Role |
|---------|---------|------|------|
| `gods-platform-core` | Python / uvicorn | `platform-core` | API + static `/Sentinel` · `/portals` · `/admin` |
| `gods-udoc-client` | static | `udoc-public` | Client console + **Citizen** |
| `gods-udoc-admin` | static | `udoc-internal` | Internal UDOC controller |
| `gods-udoc-portals` | static | `udoc-portals` | Client SaaS role/sector portals |
| `gods-udoc-sector` | static | `udoc-sector` | PUBLIC/PRIVATE sector console |
| `gods-udoc-operator` | static | `udoc-operator` | Operator workspace |
| `gods-udoc-gateway` | static | `udoc-gateway` | Sign-on router |
| `gods-udoc-web` | static build | `udoc-app` | PWA / mobile OTA |

Also in blueprint (broader GODS): `gods-platform-internal`, `gods-portals` (division portals-web).

**Quota rule:** Do not add services for Citizen or 24-portals — fold into Client and Core.

---

## Environment variables (Core)

| Variable | Notes |
|----------|-------|
| `DATABASE_URL` | **Neon** connection string (manual; free Render SQL expired) |
| `ENVIRONMENT` | `production` |
| `GODS_SOV_KEY` | Generated / preserved on Render |

Kafka, Cassandra, OpenSearch, object storage, and hardware HSM are **Canon target architecture** (other chapters). They are **not** required for Capstone UDOC smoke on free tier.

---

## Limitations (free tier) and mitigations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Neon ≤500MB | No bulk corpus / no mass user signup | Seed `model-001` · text-only knowledge · no new assessor users |
| Render cold starts | First request latency | Smoke after warm · health check path `/health` |
| ~20 service cap | Cannot spawn per-portal services | Core `/portals` data-driven dual-path |
| No paid always-on | Spiky latency | Acceptable for Capstone valuation |

---

## Deploy process

- `autoDeploy: true` on `main` for listed services.
- Post-deploy verify:
  1. `GET https://gods-platform-core.onrender.com/health`
  2. `GET /udoc/demo/ready` (auth as needed) → seed status
  3. Sentinel or Client smoke → fair ≠ BLOCK · biased = **BLOCK**

Checklist: `UDOC_SMOKE_PASS.md` · matrix: `udoc-mvp/P6_ASSESSOR_SIDE_BY_SIDE.md`.

---

## Relationship to patent / hardware

Software governance loop (evaluate → policy → block → certify → human path) is **deployable without full UDOC hardware**.  
Tier 3 air-gap / HSM / WORM (Chapters 07, 12) is the **product upgrade path** after seed — documented, not claimed live on free Render.
