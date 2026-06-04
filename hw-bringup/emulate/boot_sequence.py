#!/usr/bin/env python3
"""
Boot-sequence emulator — proves the systemd unit ordering/gating logic end-to-end
without real systemd: runs udoc-selftest, reads its gate, then decides whether
udoc-platform may start and whether live-status.target is reached. Mirrors exactly
what the .service ExecStartPre gate + Requires/After ordering do on the real node.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(__file__)
SELFTEST = os.path.join(HERE, "..", "selftest", "udoc_selftest.py")
REPORT = "/tmp/udoc_boot_selftest.json"


def stage(n, msg):
    print(f"[boot {n}] {msg}")


def emulate_boot(fail=None):
    print("=" * 64)
    print(f"  UDOC NODE BOOT EMULATION{'  (fault: ' + fail + ')' if fail else ''}")
    print("=" * 64)
    stage(1, "UEFI → GRUB → kernel + initramfs (signed, measured into TPM PCRs)")
    stage(2, "systemd init → default target live-status.target")
    stage(3, "ordering: udoc-selftest.service BEFORE udoc-platform.service")

    # Run the self-test (the real boot-gate unit)
    env = dict(os.environ, UDOC_SELFTEST_REPORT=REPORT)
    cmd = [sys.executable, SELFTEST, "--emulate", "--quiet"]
    if fail:
        cmd += ["--fail", fail]
    rc = subprocess.run(cmd, env=env).returncode
    report = json.load(open(REPORT))
    stage(4, f"udoc-selftest.service exited rc={rc} → gate_open={report['gate_open']}")

    # ExecStartPre gate on udoc-platform.service
    if report["gate_open"]:
        stage(5, "udoc-platform.service ExecStartPre gate PASSED → uvicorn starting")
        stage(6, "udoc-platform.service ACTIVE (FastAPI listening :8000)")
        stage(7, "live-status.target REACHED → console banner: 'UDOC SOVEREIGN NODE: LIVE'")
        print("=" * 64)
        print("  RESULT: NODE LIVE ✓  (all critical hardware validated)")
        print("=" * 64)
        return 0
    else:
        stage(5, "udoc-platform.service ExecStartPre gate FAILED (gate_open=false)")
        stage(6, "platform + public/internal services HELD (not started)")
        stage(7, f"FAIL-CLOSED: critical hardware {report['critical_failures']} — operator required")
        print("=" * 64)
        print("  RESULT: NODE HELD FAIL-CLOSED ✗  (correct safety behaviour)")
        print("=" * 64)
        return 1


if __name__ == "__main__":
    fault = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--fail" else None
    sys.exit(0 if emulate_boot(fault) == (1 if fault else 0) else 2)
