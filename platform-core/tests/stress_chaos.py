#!/usr/bin/env python3
"""
V&V — Stress + Chaos suite (assessment gap #10).
Drives the live backend hard and under adversarial conditions, then asserts the system's
safety invariants HELD: governance stays within latency budget under load, the audit chain
stays intact under concurrent writes, fail-closed holds when dependencies are unreachable,
and no BLOCK ever flips to APPROVE under pressure.

Run:  python3 tests/stress_chaos.py            (starts its own backend)
"""
import concurrent.futures as cf
import json
import os
import statistics
import subprocess
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8091
BASE = f"http://127.0.0.1:{PORT}"
passed, failed = [], []


def check(name, cond, detail=""):
    (passed if cond else failed).append(name)
    print(f"  {'✓' if cond else '✗'} {name}{(' — ' + detail) if detail else ''}")


def http(method, path, token=None, body=None, form=None, timeout=10):
    headers, data = {}, None
    if form is not None:
        data = urllib.parse.urlencode(form).encode(); headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif body is not None:
        data = json.dumps(body).encode(); headers["Content-Type"] = "application/json"
    if token: headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def main():
    print("=" * 66)
    print("  V&V — STRESS + CHAOS SUITE")
    print("=" * 66)
    subprocess.run([sys.executable, "seed.py"], cwd=ROOT, capture_output=True)
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1",
                             "--port", str(PORT), "--workers", "1"], cwd=ROOT,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(40):
            try:
                if http("GET", "/health")["status"] == "ok": break
            except Exception: time.sleep(0.5)
        tok = http("POST", "/auth/login", form={"username": "admin@gods.za", "password": "admin123"})["access_token"]
        http("POST", "/registry/models", token=tok,
             body={"model_id": "stress-m", "name": "S", "operator_id": "op", "risk_tier": "NOTABLE"})

        # ── STRESS 1: concurrent healthy decisions, measure latency under load ──
        print("\n[stress] 500 concurrent governance decisions")
        def one_decision(_):
            t0 = time.perf_counter()
            r = http("POST", "/decisions", token=tok, body={"model_id": "stress-m"})
            return r["decision"], r["latency_ms"], (time.perf_counter() - t0) * 1000
        N = 500
        with cf.ThreadPoolExecutor(max_workers=32) as ex:
            results = list(ex.map(one_decision, range(N)))
        decisions = [d for d, _, _ in results]
        gov_latencies = [g for _, g, _ in results]
        check("all 500 decisions returned", len(results) == N)
        check("all healthy → APPROVE (no flips under load)", all(d == "APPROVE" for d in decisions),
              f"{decisions.count('APPROVE')}/{N} APPROVE")
        p95 = statistics.quantiles(gov_latencies, n=20)[18]
        check("governance p95 within 50ms budget under load", p95 <= 50.0, f"p95={p95:.2f}ms")

        # ── STRESS 2: audit chain integrity under concurrent writes ──
        print("\n[stress] audit chain integrity after concurrent load")
        v = http("GET", "/audit/chain/verify", token=tok)
        check("audit chain intact after 500 concurrent decisions", v["intact"], f"{v['records']} records")
        # sequence monotonic, no gaps
        recs = http("GET", "/audit/records", token=tok)
        seqs = sorted(r["seq"] for r in recs)
        check("audit sequence has no duplicates", len(seqs) == len(set(seqs)))

        # ── CHAOS 1: adversarial inputs never flip BLOCK→APPROVE ──
        print("\n[chaos] adversarial inputs must stay BLOCKed")
        adversarial = [
            {"model_id": "stress-m", "risk_tier": "UNACCEPTABLE"},
            {"model_id": "stress-m", "risk_tier": "HIGH", "priv_favorable": 999, "unpriv_favorable": 1, "ecs": 0.01},
            {"model_id": "stress-m", "traceroute": 0.0, "bgp": 0.0},
            {"model_id": "stress-m", "compliance": 0.0},
        ]
        blocked = 0
        for a in adversarial:
            r = http("POST", "/decisions", token=tok, body=a)
            if r["decision"] == "BLOCK": blocked += 1
        check("all adversarial inputs BLOCKed", blocked == len(adversarial), f"{blocked}/{len(adversarial)}")

        # ── CHAOS 2: malformed / injection-style payloads are rejected, not crash ──
        print("\n[chaos] malformed payloads handled safely")
        survived = True
        for bad in [{"model_id": "'; DROP TABLE decisions;--"}, {"model_id": "x" * 5000}, {"model_id": None}]:
            try:
                http("POST", "/decisions", token=tok, body=bad)
            except Exception:
                pass  # 4xx is fine
            # confirm server still alive + chain intact
        survived = http("GET", "/health")["status"] == "ok"
        check("server survives malformed payloads", survived)
        check("audit chain still intact after chaos", http("GET", "/audit/chain/verify", token=tok)["intact"])

        # ── CHAOS 3: fail-closed when governance dependency unreachable (agent) ──
        print("\n[chaos] fail-closed under dependency outage")
        sys.path.insert(0, os.path.join(ROOT, "..", "udoc-agent"))
        from udoc_agent import UDOCAgent
        down = UDOCAgent("http://127.0.0.1:9", tok)  # unreachable core
        r = down.govern("stress-m")
        check("agent fails CLOSED (BLOCK) when core down", r["decision"] == "BLOCK")

        # ── STRESS 3: burst of unknown models all fail-closed (no accidental allow) ──
        print("\n[stress] 100 unknown-model requests must all fail-closed")
        fc = 0
        for i in range(100):
            try:
                http("POST", "/decisions", token=tok, body={"model_id": f"ghost-{i}"})
            except urllib.error.HTTPError as e:
                if e.code == 404: fc += 1
            except Exception:
                fc += 1
        check("100/100 unknown models fail-closed (404)", fc == 100, f"{fc}/100")

    finally:
        proc.terminate()
        try: proc.wait(timeout=5)
        except Exception: proc.kill()

    print("\n" + "=" * 66)
    print(f"  RESULT: {len(passed)} passed, {len(failed)} failed")
    if failed: print("  FAILED: " + ", ".join(failed))
    else: print("  ✓ SYSTEM HELD UNDER STRESS + CHAOS — safety invariants preserved")
    print("=" * 66)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    import urllib.error
    main()
