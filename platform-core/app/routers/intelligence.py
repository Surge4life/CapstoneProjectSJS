"""Cross-division intelligence — the closed-loop snapshot (SETHS→TS→UDOC→MADIBA)."""
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Learner, TSProject, CapitalCycle, Decision
from app.core.dependencies import current_user

router = APIRouter(prefix="/intelligence", tags=["intelligence"])

@router.get("/loop-snapshot")
def loop_snapshot(db: Session = Depends(get_db), _: dict = Depends(current_user)):
    placed = db.execute(select(func.count(Learner.id)).where(Learner.status == "PLACED")).scalar() or 0
    ts = db.execute(select(TSProject)).scalars().all()
    ts_profit = sum(p.monthly_revenue * p.operating_margin for p in ts)
    recycled = db.execute(select(func.coalesce(func.sum(CapitalCycle.recycled_to_seths), 0.0))).scalar() or 0.0
    decisions = db.execute(select(func.count(Decision.id))).scalar() or 0
    return {"seths_placed": placed, "ts_monthly_profit": round(ts_profit, 2),
            "madiba_cumulative_recycled": round(recycled, 2), "udoc_decisions": decisions,
            "loop": "SETHS→TS→UDOC→MADIBA→SETHS"}
