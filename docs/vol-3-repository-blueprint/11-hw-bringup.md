# Chapter 11 — hw-bringup

## What Is hw-bringup?

`hw-bringup/` contains the hardware initialisation system for the UDOC hardware node. This is real code — not documentation, not mockups. It implements the boot sequence, hardware validation, device drivers, and init service ordering for the UDOC physical hardware platform.

The code is verified against emulated hardware (QEMU with fake PCIe/PKCS#11/NIC shims). On physical hardware, the same code runs against real devices.

---

## Directory Structure

```
hw-bringup/
├── boot/                   Bootloader configuration
│   ├── grub/               GRUB2 configuration
│   │   ├── grub.cfg        Boot menu entries
│   │   └── grub.d/         Drop-in configurations
│   └── uefi/               UEFI configuration (for UEFI targets)
│
├── drivers/                Device interface contracts + emulation
│   ├── fpga_pcie/          FPGA enforcement engine (PCIe interface)
│   │   ├── probe.py        Probe FPGA over PCIe — PASS/FAIL
│   │   ├── contract.py     Device interface contract
│   │   └── emulated/       QEMU FPGA shim for emulation
│   ├── hsm_pkcs11/         HSM/TPM PKCS#11 interface
│   │   ├── probe.py        Probe HSM/TPM — PASS/FAIL
│   │   ├── client.py       PKCS#11 client for key operations
│   │   └── emulated/       SoftHSM2 for development and emulation
│   └── nic_sovereignty/    NIC sovereignty inspection hook
│       ├── probe.py        Probe NIC sovereignty capability — PASS/FAIL
│       └── emulated/       Software emulation of sovereignty hook
│
├── init/                   Systemd service definitions
│   ├── udoc-selftest.service    ★ First service — hardware validation
│   ├── udoc-platform.service    platform-core service unit
│   ├── udoc-governance.service  Governance engines service unit
│   └── udoc-live.target         Reached when all systems are live
│
├── selftest/               Self-test orchestration
│   ├── run_selftest.py     Runs all hardware probes in sequence
│   ├── report.py           Generates selftest.json report
│   └── emulate/            Emulation environment setup
│       ├── run_emulated.sh  Start full emulated boot sequence
│       └── qemu_config.sh   QEMU configuration for emulation
│
└── README.md
```

---

## The Boot Sequence

The UDOC hardware node boots in this exact sequence:

```
1. UEFI/GRUB → kernel + initrd loaded
2. systemd init started
3. udoc-selftest.service (FIRST — ordered before everything)
   ├── Probe FPGA over PCIe:
   │   ├── PASS → enforcement engine present, bitstream ID logged
   │   └── FAIL → selftest.json: CRITICAL_FAIL, downstream units held
   ├── Probe HSM/TPM (PKCS#11):
   │   ├── PASS → key hierarchy reachable, master key sealed
   │   └── FAIL → CRITICAL_FAIL
   ├── Probe NIC (sovereignty hook):
   │   ├── PASS → sovereignty inspection attachable
   │   └── FAIL → CRITICAL_FAIL
   └── Probe data core (PostgreSQL/Kafka/Cassandra/OpenSearch):
       ├── PASS → all databases reachable
       └── FAIL → CRITICAL_FAIL
4. selftest.json written to /run/udoc/selftest.json
5. If ALL PASS:
   ├── udoc-platform.service starts (platform-core)
   ├── udoc-governance.service starts (governance engines)
   └── udoc-live.target reached → LED/console: "UDOC NODE LIVE"
6. If ANY CRITICAL_FAIL:
   └── Fail-closed: services held, alarm triggered, selftest.json retained
```

---

## Emulation Testing

The full boot sequence is tested in emulation:

```bash
cd hw-bringup/selftest/emulate
./run_emulated.sh
```

This starts a QEMU VM with:
- Fake PCIe device (FPGA shim)
- SoftHSM2 (software HSM)
- Fake NIC sovereignty interface
- Local PostgreSQL/Redis/Kafka containers

The boot sequence runs, selftest executes, and the output is compared to the expected `selftest.json` output. This proves the boot sequence works correctly end-to-end.

---

## The Honest Hardware Boundary

The `hw-bringup` code is real. But it has an honest boundary:

**Proven in emulation:**
- Boot sequence ordering
- Self-test logic and reporting
- Device interface contracts (probe functions)
- Service ordering and dependency management

**Pending physical hardware:**
- Final register-level driver implementation against device datasheets
- First-boot on-silicon PASS (the real FPGA, real HSM, real NIC)

This boundary is marked clearly in every README and in the Engineering Canon. It is never represented as complete on-hardware validation until the first physical node is brought up.
