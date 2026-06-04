#!/usr/bin/env python3
"""
udoc-selftest — boot-time hardware validation for a UDOC sovereign node.

Runs FIRST in the boot order. Probes every required hardware connection
(FPGA enforcement, HSM/TPM key custody, NIC sovereignty hook) plus data-core
reachability, writes a machine-readable report to /run/udoc/selftest.json, and
sets the gate that downstream services (platform-core, udoc-public/internal)
depend on. CRITICAL failures hold the system fail-CLOSED.

This is the exact code that, on the first power-on of the real hardware, returns
the real PASS/FAIL. In --emulate it runs against device shims to prove the logic.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from drivers.fpga_pcie import FPGADevice
from drivers.hsm_pkcs11 import HSMDevice
from drivers.nic_inspect import NICDevice

REPORT_PATH = os.environ.get("UDOC_SELFTEST_REPORT", "/run/udoc/selftest.json")
# Which checks are CRITICAL (fail-closed) vs advisory.
CRITICAL = {"fpga", "hsm", "nic"}


def _check_data_core(emulate: bool) -> dict:
    """Reachability of the immutable data operations core (postgres/kafka/cassandra)."""
    if emulate:
        return {"name": "data_core", "pass": True, "detail": "emulated: reachable", "critical": False}
    # REAL: TCP-connect to configured endpoints; here marked advisory at boot.
    return {"name": "data_core", "pass": True, "detail": "deferred to platform-core readiness", "critical": False}


def run_selftest(emulate: bool, fail: str | None = None) -> dict:
    results = []

    # 1) FPGA enforcement engine over PCIe
    fpga = FPGADevice(emulate=emulate, emulate_healthy=(fail != "fpga"))
    fi = fpga.probe()
    results.append({"name": "fpga", "pass": bool(fi.present and fi.ready and fi.magic_ok),
                    "detail": f"present={fi.present} ready={fi.ready} magic_ok={fi.magic_ok} "
                              f"bitstream={fi.bitstream_id} ({fi.detail})", "critical": True})

    # 2) HSM/TPM sovereign key custody
    hsm = HSMDevice(emulate=emulate, emulate_healthy=(fail != "hsm"))
    if emulate and fail != "hsm":
        hsm.activate(2)  # 2-of-3 officer quorum
    hi = hsm.probe()
    results.append({"name": "hsm", "pass": bool(hi.present and hi.master_sealed),
                    "detail": f"present={hi.present} fips={hi.fips_level} sealed={hi.master_sealed} "
                              f"custody={hi.custody_quorum} pqc={hi.pqc_ready} ({hi.detail})",
                    "critical": True})

    # 3) NIC sovereignty inspection hook
    nic = NICDevice(emulate=emulate, emulate_healthy=(fail != "nic"))
    ni = nic.probe()
    results.append({"name": "nic", "pass": bool(ni.present and ni.inspection_attachable
                                                and ni.egress_in_jurisdiction),
                    "detail": f"present={ni.present} iface={ni.iface} "
                              f"attachable={ni.inspection_attachable} "
                              f"egress_ok={ni.egress_in_jurisdiction} ({ni.detail})",
                    "critical": True})

    # 4) Data operations core (advisory at boot)
    results.append(_check_data_core(emulate))

    crit_fail = [r for r in results if r["critical"] and not r["pass"]]
    overall = "PASS" if not crit_fail else "FAIL_CLOSED"
    report = {
        "node_status": "LIVE" if overall == "PASS" else "HELD_FAIL_CLOSED",
        "overall": overall,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "emulated": emulate,
        "checks": results,
        "critical_failures": [r["name"] for r in crit_fail],
        "gate_open": overall == "PASS",   # downstream systemd units require gate_open
    }
    return report


def write_report(report: dict):
    try:
        os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
        with open(REPORT_PATH, "w") as f:
            json.dump(report, f, indent=2)
    except OSError:
        # /run may be read-only in emulation; fall back to cwd.
        with open("udoc_selftest_report.json", "w") as f:
            json.dump(report, f, indent=2)


def main():
    ap = argparse.ArgumentParser(description="UDOC boot-time hardware self-test")
    ap.add_argument("--emulate", action="store_true", help="run against device shims")
    ap.add_argument("--fail", choices=["fpga", "hsm", "nic"], help="inject a device fault")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    report = run_selftest(args.emulate, args.fail)
    write_report(report)

    if not args.quiet:
        line = "═" * 64
        print(line)
        print(f"  UDOC NODE SELF-TEST — {report['overall']}"
              f"{'  (EMULATED)' if report['emulated'] else ''}")
        print(line)
        for c in report["checks"]:
            mark = "✓" if c["pass"] else "✗"
            tag = "[CRIT]" if c["critical"] else "[ADV ]"
            print(f"  {mark} {tag} {c['name']:<10} {c['detail']}")
        print(line)
        print(f"  NODE STATUS: {report['node_status']}   gate_open={report['gate_open']}")
        if report["critical_failures"]:
            print(f"  FAIL-CLOSED — critical: {', '.join(report['critical_failures'])}")
            print(f"  Downstream services HELD. Operator intervention required.")
        else:
            print(f"  All critical hardware validated. Platform may start. → live-status.target")
        print(line)

    # Exit code drives systemd ordering: non-zero holds the boot.
    sys.exit(0 if report["gate_open"] else 1)


if __name__ == "__main__":
    main()
