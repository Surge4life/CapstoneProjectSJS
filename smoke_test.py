#!/usr/bin/env python3
"""
GODS ECOSYSTEM — end-to-end smoke test (F4).
One script that exercises the whole stack and asserts the full flow:
  boot self-test → backend live → governance decision → immutable audit →
  division flows → closed-loop snapshot → governance attachment handshake →
  signed offline release verify.
Exit 0 only if every stage passes.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8021
BASE = f"http://127.0.0.1:{PORT}"
passed, failed = [], []


def check(name, cond, detail=""):
    (passed if cond else failed).append(name)
    print(f"  {'✓' if cond else '✗'} {name}{(' — ' + detail) if detail else ''}")


def http(method, path, token=None, body=None, form=None):
    url = f"{BASE}{path}"
    headers = {}
    data = None
    if form is not None:
        data = urllib.parse.urlencode(form).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.load(r)


def stage(n, t):
    print(f"\n[{n}] {t}")


def main():
    print("=" * 66)
    print("  GODS ECOSYSTEM — END-TO-END SMOKE TEST")
    print("=" * 66)

    # 1) Hardware boot self-test (emulated) gates the node live
    stage(1, "Boot-to-live hardware self-test")
    rep = "/tmp/smoke_selftest.json"
    rc = subprocess.run([sys.executable, f"{ROOT}/hw-bringup/selftest/udoc_selftest.py",
                         "--emulate", "--quiet"], env=dict(os.environ, UDOC_SELFTEST_REPORT=rep)).returncode
    st = json.load(open(rep))
    check("self-test PASS → node LIVE", rc == 0 and st["gate_open"], st["overall"])

    # 2) Backend boots
    stage(2, "Platform-core backend boots")
    core = os.path.join(ROOT, "platform-core")
    subprocess.run([sys.executable, "seed.py"], cwd=core, capture_output=True)
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app",
                             "--host", "127.0.0.1", "--port", str(PORT)],
                            cwd=core, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ready = False
        for _ in range(30):
            try:
                if http("GET", "/health")["status"] == "ok":
                    ready = True; break
            except Exception:
                time.sleep(0.5)
        check("backend /health ok", ready)

        # 3) Auth
        stage(3, "Authentication")
        tok = http("POST", "/auth/login", form={"username": "admin@gods.local", "password": "admin123"})["access_token"]
        check("JWT login", bool(tok))

        # 4) Governance decision path
        stage(4, "UDOC governance decision path")
        ap = http("POST", "/decisions", token=tok, body={"model_id": "model-001"})
        check("healthy → APPROVE", ap["decision"] == "APPROVE", f"svs={ap['svs']}")
        check("within latency budget", ap["within_budget"], f"{ap['latency_ms']}ms")
        check("verdict sealed (64-hex)", len(ap["seal"]) == 64)
        bl = http("POST", "/decisions", token=tok, body={"model_id": "model-001", "risk_tier": "HIGH",
                  "priv_favorable": 600, "unpriv_favorable": 300, "ecs": 0.3})
        check("biased → BLOCK", bl["decision"] == "BLOCK", f"{len(bl['block_reasons'])} reasons")
        br = http("POST", "/decisions", token=tok, body={"model_id": "model-001", "traceroute": 0.4})
        check("sovereignty breach → BLOCK", br["decision"] == "BLOCK" and not br["sovereign"])

        # 5) Immutable audit
        stage(5, "Immutable audit chain")
        v = http("GET", "/audit/chain/verify", token=tok)
        check("audit chain intact", v["intact"] and v["records"] >= 3, f"{v['records']} records")
        mr = http("GET", "/audit/chain/merkle-root", token=tok)["merkle_root"]
        check("Merkle root published", len(mr) == 64)

        # 6) Division flows + loop
        stage(6, "Division flows + closed loop")
        http("POST", "/seths/enrol", token=tok, body={"count": 10})
        check("SETHS enrol", http("GET", "/seths/metrics")["total"] >= 10)
        http("POST", "/ts/projects", token=tok, body={"sector": "ENERGY", "name": "Solar",
             "workers_deployed": 4, "monthly_revenue": 2200000, "operating_margin": 0.32})
        check("TS deploy", http("GET", "/ts/metrics")["projects"] >= 1)
        http("POST", "/madiba/allocate", token=tok, body={"month": 1, "total_inflow": 1894000})
        check("MADIBA recycle", http("GET", "/madiba/metrics")["cumulative_recycled"] > 0)
        loop = http("GET", "/intelligence/loop-snapshot", token=tok)
        check("loop snapshot", loop["loop"] == "SETHS→TS→UDOC→MADIBA→SETHS")

        # 6b) UDOC data-record-and-analytics layer (feeds the standalone division platforms)
        stage("6b", "UDOC analytics layer (division platforms data source)")
        sk = http("GET", "/analytics/SETHS/kpis", token=tok)
        check("SETHS analytics KPIs", "placement_rate" in sk, f"placed={sk.get('placed')}")
        mk = http("GET", "/analytics/MADIBA/kpis", token=tok)
        check("MADIBA recycle ratio recorded", mk.get("recycle_ratio", 0) > 0, f"ratio={mk.get('recycle_ratio')}")
        tk = http("GET", "/analytics/TS/kpis", token=tok)
        check("TS analytics KPIs", tk.get("total_revenue", 0) > 0, f"rev={tk.get('total_revenue')}")
        ts_series = http("GET", "/analytics/MADIBA/timeseries?metric=inflow", token=tok)
        check("UDOC time-series query", "series" in ts_series)
        recs = http("GET", "/analytics/TS/records", token=tok)
        check("UDOC event records feed", len(recs["records"]) > 0, f"{len(recs['records'])} records")

        # 7) Governance attachment handshake
        stage(7, "UDOC agent attachment handshake")
        sys.path.insert(0, os.path.join(ROOT, "udoc-agent"))
        from udoc_agent import UDOCAgent
        agent = UDOCAgent(BASE, tok)
        check("agent→core APPROVE", agent.allow(agent.govern("model-001")))
        bad = UDOCAgent("http://127.0.0.1:9", tok)
        check("agent fail-closed when core down", bad.govern("model-001")["decision"] == "BLOCK")

        # 7b) Portal layer — full cross-portal lifecycle (Student → Employer → Employee)
        stage("7b", "Portal lifecycle (student→employer→employee)")
        sref = http("POST", "/portal/student/register",
                    body={"full_name": "Smoke Student", "email": "smoke@learner.za"})["student_ref"]
        http("POST", f"/portal/student/{sref}/progress?pct=100", token=tok)
        check("student registers + completes", bool(sref))
        eid = http("POST", "/portal/employer/register",
                   body={"org_name": "SmokeCorp", "contact_email": "hr@smoke.za"})["employer_id"]
        oid = http("POST", "/portal/employer/opportunities", token=tok,
                   body={"employer_id": eid, "title": "Dev", "positions": 1, "monthly_stipend": 18000})["id"]
        check("employer posts opportunity", bool(oid))
        http("POST", f"/portal/student/{sref}/apply/{oid}", token=tok)
        appid = http("GET", f"/portal/employer/opportunities/{oid}/applicants", token=tok)[0]["application_id"]
        empref = http("POST", f"/portal/employer/applications/{appid}/offer", token=tok)["employee_ref"]
        check("apply → offer → employee created", empref.startswith("EMP-"))
        http("POST", f"/portal/employee/{empref}/timesheet", token=tok, body={"hours": 160})
        slip = http("GET", f"/portal/employee/{empref}/payslip", token=tok)

        # 7c) Four dedicated app backends (UDOC SaaS control · documents · MADIBA · TS)
        stage("7c", "Four-app backends + document store")
        cli = http("POST", "/saas/register", body={"org_name": "SmokeAI", "contact_email": "s@ai.za", "tier": "SOVEREIGN"})
        check("UDOC SaaS client registers", cli["client_ref"].startswith("CLI-"))
        http("POST", "/registry/models", token=tok, body={"model_id": "sm-ai", "name": "X", "operator_id": cli["client_ref"], "risk_tier": "NOTABLE"})
        sus = http("POST", f"/saas/{cli['client_ref']}/suspend/sm-ai", token=tok)
        check("client kill-switch suspend", sus["status"] == "SUSPENDED")
        st = http("POST", "/portal/student/register", body={"full_name": "DocUser", "email": "doc@s.za"})["student_ref"]
        dlist = http("GET", f"/documents/owner/{st}", token=tok)
        check("document store reachable", isinstance(dlist, list))
        eng = http("POST", "/madiba/engage", token=tok, body={"investor_name": "PIC", "investor_type": "SOVEREIGN", "instrument": "blended", "indicated_amount": 500000000})
        check("MADIBA engagement created", eng["engagement_ref"].startswith("ENG-"))
        sub = http("POST", "/ts/submit/project", token=tok, body={"submitter_name": "DoE", "submitter_type": "GOV", "sector": "ENERGY", "title": "Grid", "capex_estimate": 100000000})
        check("TS project submitted", sub["submission_ref"].startswith("SUB-"))
        import urllib.request as _u, urllib.parse as _up, json as _j

        # 7d) Role/division access control — the G.O.D.S core launcher gating
        stage("7d", "Role-based access control (G.O.D.S core launcher)")
        prof = http("GET", "/access/profile", token=tok)
        check("admin profile opens all systems", len(prof["systems"]) == 5, f"{len(prof['systems'])} systems")
        # seed a scoped operator and verify enforcement
        http("POST", "/auth/register", body={"email": "smoke.seths@gods.local", "password": "p", "role": "operator", "division": "SETHS"})
        d = _up.urlencode({"username": "smoke.seths@gods.local", "password": "p"}).encode()
        stok = _j.load(_u.urlopen(_u.Request(BASE + "/auth/login", data=d, headers={"Content-Type": "application/x-www-form-urlencoded"})))["access_token"]
        sprof = http("GET", "/access/profile", token=stok)
        skeys = [s["key"] for s in sprof["systems"]]
        check("SETHS operator scoped to own systems", set(skeys) == {"holdings-overview", "seths-ops"}, str(skeys))
        try:
            http("GET", "/access/guard/udoc-gov", token=stok); check("backend denies cross-division open", False)
        except Exception:
            check("backend denies cross-division open", True, "udoc-gov → 403 for SETHS op")
        check("employee payslip computed", slip["net"] > 0, f"net R{slip['net']}")
    finally:
        proc.terminate()
        try: proc.wait(timeout=5)
        except Exception: proc.kill()

    # 8) Signed offline release verify
    stage(8, "Signed offline release (air-gap)")
    bundle = tempfile.mktemp(suffix=".tar.gz")
    subprocess.run([sys.executable, f"{ROOT}/infra/release-tooling/build_release.py",
                    "pack", f"{ROOT}/hw-bringup", bundle], capture_output=True)
    vr = subprocess.run([sys.executable, f"{ROOT}/infra/release-tooling/build_release.py",
                         "verify", bundle], capture_output=True, text=True)
    check("signed release verifies", vr.returncode == 0)

    # Summary
    print("\n" + "=" * 66)
    print(f"  RESULT: {len(passed)} passed, {len(failed)} failed")
    if failed:
        print("  FAILED: " + ", ".join(failed))
    else:
        print("  ✓ ENTIRE ECOSYSTEM FLOW VERIFIED END-TO-END")
    print("=" * 66)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
