"""SETHS — workforce reintegration: enrol, complete, place learners."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Learner
from app.core.dependencies import require_role
from app.services import analytics_engine as ae
import uuid

router = APIRouter(prefix="/seths", tags=["SETHS"])

class EnrolReq(BaseModel):
    qualification: str = "Digital Operations & AI Literacy"
    nqf_level: int = 5
    count: int = 1

@router.post("/enrol")
def enrol(req: EnrolReq, db: Session = Depends(get_db), _=Depends(require_role("operator", "admin"))):
    created = []
    for _i in range(req.count):
        l = Learner(ref=f"SETHS-{uuid.uuid4().hex[:8]}", qualification=req.qualification, nqf_level=req.nqf_level)
        db.add(l); created.append(l.ref)
    db.commit()
    ae.record(db, "SETHS", "ENROL", metric_name="enrolled", metric_value=len(created))
    return {"enrolled": len(created), "refs": created[:20]}

@router.post("/{ref}/advance")
def advance(ref: str, monthly_value: float = 12000.0, db: Session = Depends(get_db),
            _=Depends(require_role("operator", "admin"))):
    l = db.execute(select(Learner).where(Learner.ref == ref)).scalar_one_or_none()
    if not l:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "learner not found")
    l.status = {"ENROLLED": "COMPLETED", "COMPLETED": "PLACED"}.get(l.status, l.status)
    if l.status == "PLACED":
        l.monthly_value = monthly_value
    db.commit()
    if l.status == "PLACED":
        ae.record(db, "SETHS", "PLACE", entity_ref=ref, metric_name="placed", metric_value=1)
        ae.record(db, "SETHS", "OUTPUT", entity_ref=ref, metric_name="monthly_value", metric_value=l.monthly_value)
    return {"ref": ref, "status": l.status, "monthly_value": l.monthly_value}

@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    total = db.execute(select(func.count(Learner.id))).scalar() or 0
    placed = db.execute(select(func.count(Learner.id)).where(Learner.status == "PLACED")).scalar() or 0
    completed = db.execute(select(func.count(Learner.id)).where(Learner.status == "COMPLETED")).scalar() or 0
    output = db.execute(select(func.coalesce(func.sum(Learner.monthly_value), 0.0))).scalar() or 0.0
    return {"total": total, "completed": completed, "placed": placed,
            "placement_rate": round(placed / total, 3) if total else 0.0,
            "monthly_economic_output": output}
