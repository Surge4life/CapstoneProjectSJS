# Assessor Demo Access
## Single source of truth for Capstone live credentials

**Environment:** Seeded demo / Capstone inspectable stack only  
**Not production secrets** · not institutional accounts · not customer data  
**Authority:** Capstone assessor path · `CAPSTONE_ASSESSOR_PACK.md`  
**Updated:** 2026-08-14  

---

## Purpose

All operator and client demo logins are listed **once** here.

Do **not** treat scattered UI hints as the credential policy.  
After assessment, rotate or disable these accounts if the environment is reused beyond Capstone.

---

## Core API

| Item | Value |
|------|--------|
| Base URL | https://gods-platform-core.onrender.com |
| Health | `GET /health` → `status: ok` |
| Demo ready | `GET /udoc/demo/ready` → `ready: true` |
| EVA batch | `POST /decisions/batch` body `{"scenarios":["fair","biased"]}` → fair ≠ BLOCK, biased = BLOCK |

---

## Staff / operator (GODS local demo)

| Email | Password | Typical surface |
|-------|----------|-----------------|
| `admin@gods.local` | `admin123` | GODS Admin · UDOC Admin · full staff |
| `seths@gods.local` | `staff123` | SETHS · Divisions |
| `ts@gods.local` | `staff123` | TS |
| `madiba@gods.local` | `staff123` | MADIBA · EIF |

**Rule:** Staff chips on static consoles only fill these demo values. They are not real enterprise IAM.

---

## Client package (tenant demo)

| Email | Password | Notes |
|-------|----------|--------|
| `client@udoc.demo` | `client123` | Client Web · Company Knowledge demo seed |

Citizen portal: **no login** — public path `/citizen.html` on Client host.

---

## Surface map (start here)

| Role | URL |
|------|-----|
| Gateway | https://gods-udoc-gateway.onrender.com/ |
| Core GBS | https://gods-platform-core.onrender.com/gbs |
| Sentinel (EVA) | https://gods-platform-core.onrender.com/Sentinel |
| Divisions | https://gods-platform-core.onrender.com/divisions |
| SETHS | https://gods-platform-core.onrender.com/seths |
| TS | https://gods-platform-core.onrender.com/ts |
| MADIBA | https://gods-platform-core.onrender.com/madiba |
| UDOC Admin | https://gods-platform-core.onrender.com/udoc-admin |
| Client | https://gods-udoc-client.onrender.com/ |
| Citizen | https://gods-udoc-client.onrender.com/citizen.html |

---

## Honesty (always visible to assessors)

- Capital **not_deployed**
- MADIBA **≠ AUM**
- Sovereign-Verified **designed_not_built** where stated
- Free-tier Neon / Render bounds apply
- UDOC is the controller · LLM assist is not

---

## Post-assessment

1. Disable or rotate `admin123` / `staff123` / `client123` if the stack remains online.  
2. Do not publish these credentials in marketing or public Netlify copy.  
3. Prefer pointing external readers to this file only: **ASSESSOR_DEMO_ACCESS.md**.

---

*End — replace scattered password hints in docs with a link to this file where practical.*
