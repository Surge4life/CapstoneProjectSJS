"""SETHS — workforce reintegration: enrol, complete, place learners."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, text
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.db.session import get_db, engine
from app.db.models import Learner
from app.core.dependencies import require_role
from app.services import analytics_engine as ae
import uuid

router = APIRouter(prefix="/seths", tags=["SETHS"])

class EnrolReq(BaseModel):
    qualification: str = "Digital Operations & AI Literacy"
    nqf_level: int = 5
    count: int = 1


def _heal_learner_cols():
    """Add missing Capstone columns; widen cohort so COHORT_1 fits (was VARCHAR(4))."""
    with engine.begin() as conn:
        existing = {r[0] for r in conn.execute(text(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'seths_learners'"
        )).fetchall()}
        if not existing:
            return
        cols = [
            ("cohort", "VARCHAR(24)", "'COHORT_1'"),
            ("stream", "VARCHAR(24)", "'DIGITAL_OPERATIONS'"),
            ("cetcte_stage", "VARCHAR(24)", "'STABILISATION'"),
            ("self_affirmation_json", "TEXT", "'{}'"),
            ("monthly_value", "DOUBLE PRECISION", "0"),
        ]
        for name, typ, default in cols:
            if name not in existing:
                try:
                    conn.execute(text(
                        f'ALTER TABLE seths_learners ADD COLUMN IF NOT EXISTS "{name}" {typ} DEFAULT {default}'
                    ))
                except Exception:
                    pass
        try:
            conn.execute(text(
                "ALTER TABLE seths_learners ALTER COLUMN cohort TYPE VARCHAR(24)"
            ))
        except Exception:
            pass


@router.post("/enrol")
def enrol(req: EnrolReq, db: Session = Depends(get_db), _=Depends(require_role("operator", "admin"))):
    count = max(1, min(int(req.count or 1), 20))
    def _create():
        created = []
        for _i in range(count):
            l = Learner(ref=f"SETHS-{uuid.uuid4().hex[:8]}", qualification=req.qualification, nqf_level=req.nqf_level)
            db.add(l); created.append(l.ref)
        db.commit()
        return created
    try:
        created = _create()
    except Exception:
        db.rollback()
        _heal_learner_cols()
        try:
            created = _create()
        except Exception as second:
            db.rollback()
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                f"enrol failed (schema?): {str(second)[:240]}")
    ae.record(db, "SETHS", "ENROL", metric_name="enrolled", metric_value=len(created))
    return {"enrolled": len(created), "refs": created[:20]}


@router.post("/{ref}/advance")
def advance(ref: str, monthly_value: float = 12000.0, db: Session = Depends(get_db),
            _=Depends(require_role("operator", "admin"))):
    """Advance learner toward placement.

    Capstone demo path (one click):
      ENROLLED → PLACED
      COMPLETED → PLACED  (legacy mid-state still supported)

    PLACED sets monthly_value for economic-output metrics and unlocks
    TS assign-worker (FK-backed SETHS→TS loop).
    """
    l = db.execute(select(Learner).where(Learner.ref == ref)).scalar_one_or_none()
    if not l:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "learner not found")
    prev = l.status
    # One-step to PLACED for Capstone loop UX (admin / divisions guided path)
    if l.status in ("ENROLLED", "COMPLETED"):
        l.status = "PLACED"
        l.monthly_value = monthly_value
    elif l.status == "PLACED":
        # idempotent refresh of value
        l.monthly_value = monthly_value
    db.commit()
    if l.status == "PLACED" and prev != "PLACED":
        ae.record(db, "SETHS", "PLACE", entity_ref=ref, metric_name="placed", metric_value=1)
        ae.record(db, "SETHS", "OUTPUT", entity_ref=ref, metric_name="monthly_value", metric_value=l.monthly_value)
    return {"ref": ref, "status": l.status, "previous": prev, "monthly_value": l.monthly_value}


@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    total = db.execute(select(func.count(Learner.id))).scalar() or 0
    placed = db.execute(select(func.count(Learner.id)).where(Learner.status == "PLACED")).scalar() or 0
    completed = db.execute(select(func.count(Learner.id)).where(Learner.status == "COMPLETED")).scalar() or 0
    output = db.execute(select(func.coalesce(func.sum(Learner.monthly_value), 0.0))).scalar() or 0.0
    return {"total": total, "completed": completed, "placed": placed,
            "placement_rate": round(placed / total, 3) if total else 0.0,
            "monthly_economic_output": output}


@router.get("/learners")
def list_learners(limit: int = 25, status: Optional[str] = None, db: Session = Depends(get_db),
                  _=Depends(require_role("operator", "admin"))):
    """Roster for divisions operator surface — newest first, capped for free-tier honesty."""
    lim = min(max(limit, 1), 50)
    if status:
        q = select(Learner).where(Learner.status == status.upper()).order_by(Learner.id.desc()).limit(lim)
    else:
        q = select(Learner).order_by(Learner.id.desc()).limit(lim)
    rows = db.execute(q).scalars().all()
    out = []
    for l in rows:
        out.append({
            "ref": l.ref,
            "status": l.status,
            "qualification": getattr(l, "qualification", None) or "",
            "nqf_level": getattr(l, "nqf_level", None),
            "cohort": getattr(l, "cohort", None) or "",
            "stream": getattr(l, "stream", None) or "",
            "monthly_value": getattr(l, "monthly_value", None) or 0,
        })
    return {"count": len(out), "learners": out}


@router.get("/learners/{ref}")
def get_learner(ref: str, db: Session = Depends(get_db), _=Depends(require_role("operator", "admin"))):
    l = db.execute(select(Learner).where(Learner.ref == ref)).scalar_one_or_none()
    if not l:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "learner not found")
    return {
        "ref": l.ref,
        "status": l.status,
        "qualification": getattr(l, "qualification", None) or "",
        "nqf_level": getattr(l, "nqf_level", None),
        "cohort": getattr(l, "cohort", None) or "",
        "stream": getattr(l, "stream", None) or "",
        "cetcte_stage": getattr(l, "cetcte_stage", None) or "",
        "monthly_value": getattr(l, "monthly_value", None) or 0,
    }
