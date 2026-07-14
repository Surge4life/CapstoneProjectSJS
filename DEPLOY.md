> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# G.O.D.S ECOSYSTEM — DEPLOYMENT GUIDE

## What this is
The full **software** stack for the G.O.D.S ecosystem: a sovereign AI-governance backend,
six branded React consoles, the three governance engines, the four UDOC attachment packages,
and the **boot-to-live hardware bring-up stack** that validates the UDOC node on first power-on.

Built for real and **verified in emulation**. The only step that needs the physical hardware
is the first-boot on-silicon PASS — which the included `udoc-selftest` produces automatically.

## 1. Run the platform locally (one command path)
```bash
# Backend
cd platform-core && pip install -r requirements.txt && python seed.py
uvicorn app.main:app --port 8000          # http://localhost:8000/docs  (35 routes)

# Frontend (new shell)
cd platform-web && npm install && npm run dev    # http://localhost:5173
# login: admin@gods.local / admin123
```
Or everything containerised:
```bash
cd infra && docker compose up --build           # core :8000 + web :5173
cd infra && docker compose --profile prod up     # + postgres/redis/redpanda/opensearch
```

## 2. Verify (all pass)
```bash
cd platform-core && python -m pytest -q          # 8/8 governance/audit/division tests
cd platform-web && npm run build                 # clean production bundle
node governance-engines/eva/eva-engine-complete.js     # sealed verdict + forgery detect
node governance-engines/udoc/udoc-orchestrator.js      # signed token + fail-closed
python3 hw-bringup/emulate/boot_sequence.py            # healthy → NODE LIVE
python3 hw-bringup/emulate/boot_sequence.py --fail fpga # fault → HELD FAIL-CLOSED
```

## 3. Flash to the UDOC hardware node (boot-to-live)
The boot sequence (see `hw-bringup/`): UEFI/GRUB → kernel+initramfs (signed, TPM-measured) →
systemd → **udoc-selftest** (probes FPGA-over-PCIe, HSM/TPM, NIC; PASS→gate open / critical
fault→fail-closed) → platform-core starts only if the gate is open → `live-status.target` →
console banner "UDOC SOVEREIGN NODE: LIVE".

Procedure (executed by the secure build/signing enclave — see `hw-bringup/boot/OS_IMAGE.md`):
1. Build the minimal immutable rootfs; overlay `/opt/udoc/` = this repo.
2. Install systemd units from `hw-bringup/init/`; set default target `live-status.target`.
3. On real hardware, drop `--emulate` from `udoc-selftest.service` so probes hit real devices.
4. Sign the image + produce the import manifest; flash to boot media.
5. Power on. The node self-validates and reports PASS/FAIL on its own console + `/run/udoc/selftest.json`.

## 4. Governance attachments (embed UDOC into any AI system)
- `udoc-agent/` — host process (VMs/bare metal)
- `udoc-sidecar/` — container alongside an inference service (buffers + replays)
- `udoc-gateway/` — mTLS bridge + lineage + signed air-gap relay export
- `udoc-edge/` — autonomous edge node with offline local governance + sync-on-connect
All fail-CLOSED for critical tiers, verified against the live backend.

## HONEST BOUNDARY (read this)
- **Real & tested in emulation:** all application code, the OS-image build recipe, bootloader
  config, systemd ordering, device-interface drivers, the boot self-test, services, frontends,
  the inter-service handshakes, the four attachments.
- **Requires the physical board to finalise:** register-level driver specifics against each
  device's datasheet, and the first-power-on on-silicon PASS. Nothing here is represented as
  already-validated on silicon — the self-test is precisely what produces that result.
- **Dev vs prod datastores:** SQLite + in-memory bus/audit in dev; PostgreSQL 16 + Kafka/Redpanda
  + Cassandra/WORM in prod, same interfaces, swapped by config. HSM/Dilithium emulated in dev,
  finalised against the real HSM in production.
