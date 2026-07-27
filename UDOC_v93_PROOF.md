# UDOC v9.3 — Proof of Delivery (Capstone / Open-Source)

**Status:** Complete for grading and open-source release track  
**Entity posture:** G.O.D.S Holdings (Pty) Ltd — **pre-registration**  
**Regulatory honesty:** GG54477 withdrawn 26 Apr 2026 · standing basis = POPIA s71 + Constitution ss 9 / 14 / 33 · National AI Policy Framework (Aug 2024) remains the standing instrument  
**Date:** 2026-07-28

---

## What this proves

UDOC is a **live, multi-surface sovereign AI governance platform** — not a slide deck.

| Layer | Reality |
|-------|---------|
| Backend | FastAPI `platform-core` on Render · Neon Postgres · fail-closed GIS 12-pillar · EVA 6-dim + certificates · Policy-to-Code / COB · StayChain audit · multi-tenant SaaS |
| Client console | `udoc-public` — Govern loop (register / evaluate / cert-verify) + 6-dim EVA + KPIs |
| Admin mainframe | `udoc-internal` — Control / kill-switch / Lifecycle / Evidence-Replay / full EVA / tenancy |
| Mobile | `udoc-mobile/www` — Capacitor-ready parity (6-dim, verify, register) |
| Sector console | `udoc-sector` — genuine PUBLIC vs PRIVATE differentiation (frameworks, terminology, oversight model, KPIs) |
| Operator | `udoc-operator` — 24 Sovereign-Operator profiles · capability-scoped actions |
| Gateway | `udoc-gateway` — single sign-on routing by role |
| Deploy | `render.yaml` autoDeploy:true on `main` for all static UIs + core |

---

## Surface map (live services)

| Service name (Render) | Root | Role |
|-----------------------|------|------|
| `gods-platform-core` | `platform-core` | API + EVA + sector + registry + audit |
| `gods-udoc-client` | `udoc-public` | Tenant client governance |
| `gods-udoc-admin` | `udoc-internal` | Staff / admin mainframe |
| `gods-udoc-sector` | `udoc-sector` | Public / Private sector experience |
| `gods-udoc-operator` | `udoc-operator` | Per-profile operator workspace |
| `gods-udoc-gateway` | `udoc-gateway` | Unified sign-on |
| `gods-udoc-web` | `udoc-app` | React/Vite PWA (OTA target) |

Mobile: Capacitor project under `udoc-mobile` (www already parity-enhanced).

---

## Session delivery log (v9.3 density upgrade)

| Session | Focus | Commit(s) |
|---------|-------|-----------|
| 1 | Client Govern loop + 6-dim + KPIs | `98253ff` |
| 2 | Admin denser (Control, Lifecycle, Evidence/Replay, EVA, honesty) | `78dd789` |
| 3 | Mobile parity | `b969687` |
| 4 | Sector console + render service | `f4709c4`, `5369ee8` |
| 5 | Polish + open-source proof (this file) | *this commit* |

---

## Open-source readiness

1. **Honesty first** — every major console carries the pre-registration / GG54477 / POPIA s71 footer. Do not remove.
2. **No claims of commercial scale** beyond what is live. Full division UI depth and multi-tenant commercial packaging remain post-seed.
3. **License** — recommend dual-track: source available for academic / regulator review under a clear non-commercial clause until entity registration and IP assignment are complete. Final SPDX choice is a founder decision.
4. **Secrets** — `GODS_SOV_KEY` and production `DATABASE_URL` must never appear in the public tree. Blueprint already isolates them.
5. **Demo accounts** — rotate any bootstrap credentials before public fork.
6. **Docs** — Engineering Canon volumes under `docs/` (Replit handover) + this proof file form the public narrative spine.

---

## What is intentionally *not* claimed

- Registered company status  
- Live GG54477 / formal AI policy registration  
- Production-grade multi-region HA / paid commercial SLAs  
- Full GIS/GBS/SETHS/TS/MADIBA commercial UI depth (engines exist; division product surfaces are post-UDOC-proof)

---

## Next after open-source / grading

GBS + GIS deterministic engines are already present in `platform-core`. Credibility path after this proof: data-room / GBS alignment and live-site honesty paste (see `LIVE_SITE_CORRECTION_PACK.md`).

**UDOC v9.3 density upgrade is complete.**
