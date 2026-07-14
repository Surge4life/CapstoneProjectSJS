#!/usr/bin/env python3
"""
UDOC Secure Build / Signing Enclave — offline release bundle + import manifest.

Per hardware spec §8.2: air-gapped deployments need a separate signing enclave that
(1) creates a release bundle, (2) signs it, (3) records every file hash, (4) produces an
import manifest the production site verifies before applying. Private key material never
leaves the HSM; here the HSM signing is emulated (real PKCS#11 in production).

Usage:
  build_release.py pack   <src_dir> <out_bundle.tar.gz>   # build + sign a release
  build_release.py verify <bundle.tar.gz>                  # verify manifest + signature
"""
import argparse
import hashlib
import json
import os
import sys
import tarfile
import time

# Emulated sovereign signing key (production: HSM PKCS#11 C_Sign, Dilithium).
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "hw-bringup"))
try:
    from drivers.hsm_pkcs11 import HSMDevice
    _HSM = HSMDevice(emulate=True, emulate_healthy=True)
except Exception:
    _HSM = None

MANIFEST_NAME = "UDOC_IMPORT_MANIFEST.json"


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _file_list(src_dir: str):
    for root, _dirs, files in os.walk(src_dir):
        for fn in files:
            if "__pycache__" in root or fn.endswith(".pyc") or fn == MANIFEST_NAME:
                continue
            full = os.path.join(root, fn)
            yield full, os.path.relpath(full, src_dir)


def pack(src_dir: str, out_bundle: str) -> dict:
    # 1) hash every file
    files = []
    for full, rel in sorted(_file_list(src_dir), key=lambda x: x[1]):
        files.append({"path": rel, "sha256": _sha256_file(full),
                      "size": os.path.getsize(full)})
    # 2) root hash = hash over the sorted (path:hash) lines  (chain-of-custody anchor)
    root_material = "\n".join(f"{f['path']}:{f['sha256']}" for f in files)
    root_hash = hashlib.sha256(root_material.encode()).hexdigest()
    # 3) HSM signature over the root hash (private key never leaves HSM)
    signature = _HSM.sign(root_hash.encode()) if _HSM else "no-hsm"
    manifest = {
        "manifest_version": "1.0",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_dir": os.path.basename(os.path.abspath(src_dir)),
        "file_count": len(files),
        "root_hash": root_hash,
        "signature_alg": "dilithium(emulated:hmac-sha256)",
        "signature": signature,
        "fips_target": "FIPS 140-3 L3",
        "files": files,
    }
    # 4) write manifest into the source, then tar everything (manifest travels inside)
    mpath = os.path.join(src_dir, MANIFEST_NAME)
    with open(mpath, "w") as f:
        json.dump(manifest, f, indent=2)
    with tarfile.open(out_bundle, "w:gz") as tar:
        tar.add(src_dir, arcname=os.path.basename(os.path.abspath(src_dir)))
    os.remove(mpath)
    return manifest


def verify(bundle: str) -> dict:
    """Production-site check: extract manifest, re-hash every file, verify signature."""
    import tempfile
    tmp = tempfile.mkdtemp()
    with tarfile.open(bundle, "r:gz") as tar:
        tar.extractall(tmp)
    # locate manifest
    mpath = None
    for root, _d, files in os.walk(tmp):
        if MANIFEST_NAME in files:
            mpath = os.path.join(root, MANIFEST_NAME); break
    if not mpath:
        return {"verified": False, "error": "manifest not found"}
    manifest = json.load(open(mpath))
    base = os.path.dirname(mpath)
    # re-hash
    mismatches = []
    for entry in manifest["files"]:
        full = os.path.join(base, entry["path"])
        if not os.path.exists(full):
            mismatches.append({"path": entry["path"], "issue": "missing"}); continue
        actual = _sha256_file(full)
        if actual != entry["sha256"]:
            mismatches.append({"path": entry["path"], "issue": "hash mismatch"})
    # recompute root hash + verify signature
    root_material = "\n".join(f"{f['path']}:{f['sha256']}" for f in manifest["files"])
    root_hash = hashlib.sha256(root_material.encode()).hexdigest()
    root_ok = (root_hash == manifest["root_hash"])
    sig_ok = bool(_HSM and _HSM.sign(root_hash.encode()) == manifest["signature"])
    return {
        "verified": root_ok and sig_ok and not mismatches,
        "root_hash_ok": root_ok, "signature_ok": sig_ok,
        "file_count": manifest["file_count"], "mismatches": mismatches,
        "chain_of_custody": "intact" if (root_ok and sig_ok and not mismatches) else "BROKEN",
    }


def main():
    ap = argparse.ArgumentParser(description="UDOC secure offline release tooling")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pack"); p.add_argument("src"); p.add_argument("out")
    v = sub.add_parser("verify"); v.add_argument("bundle")
    a = ap.parse_args()
    if a.cmd == "pack":
        m = pack(a.src, a.out)
        print(f"✓ release bundle: {a.out}")
        print(f"  files={m['file_count']} root_hash={m['root_hash'][:24]}…")
        print(f"  signature={m['signature'][:24]}…  ({m['signature_alg']})")
    else:
        r = verify(a.bundle)
        print(json.dumps(r, indent=2))
        sys.exit(0 if r["verified"] else 1)


if __name__ == "__main__":
    main()
