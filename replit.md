# G.O.D.S Ecosystem Engineering Canon

## Project Overview

This is the **G.O.D.S Ecosystem** — a sovereign governance platform for artificial intelligence and industrial participation. The acronym stands for **Governance, Operations, Decisioning, and Sovereignty**.

The repository is a monorepo containing:
- `platform-core/` — FastAPI backend (Python 3.12, all governance APIs)
- `governance-engines/` — EVA scoring engine, UDOC orchestrator, GIS engine, G.O.D.S intelligence
- `*-app/` — Four React/Vite PWAs (UDOC Control, SETHS, MADIBA, TS Industries)
- `*-mobile/` — Capacitor wrappers for Android/iOS
- `platform-web/` — G.O.D.S Admin Console (browser-only)
- `udoc-agent/`, `udoc-gateway/`, `udoc-edge/`, `udoc-sidecar/` — AI governance attachment components
- `infra/` — Docker Compose, Kubernetes, Terraform
- `hw-bringup/` — Hardware initialisation (boot, selftest, init)
- `docs/` — **G.O.D.S Ecosystem Engineering Canon** (11 volumes)

## Engineering Canon

The primary documentation artifact is `docs/ENGINEERING_CANON.md` — the canonical engineering reference for the entire ecosystem across 11 volumes:

- **Vol I:** Ecosystem Canon (vision, philosophy, constitutional pillars)
- **Vol II:** System Architecture (every service and engine)
- **Vol III:** Repository Blueprint (every folder explained)
- **Vol IV:** G.O.D.S Intelligence White Paper (institutional intelligence)
- **Vol V:** GBS Constitutional Runtime (every rule and decision tree)
- **Vol VI:** Developer Implementation Guide (every commit, in order)
- **Vol VII:** Database Design (every table, relationship, audit chain)
- **Vol VIII:** API Reference (every endpoint)
- **Vol IX:** UI/UX Design System (every portal and workflow)
- **Vol X:** Infrastructure White Paper (production deployment)
- **Vol XI:** Roadmap (current → 250-year governance)

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy, Pydantic v2 |
| Frontend | React 18, Vite 5, TypeScript, vite-plugin-pwa |
| Mobile | Capacitor 5 |
| Database | PostgreSQL 15 |
| Event streaming | Apache Kafka |
| Audit storage | Cassandra / WORM |
| Search | OpenSearch |
| Cache | Redis |
| Infrastructure | Docker, Kubernetes, Render (current cloud) |

## Running

```bash
# Start infrastructure services
cd infra && docker compose up -d

# Start backend
cd platform-core
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure environment variables
uvicorn app.main:app --reload --port 8000

# Start a frontend app
cd seths-app && npm install && npm run dev
```

See `docs/vol-6-developer-implementation-guide/01-environment-setup.md` for the full setup guide.

## Entity Status

G.O.D.S Holdings (Pty) Ltd is a **proposed entity — not yet registered**. All IP vests in Sashin J. Singh pending CIPC registration and IP Trust establishment. All marks carry ™ notice only.

## User Preferences

- All architectural decisions must align with the Engineering Canon in `docs/`
- The constitutional pillars (Vol I, Ch 03) are non-negotiable constraints
- Every new service, router, or endpoint must be documented in the appropriate Canon volume
- The audit chain is sacred — never compromise audit integrity for performance
