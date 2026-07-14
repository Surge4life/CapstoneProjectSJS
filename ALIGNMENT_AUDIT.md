# UDOC Alignment Audit — live system vs v2 whitepapers, EVA v9.1 & the patent blueprint

| Blueprint / patent metric | Live system | Status |
|---|---|---|
| Five-plane architecture (L1 HW → L5 Oversight) | platform-core + station self-test across all 5 | ✅ aligned (HW planes = dependencies) |
| EVA six dimensions: Validity, Confidence, Risk, Compliance, Stability, Impact | engine emits all six on 0–10 (Reliability→**Confidence** renamed) | ✅ aligned |
| Composite Governance Score is **advisory**; BLOCK is strictly dimensional | BLOCK only from dimension thresholds; composite nudges ESCALATE/REVIEW only | ✅ aligned |
| Outcomes APPROVE / REVIEW / ESCALATE / BLOCK | implemented (RESTRICT→ESCALATE) | ✅ aligned |
| Signed cert per **every** decision: SHA-3-256 content hash + policy version + Merkle leaf | EvaCertificate now carries `content_sha3`, `policy_version`, `merkle_leaf`; issued every decision; verifiable | ✅ aligned (PQC sig = Dilithium-ref) |
| Merkle-linked tamper-evident audit | HMAC-chained + Merkle root + verify | ✅ aligned |
| Post-Quantum signatures (CRYSTALS-Kyber/Dilithium) | reference (HMAC stand-in) | ⚙ dependency — install liboqs |
| Append-only WORM (Cassandra, 10-yr) | platform audit chain active | ⚙ dependency — provision Cassandra |
| FIPS 140-3 L3 HSM, split-custody (3 officers) | software key-custody fallback + posture check | ⚙ dependency — install HSM |
| Jurisdiction-locked sovereignty, 6-hourly checks (Pillar III) | sovereignty posture + station config | ✅ aligned |
| HQ-OS quantum-hybrid, graceful degradation | classical-first; QPU auto-activate (forecast) | ✅ aligned (QPU = dependency) |
| Policy-as-Code, hot-reload <5ms, COB-approved/versioned | upload→compile→activate→enforce live | ◐ partial — versioning + COB workflow + <5ms = next increment |
| Fail-closed operation | unknown system → blocked; suspended tenant → 403 | ✅ aligned |
| Human Primacy enforcement (Pillar VIII) | Intelligence guardrail (non-overridable) + HITL/oversight | ✅ aligned |
| Multi-tenancy + isolation | per-tenant scoping on models/decisions/policy/certs | ✅ aligned |
| Six-tier commercial + API keys + quotas + metering | tiers SANDBOX..SOVEREIGN, X-API-Key, quota/suspension | ✅ aligned |
| Four deployment models | station supports edge-appliance; others documented | ◐ partial |
| Bootable station + readiness self-test + test env | `udoc-station/` — verdict READY-WITH-DEPENDENCIES | ✅ delivered |
| SA AI Policy GG54477 "active" (whitepaper, 10 Apr 2026) | **withdrawn 26 Apr 2026** — live system reflects withdrawal | ⚠ whitepaper predates withdrawal; live is current-accurate |

**Queued next:** policy versioning + COB workflow + <5ms hot-reload; production PQC (liboqs) / HSM / Cassandra-WORM integration (hardware-dependent); remaining UDOC v9.3 admin tab pages; full Google-Drive corpus ingest (loader ready — awaiting your zip); offline public Intelligence app alignment.
