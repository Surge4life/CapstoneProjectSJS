"""UDOC human-in-the-loop oversight — open/assign/resolve/override cases (Pillar VIII)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import OversightCase
from app.core.dependencies import require_role
from app.services.audit_writer import append_audit
import uuid

router = APIRouter(prefix="/oversight", tags=["UDOC oversight"])

class CaseReq(BaseModel):
    model_id: str
    reason: str

@router.post("/cases")
def open_case(req: CaseReq, db: Session = Depends(get_db), user=Depends(require_role("operator", "auditor", "admin"))):
    c = OversightCase(case_ref=f"COB-{uuid.uuid4().hex[:8]}", model_id=req.model_id, reason=req.reason)
    db.add(c); db.commit(); db.refresh(c)
    append_audit(db, "OVERSIGHT_OPEN", {"case": c.case_ref, "model": req.model_id}, classification="GOVERNANCE")
    return {"case_ref": c.case_ref, "state": c.state}

@router.post("/cases/{case_ref}/resolve")
def resolve(case_ref: str, resolution: str, override: bool = False,
            db: Session = Depends(get_db), user=Depends(require_role("auditor", "admin"))):
    c = db.execute(select(OversightCase).where(OversightCase.case_ref == case_ref)).scalar_one_or_none()
    if not c:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "case not found")
    c.state = "OVERRIDDEN" if override else "RESOLVED"
    c.resolution = resolution; c.assigned_to = user.get("sub", "")
    db.commit()
    append_audit(db, "OVERSIGHT_RESOLVE", {"case": case_ref, "state": c.state, "override": override},
                 classification="GOVERNANCE", actor_class=user.get("role", "auditor"))
    return {"case_ref": case_ref, "state": c.state}

@router.get("/cases")
def list_cases(db: Session = Depends(get_db), _=Depends(require_role("operator", "auditor", "admin"))):
    rows = db.execute(select(OversightCase).order_by(OversightCase.id.desc())).scalars().all()
    return [{"case_ref": c.case_ref, "model_id": c.model_id, "reason": c.reason,
             "state": c.state, "assigned_to": c.assigned_to} for c in rows]
