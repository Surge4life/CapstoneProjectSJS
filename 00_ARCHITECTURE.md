> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# GODS ECOSYSTEM — ARCHITECTURE
Maps the UDOC hardware spec (5 planes) → software services → the boot-to-live flow.
Everything here is built as real software; the hardware boundary is marked explicitly.

## 1. The five hardware planes → software mapping

| Plane (from HW spec) | Hardware emphasis | Software in this ecosystem |
|---|---|---|
| **1. Embedded governance fabric** | low-latency compute, fail-closed | `udoc-agent`, `udoc-sidecar`, `udoc-gateway`, `udoc-edge` + SDK |
| **2. Ingestion & control** | fast NVMe, 25/100GbE, mTLS | `platform-core` ingress routers, auth, mTLS contract |
| **3. Governance & processing** | balanced CPU/RAM | `platform-core` FastAPI services + `governance-engines` (EVA/UDOC) |
| **4. Immutable data operations core** | storage endurance, replication | PostgreSQL (state) + Kafka (events) + Cassandra/WORM (audit) + OpenSearch (search) + object archive |
| **5. Security & operations** | trust isolation, mgmt | HSM/TPM client (PKCS#11), key hierarchy, bastion, SIEM hooks, `hw-bringup` self-test |

## 2. Service catalogue (platform-core)

```
platform-core/app/
  core/          config · security(JWT,bcrypt) · dependencies · mtls
  db/            session · models (registry, decisions, audit_ref, workforce, capital, projects, oversight)
  routers/       auth admin health
                 seths workforce          ← SETHS division
                 madiba                    ← MADIBA division (capital)
                 ts                        ← TS Industries division
                 registry decisions        ← UDOC model registry + decisioning
                 compliance bias           ← UDOC compliance + fairness
                 oversight sovereignty     ← UDOC internal oversight
                 audit lineage             ← immutable audit + provenance
                 intelligence              ← cross-division analytics
  services/      governance_bridge · event_bus · audit_writer · key_service · selftest_client
  schemas/       pydantic models per router
```

## 3. The governance path (non-bypassable, sub-50 ms target)

```
AI request ─▶ attachment (agent/sidecar/gateway/edge)
           ─▶ platform-core /decisions  ─▶ governance-engines: EVA 6-D score
                                         ─▶ UDOC orchestrator: sovereignty(SVS)→FSM→enforce
           ─▶ decision {APPROVE|REVIEW|ESCALATE|BLOCK} (+ HMAC/Dilithium-ref seal)
           ─▶ event_bus(Kafka) ─▶ audit_writer ─▶ Cassandra/WORM hash-chain + Merkle root
           ─▶ response to caller; fail-CLOSED if engine/HSM unreachable for critical class
```

## 4. Boot-to-live flow (hw-bringup) — what runs when the new hardware is switched on

```
power-on
 └─ bootloader (UEFI/U-Boot per node class)        [hw-bringup/boot]
     └─ init (systemd)                              [hw-bringup/init]
         ├─ udoc-selftest.service  ★ HARDWARE VALIDATION, ordered FIRST
         │    ├─ probe FPGA over PCIe   → enforcement engine present? bitstream id?   PASS/FAIL
         │    ├─ probe HSM/TPM (PKCS#11)→ key hierarchy reachable? master key sealed?  PASS/FAIL
         │    ├─ probe NIC              → sovereignty inspection hook attachable?      PASS/FAIL
         │    ├─ probe data core        → postgres/kafka/cassandra/opensearch reachable? PASS/FAIL
         │    └─ emit report → /run/udoc/selftest.json ; gate downstream units
         ├─ (if PASS) platform-core.service   → FastAPI up, mTLS, health green
         ├─ (if PASS) udoc-public / udoc-internal services
         └─ live-status.target reached ; LED/console/registry → "UDOC NODE LIVE"
         └─ (if any critical FAIL) → fail-closed: services held, alarm, report retained
```

- Self-test logic is **real code**; device probes are written against the spec's interfaces
  and are **emulation-mocked** (QEMU + fake PCIe/PKCS#11/NIC shims) so the boot sequence is
  proven to run and report correctly. On the physical board the same probes hit real devices
  and return the real PASS/FAIL — that first-boot result is the on-silicon validation.

## 5. Branding
Navy `#060E1C` + gold `#C9A84C`, `G.O.D.S LOGO.jpeg`, per `GODS_Brand_Manual`. Applied across
all React platforms and the console/boot banner.

## 6. Honest boundary
Real: all application software, OS image build, bootloader config, init ordering, device-interface
**contracts**, self-test logic, services, frontends — tested in emulation. Pending real hardware:
the actual driver register-level finalisation against device datasheets, and the first-boot
on-silicon PASS. Marked in every README; never represented as already-validated-on-hardware.
