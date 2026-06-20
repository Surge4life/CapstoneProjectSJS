#!/usr/bin/env python3
"""
UDOC / G.O.D.S — Capstone Snapshot Exporter
═══════════════════════════════════════════
Run this against your LIVE Platform Core API to freeze the entire platform state into one JSON file,
so the Netlify Capstone showcase keeps working after the gods-db database is removed on 2026-07-03.

USAGE (no dependencies — just Python 3):
    python3 export_snapshot.py https://gods-platform-core.onrender.com admin@gods.local admin123

Output: capstone-snapshot.json  (drop this next to the Capstone hub page on Netlify)

Run it a few times before July 3; the latest file is the one that ships.
"""
import sys, json, datetime, urllib.request, urllib.error
from urllib.parse import urlencode

def main():
    if len(sys.argv) < 4:
        print("usage: python3 export_snapshot.py <API_BASE_URL> <email> <password>"); sys.exit(1)
    base = sys.argv[1].rstrip("/"); email = sys.argv[2]; pw = sys.argv[3]

    def req(path, token=None, form=None):
        url = base + path
        data = urlencode(form).encode() if form else None
        r = urllib.request.Request(url, data=data, method="POST" if data else "GET")
        if token: r.add_header("Authorization", "Bearer " + token)
        if form: r.add_header("Content-Type", "application/x-www-form-urlencoded")
        try:
            with urllib.request.urlopen(r, timeout=45) as resp:
                return resp.status, json.loads(resp.read().decode() or "null")
        except urllib.error.HTTPError as e:
            return e.code, None
        except Exception as e:
            return 0, None

    print(f"→ Authenticating at {base} as {email} …")
    st, body = req("/auth/login", form={"username": email, "password": pw})
    if st != 200 or not body or "access_token" not in body:
        print(f"  ✗ login failed (HTTP {st}). Check the URL/credentials and that the service is awake."); sys.exit(2)
    tok = body["access_token"]
    print(f"  ✓ signed in as role={body.get('role')}")

    # (label, path) — best-effort; missing endpoints are simply skipped
    ENDPOINTS = [
        ("summary",            "/udoc/regulator/summary"),
        ("portals",            "/access/profiles"),
        ("access_matrix",      "/access/matrix"),
        ("rbac_matrix",        "/rbac/matrix"),
        ("decisions",          "/decisions"),
        ("certificates",       "/decisions/certificates"),
        ("models",             "/registry/models"),
        ("oversight_cases",    "/oversight/cases"),
        ("conformance_status", "/conformance/status"),
        ("conformance_systems","/conformance/systems"),
        ("conformance_findings","/conformance/findings?limit=200"),
        ("conformance_scans",  "/conformance/scans?limit=100"),
        ("audit_records",      "/audit/records"),
        ("audit_merkle_root",  "/audit/chain/merkle-root"),
        ("sectors",            "/sector/frameworks"),
        ("tenants",            "/tenants"),
    ]
    snap = {"_meta": {
        "source": base,
        "exported_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "exported_by": email,
        "purpose": "Capstone showcase snapshot — survives gods-db decommission (2026-07-03).",
        "captured": []
    }}
    for label, path in ENDPOINTS:
        st, body = req(path, token=tok)
        if st == 200 and body is not None:
            snap[label] = body
            n = len(body) if isinstance(body, list) else (len(body.get("profiles", body)) if isinstance(body, dict) else 1)
            snap["_meta"]["captured"].append(label)
            print(f"  ✓ {label:22s} ({'list:'+str(len(body)) if isinstance(body,list) else 'object'})")
        else:
            print(f"  · {label:22s} skipped (HTTP {st})")

    out = "capstone-snapshot.json"
    with open(out, "w") as f:
        json.dump(snap, f, indent=2, default=str)
    import os
    print(f"\n✓ Wrote {out} — {os.path.getsize(out)//1024} KB, {len(snap['_meta']['captured'])} datasets captured.")
    print("  Place this file next to your Capstone hub page on Netlify and redeploy.")

if __name__ == "__main__":
    main()
