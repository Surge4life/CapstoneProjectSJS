# UDOC Secure Build / Signing Enclave — offline release tooling (air-gap)
Per hardware spec §8.2. Produces signed release bundles + import manifests for air-gapped sites.

```bash
# In the signing enclave (offline):
python3 build_release.py pack <src_dir> release.tar.gz   # hash every file, sign root via HSM
# Transfer release.tar.gz via signed media to the production site, then:
python3 build_release.py verify release.tar.gz           # re-hash + verify signature; exit!=0 on tamper
```
Manifest records: per-file SHA-256, root hash (chain-of-custody anchor), Dilithium signature
(emulated as HMAC here; real PKCS#11 C_Sign in production — private key never leaves the HSM).
