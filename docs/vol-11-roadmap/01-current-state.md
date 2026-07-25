# Chapter 01 — Current State

## Where We Are

As of the initial publication of this Engineering Canon, the G.O.D.S ecosystem is a **fully built, tested, and deployable platform** in its v1 state. It is not a prototype. It is not a concept document. It is real software.

---

## What Is Built

### Core Platform
- ✅ FastAPI backend (`platform-core`) with 30+ routers
- ✅ Complete authentication and RBAC system
- ✅ Governance path (EVA + GBS + UDOC Orchestrator)
- ✅ Decision sealing (HMAC + Dilithium reference)
- ✅ Audit engine with hash chaining
- ✅ Full PostgreSQL schema with all models

### Governance Engines
- ✅ EVA 6-dimensional risk scoring engine
- ✅ GIS (franchise/certification layer)
- ✅ UDOC Orchestrator (SVS → FSM → Enforce)
- ✅ G.O.D.S Intelligence (RAG with constitutional bounds)

### Four Division Applications
- ✅ UDOC Control — PWA (web + Capacitor mobile)
- ✅ SETHS — PWA (web + Capacitor mobile) with document upload/download
- ✅ MADIBA — PWA (web + Capacitor mobile)
- ✅ TS Industries — PWA (web + Capacitor mobile)
- ✅ G.O.D.S Admin Console (`platform-web`) — browser-only

### Edge Layer
- ✅ `udoc-agent` — host-side AI attachment
- ✅ `udoc-gateway` — mTLS protocol bridge
- ✅ `udoc-edge` — autonomous governance node
- ✅ `udoc-sidecar` — event buffer

### Infrastructure
- ✅ Docker Compose development stack
- ✅ Kubernetes manifests
- ✅ Render deployment configuration (`render.yaml`)
- ✅ `hw-bringup` with real boot sequence, selftest, and device interface contracts (emulation-verified)

### Testing
- ✅ Smoke test suite: 31/31 paths verified
- ✅ Service worker generation (all 4 PWAs)
- ✅ End-to-end data path verification (including multipart document upload)

---

## What Is Pending

| Item | Status | Blocker |
|------|--------|---------|
| Entity registration (CIPC) | Pending | Founder action |
| IP Trust establishment | Pending | Entity registration |
| Domain registration | Pending | Entity registration |
| First paying client | Pending | Entity + production deployment |
| UDOC hardware node (physical) | Pending | Hardware procurement |
| Android APK build | Pending | Android Studio environment (cannot run in build sandbox) |
| Third-party security audit | Planned | Pre-first client |
| Regtech certification | Planned | Post-pilot |
| Employment Equity Act compliance certification | Planned | Post-pilot |

---

## The Honest Boundary

The G.O.D.S system is real software. Its hardware boundary is honestly marked:

**Software (built and tested in emulation):**
- All application code
- OS image build
- Bootloader configuration
- Init service ordering
- Device interface contracts
- Self-test logic (proven against emulated FPGA/HSM/NIC via QEMU)

**Pending physical hardware:**
- Final driver register-level implementation against device datasheets
- First-boot on-silicon PASS verification
- Physical HSM/TPM integration (using real PKCS#11 hardware)

This boundary is documented in every relevant README. It is never misrepresented.

---

## Deployment Status

**Current deployment:** Render (cloud, Tier 1)
- URL: `https://gods-platform-core.onrender.com`
- Static apps: Separate Render static services
- Database: Render PostgreSQL
- Status: Operational

**Next deployment target:** Private server / UDOC hardware node (Tier 2/3)
