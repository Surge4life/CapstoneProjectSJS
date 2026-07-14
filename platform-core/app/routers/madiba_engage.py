"""MADIBA investor engagement + project-update API (MADIBA .apk)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import InvestmentEngagement
from app.core.dependencies import current_user
from app.services import analytics_engine as ae
import uuid

router = APIRouter(prefix="/madiba/engage", tags=["MADIBA engagements"])
STAGES = ["INTRODUCED", "DD", "TERM_SHEET", "COMMITTED", "FUNDED"]

class EngageReq(BaseModel):
    investor_name: str
    investor_type: str = "INSTITUTIONAL"
    instrument: str = "blended"
    indicated_amount: float = 0.0

@router.post("")
def create(req: EngageReq, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    e = InvestmentEngagement(engagement_ref=f"ENG-{uuid.uuid4().hex[:8]}", **req.model_dump())
    db.add(e); db.commit(); db.refresh(e)
    ae.record(db, "MADIBA", "ENGAGEMENT", entity_ref=e.engagement_ref,
              metric_name="pipeline", metric_value=req.indicated_amount)
    return {"engagement_ref": e.engagement_ref, "stage": e.stage}

@router.post("/{ref}/advance")
def advance(ref: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    e = db.execute(select(InvestmentEngagement).where(InvestmentEngagement.engagement_ref == ref)).scalar_one_or_none()
    if not e: raise HTTPException(404, "engagement not found")
    i = STAGES.index(e.stage)
    if i < len(STAGES) - 1: e.stage = STAGES[i + 1]
    db.commit()
    if e.stage == "FUNDED":
        ae.record(db, "MADIBA", "FUNDED", entity_ref=ref, metric_name="committed", metric_value=e.indicated_amount)
    return {"engagement_ref": ref, "stage": e.stage}

@router.get("/pipeline")
def pipeline(db: Session = Depends(get_db), _: dict = Depends(current_user)):
    rows = db.execute(select(InvestmentEngagement).order_by(InvestmentEngagement.id.desc())).scalars().all()
    by_stage = {}
    for s in STAGES:
        by_stage[s] = sum(1 for e in rows if e.stage == s)
    total = sum(e.indicated_amount for e in rows)
    committed = sum(e.indicated_amount for e in rows if e.stage in ("COMMITTED", "FUNDED"))
    return {"engagements": len(rows), "by_stage": by_stage,
            "indicated_total": total, "committed_total": committed,
            "list": [{"ref": e.engagement_ref, "investor": e.investor_name, "type": e.investor_type,
                      "instrument": e.instrument, "amount": e.indicated_amount, "stage": e.stage} for e in rows]}
