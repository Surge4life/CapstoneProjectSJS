"""
G.O.D.S / UDOC — L5 Sur²Secure Enclave attestation (patent v9.2, Layer 5).

The patent's L5 "Digital Bunker" runs the governance core inside a hardware-isolated enclave:
PMP-protected memory regions (TOR / NAPOT addressing modes, Part 4.2), a periodic G_VERIFY
integrity check (default hourly), and remote attestation (SEV-SNP / TrustZone class). This
router exposes that layer as software:

  • GET  /enclave/status   — L5 architecture + attestation scheme (public).
  • GET  /enclave/regions  — the PMP-protected memory map (public).
  • POST /enclave/attest   — run a G_VERIFY integrity attestation now (auth). Recomputes the
                             enclave measurement and compares it to the sealed golden value;
                             a mismatch fails closed. Writes a StayChain audit record.

HONESTY: the SHA-256 measurement over the enclave configuration is REAL. "PMP regions",
"SEV-SNP/TrustZone", "remote attestation quote", "hardware G_VERIFY" are the production design
— EMULATED here. The "quote" is an HMAC over the measurement + nonce, not a real TEE quote.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import hashlib, os, json

from app.db.session import get_db
from app.core.dependencies import principal
from app.services.audit_writer import append_audit
from app.services.governance_bridge import seal_payload

router = APIRouter(prefix="/enclave", tags=["UDOC L5 enclave"])
_now = lambda: datetime.now(timezone.utc).isoformat()

# The sealed enclave configuration (the components measured by G_VERIFY). In a real deployment
# this is the loaded firmware/policy image; here it is a fixed manifest we can hash.
ENCLAVE_IMAGE = {
    "core": "udoc-governance-core", "version": "9.2",
    "components": ["eva-engine", "policy-cells", "sovereign-verify", "staychain-writer"],
    "pmp_locked": True, "secure_boot": True,
}

# PMP-protected memory regions (Part 4.2). RO = read-only, RX = read-execute, RW = read-write.
PMP_REGIONS = [
    {"region": "axiom-store", "mode": "NAPOT", "access": "RO", "note": "128 governance axioms; immutable at runtime"},
    {"region": "policy-cells", "mode": "TOR", "access": "RO", "note": "active compiled policy rules"},
    {"region": "eva-text", "mode": "NAPOT", "access": "RX", "note": "EVA engine code; execute-only"},
    {"region": "key-custody", "mode": "NAPOT", "access": "RW", "note": "HSM-mediated; dual-custody"},
    {"region": "staychain-buffer", "mode": "TOR", "access": "RW", "note": "append-only audit staging"},
]

VERIFY_INTERVAL_SECONDS = 3600   # G_VERIFY periodic check (Part: default hourly)


def _measure(image: dict) -> str:
    """Real SHA-256 measurement over the canonical enclave image."""
    return hashlib.sha256(json.dumps(image, sort_keys=True).encode()).hexdigest()


# Golden measurement sealed at boot (the value G_VERIFY checks against).
GOLDEN_MEASUREMENT = _measure(ENCLAVE_IMAGE)


class AttestReq(BaseModel):
    nonce: str | None = Field(None, description="Challenge nonce for the attestation quote (freshness).")
    tamper: bool = Field(False, description="Demo only: simulate a tampered enclave image to show a FAILED attestation.")


@router.get("/status")
def enclave_status():
    """Public: the L5 Sur²Secure enclave architecture and attestation scheme."""
    return {
        "layer": "L5 — Sur²Secure Enclave (Digital Bunker)",
        "patent_ref": "v9.2 Layer 5 / Part 4.2",
        "isolation": "PMP-protected regions (TOR / NAPOT modes)",
        "tee_class": "SEV-SNP / TrustZone (emulated)",
        "integrity_check": {"mechanism": "G_VERIFY", "interval_seconds": VERIFY_INTERVAL_SECONDS,
                            "on_failure": "fail-closed — halt enclave, raise attestation alarm"},
        "secure_boot": ENCLAVE_IMAGE["secure_boot"],
        "golden_measurement": GOLDEN_MEASUREMENT,
        "real_vs_emulated": "SHA-256 measurement is REAL; PMP / SEV-SNP / remote-attestation "
                            "quote / hardware G_VERIFY are the production design, emulated here.",
        "endpoints": {
            "GET /enclave/regions": "PMP-protected memory map (public).",
            "POST /enclave/attest": "Run a G_VERIFY integrity attestation now (auth).",
        },
        "generated_at": _now(),
    }


@router.get("/regions")
def enclave_regions():
    """Public: the PMP-protected memory regions of the enclave."""
    return {
        "count": len(PMP_REGIONS),
        "regions": PMP_REGIONS,
        "note": "TOR/NAPOT are RISC-V PMP addressing modes; access enforced in hardware in "
                "production, described here.",
        "generated_at": _now(),
    }


@router.post("/attest")
def enclave_attest(req: AttestReq, db: Session = Depends(get_db),
                   user: dict = Depends(principal)):
    """
    Run a G_VERIFY integrity attestation now.

    Recomputes the enclave measurement and compares it to the sealed golden value. If they
    match, the enclave is attested and a remote-attestation quote is produced; if they differ
    (e.g. a tampered image), attestation FAILS and the enclave fails closed.
    """
    # In production this measures live enclave memory; here we measure the image, optionally
    # perturbed to demonstrate a detected-tamper path.
    image = dict(ENCLAVE_IMAGE)
    if req.tamper:
        image["components"] = image["components"] + ["UNVERIFIED-MODULE"]
    measurement = _measure(image)
    attested = (measurement == GOLDEN_MEASUREMENT)

    nonce = req.nonce or os.urandom(8).hex()
    # Emulated remote-attestation quote: HMAC over measurement + nonce (real HMAC, not a TEE quote).
    quote = seal_payload(f"ATTEST:{measurement}:{nonce}")

    ref = append_audit(db, "ENCLAVE_ATTEST", {
        "attested": attested, "measurement": measurement[:16], "tamper_demo": req.tamper,
        "actor": user.get("email") if isinstance(user, dict) else str(user),
    }, classification="INTERNAL", actor_class="SYSTEM")
    audit_ref = getattr(ref, "seq", None) or getattr(ref, "id", None)

    return {
        "g_verify": attested,
        "attested": attested,
        "verdict": "ATTESTED" if attested else "FAILED — enclave halted (fail-closed)",
        "measurement": measurement,
        "golden_measurement": GOLDEN_MEASUREMENT,
        "match": attested,
        "nonce": nonce,
        "attestation_quote": quote,
        "tee_class": "SEV-SNP / TrustZone (emulated)",
        "audit_ref": audit_ref,
        "note": "Measurement (SHA-256) is real; quote/TEE are emulated. A mismatch fails closed.",
        "generated_at": _now(),
    }
