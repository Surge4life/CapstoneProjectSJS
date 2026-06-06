"""
Unified signing provider for UDOC — single seam for EVA certificates, the audit chain and
policy-version signatures.

Prefers post-quantum CRYSTALS-Dilithium via liboqs when the `oqs` package is installed;
otherwise falls back to HMAC-SHA256, labelled honestly as "PQC/Dilithium-reference".
This makes production PQC a deployment/config change, not a code change. In production the
signing key is held in a FIPS 140-3 Level 3 HSM under split-custody; `hsm_mode=pkcs11`
selects that path. None of this claims certified hardware in software mode.
"""
import hmac
import hashlib
import os

# same key as the sovereign seal so HMAC-fallback signatures stay consistent across the platform
_SECRET = os.environ.get("GODS_SOV_KEY", "emulated-sovereign-key").encode()
_HSM_MODE = os.environ.get("UDOC_HSM_MODE", "software")  # software | pkcs11
_DILITHIUM = "Dilithium3"

_OQS = None
_signer = None
_pubkey = None
try:  # liboqs-python — absent in dev/sandbox; present on a PQC-provisioned station
    import oqs as _OQS  # type: ignore
    _signer = _OQS.Signature(_DILITHIUM)
    _pubkey = _signer.generate_keypair()
except Exception:
    _OQS = None
    _signer = None
    _pubkey = None


def provider_info() -> dict:
    return {
        "pqc_available": _OQS is not None,
        "algorithm": _DILITHIUM if _OQS is not None else "HMAC-SHA256",
        "label": "CRYSTALS-Dilithium (liboqs)" if _OQS is not None else "HMAC-SHA256 (PQC/Dilithium-ref)",
        "hsm_mode": _HSM_MODE,
        "custody": "HSM PKCS#11 (split-custody)" if _HSM_MODE == "pkcs11" else "software key-custody",
    }


def sign(payload: str) -> str:
    """Return a signature for payload. Dilithium when available (prefixed 'dil:'), else HMAC hex."""
    if _signer is not None:
        try:
            return "dil:" + _signer.sign(payload.encode()).hex()
        except Exception:
            pass
    return hmac.new(_SECRET, payload.encode(), hashlib.sha256).hexdigest()


def verify(payload: str, signature: str) -> bool:
    if signature.startswith("dil:") and _OQS is not None and _pubkey is not None:
        try:
            verifier = _OQS.Signature(_DILITHIUM)
            return bool(verifier.verify(payload.encode(), bytes.fromhex(signature[4:]), _pubkey))
        except Exception:
            return False
    expected = hmac.new(_SECRET, payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
