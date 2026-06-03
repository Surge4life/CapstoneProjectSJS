# UDOC Node OS Image — build & flash notes
Target: the node classes in `UDOC_Full_Hardware_Specification v1.0` (x86-64 server class
with UEFI + TPM 2.0 + signed firmware; PCIe FPGA card; network-attached HSM; 25/100GbE NIC).

## Image principles (from the spec's non-negotiables)
- **Minimal, immutable rootfs** (read-only `/`, writable `/var` + `/run`) so the governance
  software estate is tamper-resistant and updated only via signed offline-capable bundles.
- **Secure/measured boot**: UEFI Secure Boot + TPM 2.0 PCR measurement of kernel + initramfs;
  the HSM holds the sovereign key hierarchy (master never leaves HSM).
- **Self-test gates boot**: `udoc-selftest.service` runs before any platform service and
  fails CLOSED on any critical hardware fault.
- **Air-gap capable**: no dependency on public cloud; updates arrive as signed import bundles
  produced by the secure build/signing enclave.

## Build recipe (reference; produced by the secure build enclave)
1. Base: a minimal Debian/Ubuntu LTS or RHEL-class server image, server kernel.
2. Overlay `/opt/udoc/` = this repo (hw-bringup, platform-core, governance-engines).
3. Install Python 3.12 + `platform-core/requirements.txt` into a venv at `/opt/udoc/venv`.
4. Install systemd units from `hw-bringup/init/` into `/etc/systemd/system/`, enable
   `udoc-selftest.service`, `udoc-platform.service`, `udoc-live-banner.service`.
5. Set default target to `live-status.target`.
6. Make `/` read-only; mark `/run/udoc` tmpfs.
7. Sign the resulting image + produce an import manifest (hashes, Dilithium signature).
8. Flash via the boot media; first power-on runs the self-test against real devices.

## Bootloader
- UEFI (x86-64 server). GRUB2 entry boots the signed kernel + initramfs.
- For ARM64/custom-SoC node classes, swap to U-Boot + device tree (porting guide in repo root).

## Honest boundary
Steps 1–8 are real and scriptable; the only step that requires the physical board is the
first-power-on PASS, which `udoc-selftest` produces and reports automatically.
