#!/usr/bin/env python3
"""db_restore.py — restore a G.O.D.S / UDOC backup bundle into a (usually fresh, empty) core.

Run on YOUR machine (standard library only). DRY-RUN first to see what WOULD load, then add
--confirm to actually WIPE the target database and load the bundle.

    # see what the bundle contains (changes nothing):
    python3 tools/db_restore.py --base https://gods-platform-core.onrender.com \
        --email admin@gods.local --password admin123 --file gods_backup_XXXX.json

    # actually restore (WIPES the target first):
    python3 tools/db_restore.py --base https://gods-platform-core.onrender.com \
        --email admin@gods.local --password admin123 --file gods_backup_XXXX.json --confirm

IMPORTANT: the target core must run with the SAME GODS_SOV_KEY the backup was sealed under, or seal
verification fails (intentional safety). If you knowingly changed the key, add --skip-verify.
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request


def _req(url, data=None, headers=None, method=None, timeout=300):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:  # surface FastAPI error detail
        return e.code, e.read()


def login(base, email, password, attempts=6):
    body = urllib.parse.urlencode({"username": email, "password": password}).encode()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    last = None
    for i in range(attempts):
        status, raw = _req(base + "/auth/login", data=body, headers=headers, method="POST", timeout=60)
        if status == 200:
            return json.loads(raw)["access_token"]
        last = f"HTTP {status}: {raw[:200]!r}"
        wait = 5 * (i + 1)
        print(f"  login attempt {i + 1}/{attempts} failed ({last}); retrying in {wait}s")
        time.sleep(wait)
    raise SystemExit(f"login failed after {attempts} attempts: {last}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://gods-platform-core.onrender.com")
    ap.add_argument("--email", required=True)
    ap.add_argument("--password", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--confirm", action="store_true", help="WIPE the target and load the bundle")
    ap.add_argument("--skip-verify", action="store_true", help="skip seal verification")
    a = ap.parse_args()
    base = a.base.rstrip("/")

    with open(a.file, "rb") as f:
        payload = f.read()
    bundle = json.loads(payload)
    print(f"→ bundle {a.file}: schema={bundle.get('schema')} generated={bundle.get('generated_at')} "
          f"rows={bundle.get('total_rows')}")

    print(f"→ logging in to {base} as {a.email}")
    token = login(base, a.email, a.password)
    print("  ✓ authenticated")

    q = {"confirm": "true" if a.confirm else "false",
         "skip_verify": "true" if a.skip_verify else "false"}
    url = base + "/system/restore?" + urllib.parse.urlencode(q)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    action = "RESTORING (wipe + load)" if a.confirm else "DRY-RUN (no changes)"
    print(f"→ {action} via POST /system/restore …")
    status, raw = _req(url, data=payload, headers=headers, method="POST", timeout=600)
    try:
        res = json.loads(raw)
    except Exception:  # noqa: BLE001
        res = {"raw": raw[:500].decode("utf-8", "replace")}
    if status != 200:
        print(f"  ✗ HTTP {status}: {json.dumps(res, indent=2)}")
        raise SystemExit(1)

    print("  ✓ " + ("RESTORED" if res.get("restored") else "dry-run complete"))
    print(json.dumps(res, indent=2))
    if not a.confirm:
        print("\nThis was a dry-run. Re-run with --confirm to actually wipe + load.")
    else:
        print("\nDone. Verify: log in, check /udoc/regulator/summary counts, and verify one certificate.")


if __name__ == "__main__":
    sys.exit(main())
