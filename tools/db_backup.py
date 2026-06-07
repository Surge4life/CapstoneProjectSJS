#!/usr/bin/env python3
"""db_backup.py — download the ENTIRE G.O.D.S / UDOC datastore from a live core as one signed JSON file.

Run this on YOUR machine (no dependencies — standard library only) before the database is migrated
or expires. Example:

    python3 tools/db_backup.py \
        --base https://gods-platform-core.onrender.com \
        --email admin@gods.local --password admin123

Writes ./gods_backup_<UTC-timestamp>.json and prints the row counts it captured.
The core wakes on first request (free tier), so login is retried a few times automatically.
"""
import argparse
import datetime
import json
import sys
import time
import urllib.parse
import urllib.request


def _req(url, data=None, headers=None, method=None, timeout=120):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def login(base, email, password, attempts=6):
    body = urllib.parse.urlencode({"username": email, "password": password}).encode()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    last = None
    for i in range(attempts):
        try:
            status, raw = _req(base + "/auth/login", data=body, headers=headers, method="POST", timeout=60)
            if status == 200:
                return json.loads(raw)["access_token"]
            last = f"HTTP {status}: {raw[:200]!r}"
        except Exception as e:  # noqa: BLE001
            last = str(e)
        wait = 5 * (i + 1)
        print(f"  login attempt {i + 1}/{attempts} failed ({last}); server may be waking — retrying in {wait}s")
        time.sleep(wait)
    raise SystemExit(f"login failed after {attempts} attempts: {last}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://gods-platform-core.onrender.com")
    ap.add_argument("--email", required=True)
    ap.add_argument("--password", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    base = a.base.rstrip("/")

    print(f"→ logging in to {base} as {a.email}")
    token = login(base, a.email, a.password)
    print("  ✓ authenticated")

    print("→ exporting full datastore (GET /system/backup) …")
    status, raw = _req(base + "/system/backup",
                       headers={"Authorization": f"Bearer {token}"}, timeout=300)
    if status != 200:
        raise SystemExit(f"backup failed: HTTP {status}: {raw[:300]!r}")
    bundle = json.loads(raw)

    out = a.out or f"gods_backup_{datetime.datetime.utcnow():%Y%m%dT%H%M%SZ}.json"
    with open(out, "wb") as f:
        f.write(raw)

    print(f"  ✓ saved {out}  ({len(raw) / 1024:.1f} KB, {bundle.get('total_rows')} rows across "
          f"{bundle.get('source', {}).get('tables')} tables)")
    nonempty = {t: n for t, n in sorted(bundle.get("counts", {}).items()) if n}
    print("  rows captured:")
    for t, n in nonempty.items():
        print(f"    {t:<22} {n}")
    print(f"  seal: {bundle.get('seal', '')[:32]}…  ({bundle.get('source', {}).get('crypto', {}).get('label')})")
    print("\nKeep this file safe — it contains password/key hashes. Restore with tools/db_restore.py.")


if __name__ == "__main__":
    sys.exit(main())
