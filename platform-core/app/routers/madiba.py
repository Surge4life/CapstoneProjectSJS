"""MADIBA — capital allocation: pool returns, recycle 55% to SETHS (loop-closer)."""
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import CapitalCycle
from app.core.dependencies import require_role
from app.services import analytics_engine as ae

router = APIRouter(prefix="/madiba", tags=["MADIBA"])

class AllocateReq(BaseModel):
    month: int
    total_inflow: float
    dfi_pct: float = 0.20
    reserve_pct: float = 0.15
    holdings_pct: float = 0.10

@router.post("/allocate")
def allocate(req: AllocateReq, db: Session = Depends(get_db), _=Depends(require_role("operator", "admin"))):
    recycle_pct = 1 - req.dfi_pct - req.reserve_pct - req.holdings_pct
    dfi = req.total_inflow * req.dfi_pct
    reserve = req.total_inflow * req.reserve_pct
    opex = req.total_inflow * req.holdings_pct
    recycled = req.total_inflow - dfi - reserve - opex
    c = CapitalCycle(month=req.month, total_inflow=req.total_inflow, dfi_servicing=dfi,
                     reserve=reserve, holdings_opex=opex, recycled_to_seths=recycled)
    db.add(c); db.commit(); db.refresh(c)
    period = f"2026-{req.month:02d}"
    ae.record(db, "MADIBA", "ALLOCATE", metric_name="inflow", metric_value=req.total_inflow, period=period)
    ae.record(db, "MADIBA", "RECYCLE", metric_name="recycled", metric_value=recycled, period=period)
    return {"month": req.month, "recycled_to_seths": round(recycled, 2),
            "recycle_pct": round(recycle_pct, 3), "pillar2_ok": recycle_pct > 0.5}

@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    rows = db.execute(select(CapitalCycle).order_by(CapitalCycle.month)).scalars().all()
    return {"cycles": len(rows),
            "cumulative_recycled": round(sum(c.recycled_to_seths for c in rows), 2),
            "series": [{"month": c.month, "inflow": c.total_inflow,
                        "recycled": c.recycled_to_seths} for c in rows]}
