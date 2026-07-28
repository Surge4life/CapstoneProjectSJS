"""Public Citizen Portal API — AI rights challenges without client login.

Attached to existing platform-core + Neon. Does not create a Render service.
Auth-gated /oversight/* remains for operators; this path is citizen-facing.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.db.session import get_db
from app.db.models import OversightCase
from app.services.audit_writer import append_audit
import uuid
import re

router = APIRouter(prefix="/citizen", tags=["citizen"])


class ChallengeReq(BaseModel):
    service: str = Field(..., min_length=1, max_length=120)
    description: str = Field(..., min_length=3, max_length=4000)
    email: str = Field("", max_length=255)
    fairness: str = Field("", max_length=200)


@router.post("/challenge")
def submit_challenge(req: ChallengeReq, db: Session = Depends(get_db)):
    """Open a human-in-the-loop oversight case from the public Citizen Portal."""
    case_ref = f"CASE-{uuid.uuid4().hex[:6].upper()}"
    reason = f"{req.service}: {req.description}".strip()
    if len(reason) > 200:
        reason = reason[:197] + "..."
    detail_bits = []
    if req.email:
        detail_bits.append(f"email={req.email[:80]}")
    if req.fairness:
        detail_bits.append(f"fairness={req.fairness[:80]}")
    if detail_bits:
        # fold contact into reason tail if room
        tail = " | " + "; ".join(detail_bits)
        if len(reason) + len(tail) <= 200:
            reason = reason + tail

    c = OversightCase(
        case_ref=case_ref,
        model_id="CITIZEN-PORTAL",
        reason=reason,
        state="OPEN",
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    try:
        append_audit(
            db,
            "CITIZEN_CHALLENGE",
            {"case": case_ref, "service": req.service[:80]},
            classification="GOVERNANCE",
            actor_class="CITIZEN",
        )
    except Exception:
        pass
    return {
        "case_ref": c.case_ref,
        "state": c.state,
        "message": "Challenge received. Keep your case number to check status.",
    }


@router.get("/cases/{case_ref}")
def get_case(case_ref: str, db: Session = Depends(get_db)):
    """Public status lookup for a citizen case reference."""
    ref = case_ref.strip().upper()
    if not re.match(r"^[A-Z0-9\-]{4,40}$", ref):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid case reference")
    c = db.execute(select(OversightCase).where(OversightCase.case_ref == ref)).scalar_one_or_none()
    if not c:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "case not found")
    return {
        "case_ref": c.case_ref,
        "state": c.state,
        "model_id": c.model_id,
        "reason": c.reason,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "assigned_to": c.assigned_to or None,
        "resolution": (c.resolution or "")[:500] or None,
    }


@router.get("/health")
def citizen_health():
    return {"surface": "citizen", "status": "live", "core": "platform-core"}
