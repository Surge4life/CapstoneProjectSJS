# UDOC Live Environments · Access Nodes · API Routing

**Purpose:** Clean map of *what exists on free Render + Neon* for Capstone valuation.  
**Date:** 2026-07-30  
**Constraints:** Render ~20 services · Neon ≤500MB · no new registration required for smoke  
**GIS / GBS / GODS Holdings expansion:** deferred until UDOC Task 2 operator-verified green.

---

## 1. What UDOC is in this deployment

UDOC (Unified Digital Oversight & Coordination) is the **governance division** of the G.O.D.S ecosystem. On this Capstone stack it is:

| Layer | Role |
|-------|------|
| **API Core** | Single FastAPI process: auth, registry, decisions/EVA, policy-to-code, oversight, citizen, portals |
| **Client SaaS surfaces** | Tenant-facing consoles (govern, compliance, sector, SaaS portals) |
| **Internal GODS UDOC** | Admin controller (`udoc-internal`) — not a separate fabricated service purpose |
| **Public Citizen** | No-login rights / challenge surface on Client host |
| **Gateway** | Sign-on router into the correct console by role |

Patent / whitepaper depth (v9.3 hardware, StayChain, full MFCM cells) is **architected in demos + docs**; live is **bootloader-grade software** on free infra — same product line, not full hardware product.

---

## 2. Live hosts (existing only)

| Host | Render service | Root dir | Purpose |
|------|----------------|----------|---------|
| `gods-platform-core.onrender.com` | gods-platform-core | `platform-core` | **API +** `/Sentinel` + `/portals` + `/admin` (constitutional) |
| `gods-udoc-client.onrender.com` | gods-udoc-client | `udoc-public` | Client governance + `/citizen.html` |
| `gods-udoc-admin.onrender.com` | gods-udoc-admin | `udoc-internal` | Internal UDOC controller (GODS UDOC Admin) |
| `gods-udoc-portals.onrender.com` | gods-udoc-portals | `udoc-portals` | Client SaaS role/sector portal access |
| `gods-udoc-sector.onrender.com` | gods-udoc-sector | `udoc-sector` | PUBLIC / PRIVATE sector console |
| `gods-udoc-operator.onrender.com` | gods-udoc-operator | `udoc-operator` | Operator workspace |
| `gods-udoc-gateway.onrender.com` | gods-udoc-gateway | `udoc-gateway` | Sovereign sign-on |
| `gods-udoc-web.onrender.com` | gods-udoc-web | `udoc-app` | PWA / mobile OTA shell |

**Do not** invent extra Render services for Citizen or 24-portals — Citizen is Client; 24 dual-path is Core `/portals`.

---

## 3. Access nodes by user class

| User class | Entry | Auth | Primary routes |
|------------|-------|------|----------------|
| **Citizen (public)** | Client `/citizen.html` or Gateway Citizen tile | None | `POST /citizen/challenge` · `GET /citizen/cases/{ref}` · `GET /citizen/health` |
| **Client operator** | Gateway → Client · or direct Client | Bearer JWT | `/decisions` · `/registry/models` · `/policy/*` · `/compliance/sweep` · `/bias/scan` |
| **Sector operator** | Gateway → Sector · or Sector host | Bearer JWT | `/sector/profile` · `/sector/frameworks` · `/decisions` |
| **SaaS portal user** | Gateway → Portals SaaS | Bearer JWT | `/access/profiles` · `/portal/{key}` · `POST /portal/{key}/control` · `/tenants/me` |
| **UDOC Admin (internal)** | Gateway → Admin · `gods-udoc-admin` | Bearer JWT | Full admin views + enhance inject · links to Sentinel / Portals |
| **GODS constitutional** | Core `/admin` | Bearer JWT | Platform constitutional governance |
| **EVA / policy runtime** | Core `/Sentinel` | Bearer JWT | Same Core APIs; Command Centre shell |
| **24-portal dual-path** | Core `/portals` | Bearer JWT | Catalog + control + OversightCase open/resolve |

Default seed operator: existing `admin@gods.local` only (no new users on free Neon).

---

## 4. API routing map (all surfaces → one Core)

```
                    ┌─────────────────────────────┐
   Gateway SSO ────►│  gods-platform-core (API)   │◄── Neon Postgres ≤500MB
                    │  /auth/login                │
   Client ─────────►│  /decisions  /registry/*    │
   Admin ──────────►│  /policy/*   /oversight/*   │
   Sector ─────────►│  /sector/*   /udoc/*        │
   SaaS Portals ───►│  /portal/{key}/control      │
   Sentinel ───────►│  /citizen/* (public)        │
   Citizen ────────►│  /health  /udoc/demo/ready  │
                    └─────────────────────────────┘
```

**Rule:** UI hosts are static. Business logic and state live on Core + Neon. Fail-closed when model/policy seed missing.

---

## 5. MVP tier structure (UDOC-only)

| Tier | Audience | Live surface |
|------|----------|--------------|
| **Core** | Runtime | platform-core APIs + Sentinel + `/portals` |
| **External client** | Paying / pilot tenants | Client · Sector · SaaS Portals |
| **Public** | Affected persons | Citizen |
| **Internal ops** | GODS staff | Admin (udoc-internal) · Operator |
| **Edge** | Mobile | udoc-web / PWA (OTA) |

GODS Intelligence / GIS / GBS frameworks remain **documented + partially coded** under Core engines; commercial GIS file-corpus and full GBS franchise runtime are **post-UDOC-smoke / post-seed**.

---

## 6. Valuation / assessor path

1. `UDOC_SMOKE_PASS.md` — A + B + (C or C2) + biased **BLOCK**  
2. `P6_ASSESSOR_SIDE_BY_SIDE.md` — surfaces 1–5 live  
3. This file — environment honesty  
4. Netlify demos — UI acceptance SoT (`UDOC_DEMO_INVENTORY.md` + demos 6/7 note)

**Task 2 close** = operator green on live matrix.  
**Task 1** = Engineering Canon volume commits after Task 2.  
**GIS/GBS build** = after UDOC post-production smoke.
