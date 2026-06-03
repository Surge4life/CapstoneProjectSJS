# UDOC Hardware Bring-Up — boot-to-live stack
The software that is flashed onto a new UDOC sovereign node and, on first power-on,
validates every hardware connection, then reaches live status.

## What this is (honest)
- **Real code**, written against the interfaces in `UDOC_Full_Hardware_Specification v1.0`:
  bootloader/init ordering, device-interface drivers (FPGA-over-PCIe, HSM/TPM via PKCS#11,
  NIC sovereignty hook), a boot-time self-test that probes each device and emits PASS/FAIL,
  and systemd units that gate the platform on a clean self-test.
- **Tested in emulation** (QEMU + device shims) so the boot+self-test logic provably runs
  and reports correctly with mocked devices.
- **Pending real hardware:** the register-level finalisation of each driver against the
  device datasheet, and the first-boot on-silicon PASS. The self-test shipped here is
  exactly what produces that PASS/FAIL the first time the real board is switched on.

## Layout
```
hw-bringup/
├── drivers/      device-interface layer (fpga_pcie, hsm_pkcs11, nic_inspect) + EMULATION shims
├── selftest/     udoc-selftest: probes all devices, writes /run/udoc/selftest.json, gates boot
├── init/         systemd units + ordering (selftest → platform → live-status.target)
├── boot/         bootloader/OS-image notes + build script (minimal immutable rootfs)
└── emulate/      QEMU harness proving the boot sequence runs
```

## Run the emulation proof
```bash
python3 selftest/udoc_selftest.py --emulate     # all devices mocked → PASS, live status
python3 selftest/udoc_selftest.py --emulate --fail fpga   # inject FPGA fault → fail-closed
```
