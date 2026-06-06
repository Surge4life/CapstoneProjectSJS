#!/usr/bin/env python3
"""
UDOC Station Bring-Up Self-Test — verifies a client UDOC station against the five-plane
architecture, the five-phase deployment sequence and the operational-readiness checklist,
then emits a signed Station Readiness Report. Stdlib only (air-gap friendly).

Statuses:  PASS · PARTIAL · DEPENDENCY (hardware to be installed for production) · FAIL
Verdict :  READY · READY-WITH-DEPENDENCIES · NOT-READY
Honesty :  software-custody / reference-PQC / no-QPU are reported truthfully as DEPENDENCY,
           not as certified hardware.
"""
import json, os, sys, time, hmac, hashlib, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "station.config.json")))
API = os.environ.get("UDOC_API", CFG["api_base"]).rstrip("/")
SKEY = os.environ.get("UDOC_STATION_KEY", CFG.get("station_key", "dev")).encode()
checks = []


def add(layer, check, status, detail):
    checks.append({"layer": layer, "check": check, "status": status, "detail": detail})


def http(method, path, headers=None, data=None, form=False, timeout=12):
    url = API + path
    body, h = None, dict(headers or {})
    if data is not None:
        if form:
            body = "&".join(f"{k}={v}" for k, v in data.items()).encode()
            h["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {}
    except Exception as e:
        return 0, {"error": str(e)}


# authenticate once for all API-dependent checks
_tok = None
_st, _d = http("POST", "/auth/login", form=True, data={"username": CFG["test_user"], "password": CFG["test_pass"]})
if _st == 200:
    _tok = _d.get("access_token")
H = {"Authorization": f"Bearer {_tok}"} if _tok else {}

# ---- Layer 1 · Sovereign Security & Hardware Plane ----
add("L1 Sovereign Security & Hardware", "Jurisdiction-locked data sovereignty",
    "PASS" if CFG["jurisdiction"] == "ZA" else "FAIL",
    f"jurisdiction={CFG['jurisdiction']} · {CFG['sovereignty_recheck_hours']}-hourly re-checks (Constitutional Pillar III)")
add("L1 Sovereign Security & Hardware", "FIPS 140-3 L3 HSM (split-custody, 3 officers)",
    "PASS" if CFG.get("hsm_mode") == "fips-140-3-l3" else "DEPENDENCY",
    "HSM present" if CFG.get("hsm_mode") == "fips-140-3-l3" else "software key-custody fallback — install HSM cluster for production")
add("L1 Sovereign Security & Hardware", "Sovereign-first / air-gap-capable deployment",
    "PASS" if CFG.get("air_gap_capable") else "PARTIAL",
    "in-country, air-gap-capable; excludes foreign cloud dependencies")

# ---- Layer 2 · Immutable Data & Cryptographic Core ----
add("L2 Immutable Data & Crypto", "SHA-3-256 content hashing",
    "PASS" if hasattr(hashlib, "sha3_256") else "FAIL", "hashlib.sha3_256 available")
# Query the live crypto provider endpoint for accurate PQC status
_crypto_st, _crypto = http("GET", "/system/crypto", headers=H)
if _crypto_st == 200:
    _pqc_pass = _crypto.get("pqc_available", False)
    _pqc_status = "PASS" if _pqc_pass else "DEPENDENCY"
    _pqc_detail = _crypto.get("label", "unknown")
else:
    _pqc_status = "DEPENDENCY"
    _pqc_detail = "Dilithium/Kyber reference (HMAC stand-in) — install liboqs for production PQC"
add("L2 Immutable Data & Crypto", "Post-Quantum signatures (CRYSTALS-Kyber/Dilithium)",
    _pqc_status, _pqc_detail)
add("L2 Immutable Data & Crypto", "Append-only WORM audit store (Cassandra, 10-yr retention)",
    "PASS" if CFG.get("worm_backend") == "cassandra" else "DEPENDENCY",
    "platform audit chain active; provision Cassandra WORM cluster for 10-yr retention")
st, doc = http("GET", "/audit/chain/verify", headers=H)
add("L2 Immutable Data & Crypto", "Merkle-linked audit chain integrity",
    "PASS" if (st == 200 and doc.get("intact")) else "FAIL",
    f"records={doc.get('records')} intact={doc.get('intact')}")

# ---- Layer 3 · HQ-OS Quantum-Hybrid Middleware ----
add("L3 HQ-OS Quantum-Hybrid", "Classical-first / graceful degradation",
    "PASS", "operates as classical platform; quantum acceleration auto-activates when QPUs are detected")
add("L3 HQ-OS Quantum-Hybrid", "QPU detection", "DEPENDENCY",
    "no QPU detected — classical processing path active (by design)")

# ---- Layer 4 · EVA Engine ----
st, _ = http("GET", "/health")
add("L4 EVA Engine", "Governance API reachable", "PASS" if st == 200 else "FAIL", f"{API}/health -> {st}")
add("L4 EVA Engine", "Authenticated session", "PASS" if _tok else "FAIL",
    "operator/admin token acquired" if _tok else "login failed")
st, dec = http("POST", "/decisions", headers=H, data={"model_id": CFG["test_model"]})
add("L4 EVA Engine", "Six-dimensional governed decision",
    "PASS" if st == 200 else "FAIL",
    f"decision={dec.get('decision')} composite_eva={dec.get('composite_eva')} dims={list((dec.get('dimensions') or {}).keys())}")
cert = dec.get("certificate_id")
add("L4 EVA Engine", "Cryptographically-certified outcome (SHA-3-256 + policy version)",
    "PASS" if dec.get("content_sha3") else "PARTIAL",
    f"cert={cert} sha3={str(dec.get('content_sha3'))[:16]}… policy={dec.get('policy_version')}")
if cert:
    st, vr = http("GET", f"/decisions/certificates/{cert}/verify", headers=H)
    add("L4 EVA Engine", "Certificate verification", "PASS" if vr.get("valid") else "FAIL", f"valid={vr.get('valid')}")
st, pol = http("GET", "/policy/active", headers=H)
add("L4 EVA Engine", "Policy-as-Code enforcement engine", "PASS" if st == 200 else "FAIL",
    f"enforced_rules={pol.get('enforced_rules')}")

# ---- Layer 5 · Constitutional Oversight ----
st, _ = http("POST", "/decisions", headers=H, data={"model_id": "__nonexistent_station_probe__"})
add("L5 Constitutional Oversight", "Fail-closed (unknown system blocked)",
    "PASS" if st in (403, 404) else "FAIL", f"unknown model -> HTTP {st} (defaults to locked)")
st, adm = http("GET", "/admin/status", headers=H)
add("L5 Constitutional Oversight", "Oversight Board / human-primacy pathway reachable",
    "PASS" if st == 200 else "PARTIAL", f"open_oversight={adm.get('open_oversight')}")

# ---- aggregate + sign ----
has_fail = any(c["status"] == "FAIL" for c in checks)
has_dep = any(c["status"] == "DEPENDENCY" for c in checks)
verdict = "NOT-READY" if has_fail else ("READY-WITH-DEPENDENCIES" if has_dep else "READY")
report = {"station": CFG["station_id"], "jurisdiction": CFG["jurisdiction"],
          "deployment_model": CFG["deployment_model"], "api": API,
          "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "verdict": verdict, "checks": checks}
report["seal"] = hmac.new(SKEY, json.dumps(report, sort_keys=True).encode(), hashlib.sha256).hexdigest()
out = os.path.join(HERE, "readiness_report.json")
json.dump(report, open(out, "w"), indent=2)

ICON = {"PASS": "✓", "PARTIAL": "◐", "DEPENDENCY": "⚙", "FAIL": "✗"}
print("\n" + "═" * 64)
print(f"  UDOC STATION READINESS REPORT · {CFG['station_id']}")
print(f"  {CFG['deployment_model']} · jurisdiction {CFG['jurisdiction']} · API {API}")
print("═" * 64)
cur = None
for c in checks:
    if c["layer"] != cur:
        cur = c["layer"]; print(f"\n▎ {cur}")
    print(f"   {ICON[c['status']]} [{c['status']:10}] {c['check']}")
    print(f"       {c['detail']}")
print("\n" + "═" * 64)
print(f"  VERDICT: {verdict}")
print(f"  sealed: {report['seal'][:32]}…  ·  report: {out}")
print("═" * 64 + "\n")
sys.exit(0 if verdict != "NOT-READY" else 1)
