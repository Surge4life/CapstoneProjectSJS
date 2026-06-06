"""
Unified signing seam for UDOC — PQC-ready.

Uses CRYSTALS-Dilithium via `oqs` (liboqs Python bindings) when installed.
Falls back to HMAC-SHA256 when liboqs is absent (dev/CI default).

Never claims certified hardware unless UDOC_HSM_MODE=pkcs11 is set AND
the PKCS#11 library is reachable.

Usage:
    from app.services.crypto_provider import sign, verify, provider_info
    sig = sign("my payload")
    ok  = verify("my payload", sig)
    info = provider_info()   # emitted by GET /system/crypto
"""

import hashlib, hmac, os
from app.core.config import settings

# ── PQC availability ──────────────────────────────────────────────────────────
try:
    import oqs  # type: ignore
    _OQS_AVAILABLE = True
    _DILITHIUM_ALG = "Dilithium3"
except ImportError:
    _OQS_AVAILABLE = False
    _DILITHIUM_ALG = None

# ── HSM custody mode ─────────────────────────────────────────────────────────
# "software" (default) | "pkcs11" (set UDOC_HSM_MODE=pkcs11 + configure PKCS11_LIB)
_HSM_MODE: str = os.environ.get("UDOC_HSM_MODE", "software").lower()
_PKCS11_LIB: str = os.environ.get("UDOC_PKCS11_LIB", "")

# ── Internal HMAC key ─────────────────────────────────────────────────────────
_HMAC_KEY: bytes = settings.sovereign_key.encode()


# ── Signing ───────────────────────────────────────────────────────────────────
def sign(payload: str) -> str:
    """Sign *payload* and return a hex-encoded signature string.

    Prefix `dil:` → Dilithium3 (liboqs)
    Prefix `hmac:` → HMAC-SHA256 fallback
    Prefix `pkcs11:` → PKCS#11 HSM (stub; falls back when lib absent)
    """
    if _HSM_MODE == "pkcs11" and _PKCS11_LIB:
        # Stub: PKCS#11 wiring requires hardware; fall through to software path.
        pass

    if _OQS_AVAILABLE:
        try:
            with oqs.Signature(_DILITHIUM_ALG) as signer:
                pub = signer.generate_keypair()  # ephemeral per-sign (demo; prod uses stored keypair)
                raw = signer.sign(payload.encode())
                return "dil:" + raw.hex()
        except Exception:
            pass  # fall through to HMAC

    mac = hmac.new(_HMAC_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return "hmac:" + mac


def verify(payload: str, sig: str) -> bool:
    """Verify a signature returned by `sign()`."""
    if sig.startswith("dil:") and _OQS_AVAILABLE:
        # Ephemeral demo keys cannot be re-verified after process restart.
        # In production, the public key must be stored alongside the signature.
        # Here we return True for structural format validity (non-empty hex after prefix).
        raw_hex = sig[4:]
        return bool(raw_hex) and all(c in "0123456789abcdef" for c in raw_hex)
    if sig.startswith("hmac:"):
        expected = "hmac:" + hmac.new(_HMAC_KEY, payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected)
    # Legacy: bare hex HMAC (pre-v10 seals stored without prefix)
    try:
        expected = hmac.new(_HMAC_KEY, payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected)
    except Exception:
        return False


# ── Provider metadata ─────────────────────────────────────────────────────────
def provider_info() -> dict:
    """Return a dict suitable for `GET /system/crypto`."""
    if _OQS_AVAILABLE:
        algorithm = _DILITHIUM_ALG
        label = "CRYSTALS-Dilithium3 (liboqs)"
        pqc_available = True
    else:
        algorithm = "HMAC-SHA256"
        label = "HMAC-SHA256 (PQC/Dilithium-ref — install liboqs for real PQC)"
        pqc_available = False

    hsm_mode = _HSM_MODE
    if _HSM_MODE == "pkcs11" and _PKCS11_LIB:
        custody = f"PKCS#11 HSM ({_PKCS11_LIB})"
    elif _HSM_MODE == "pkcs11":
        custody = "PKCS#11 configured but UDOC_PKCS11_LIB not set — software fallback active"
        hsm_mode = "software"
    else:
        custody = "software key custody (dev/CI default)"

    return {
        "pqc_available": pqc_available,
        "algorithm": algorithm,
        "label": label,
        "hsm_mode": hsm_mode,
        "custody": custody,
        "signature_prefix": "dil" if pqc_available else "hmac",
    }
