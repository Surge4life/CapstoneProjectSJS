# UDOC Client Station — bootable bring-up + deployment

A client UDOC station is the in-country, **air-gap-capable** governance appliance that runs the
UDOC core (FastAPI governance engine + EVA + Policy-to-Code + tamper-evident audit) and self-tests
against the five-plane architecture before go-live.

## Quick start (test environment)
```bash
./udoc-station/run_test_env.sh        # boots the core + runs the readiness self-test
```
Produces a signed `readiness_report.json` and a verdict: READY · READY-WITH-DEPENDENCIES · NOT-READY.

## Install on a station (production)
```bash
cd udoc-station
./install.sh                 # or ./install.sh --offline  (uses ./wheels for air-gap)
python3 bringup_selftest.py  # validate; UDOC_API=https://<host> to target a remote core
```
Containerised: `docker compose -f udoc-station/docker-compose.yml up` (builds `Dockerfile.station`).

## Five-plane readiness (what the self-test verifies)
- **L1 Sovereign Security & Hardware** — jurisdiction-locked sovereignty (6-hourly), FIPS 140-3 L3 HSM (split-custody, 3 officers), sovereign-first/air-gap.
- **L2 Immutable Data & Crypto** — SHA-3-256 hashing, PQC (Kyber/Dilithium), WORM Cassandra (10-yr), Merkle audit chain.
- **L3 HQ-OS Quantum-Hybrid** — classical-first with graceful degradation; QPU auto-activation when detected.
- **L4 EVA Engine** — six-dimensional governed decision, SHA-3-256 certified outcome + verification, Policy-as-Code.
- **L5 Constitutional Oversight** — fail-closed on unknown systems, Oversight Board / human-primacy pathway.

## Honesty (pre-registration)
Items reported **DEPENDENCY** are real hardware/产 to install for production: FIPS 140-3 L3 HSM,
a PQC library (liboqs) for production Kyber/Dilithium signing, a Cassandra WORM cluster for 10-yr
retention, and QPUs. In software mode the station uses an HMAC seal (PQC/Dilithium-reference) and
the platform audit chain — clearly labelled, never presented as certified hardware.

## Deployment models (UDOC Technical Whitepaper §2.1)
Edge-appliance (store-and-forward, default here) · Primary+DR · Two-site + signing enclave · Sovereign multi-site.
Set `deployment_model`, `hsm_mode`, `pqc`, `worm_backend`, `jurisdiction`, and `api_base` in `station.config.json`.
