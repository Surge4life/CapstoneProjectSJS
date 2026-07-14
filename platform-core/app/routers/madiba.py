"""MADIBA — capital allocation: pool returns, recycle 55% to SETHS (loop-closer)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timezone
from app.db.session import get_db
from app.db.models import CapitalCycle, Learner, TSProject, SaaSClient, InstitutionalMilestone
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

# ───────────────────────── Series A trigger tracking ─────────────────────────
# Document 00 §13 / live-site-confirmed 4 conditions. Three are derived from real,
# already-existing transactional data; the fourth (govt LOI) has no natural
# transactional trace and is recorded manually via /madiba/milestones.

SERIES_A_PLACEMENT_TARGET = 100

@router.get("/series-a-status")
def series_a_status(db: Session = Depends(get_db)):
    placements = db.execute(select(func.count(Learner.id)).where(Learner.status == "PLACED")).scalar() or 0
    paying_clients = db.execute(select(func.count(SaaSClient.id))).scalar() or 0
    ts_operational = db.execute(select(func.count(TSProject.id)).where(TSProject.active == True)).scalar() or 0  # noqa: E712
    loi = db.execute(select(InstitutionalMilestone).where(InstitutionalMilestone.key == "GOVT_LOI_SIGNED")).scalar_one_or_none()

    triggers = {
        "verified_placements_100plus": {"target": SERIES_A_PLACEMENT_TARGET, "actual": placements,
                                         "met": placements >= SERIES_A_PLACEMENT_TARGET},
        "udoc_clients_3plus": {"target": 3, "actual": paying_clients, "met": paying_clients >= 3},
        "govt_loi_signed": {"met": bool(loi and loi.achieved),
                            "evidence_note": loi.evidence_note if loi else ""},
        "ts_first_project_operational": {"target": 1, "actual": ts_operational, "met": ts_operational >= 1},
    }
    all_met = all(t["met"] for t in triggers.values())
    return {"triggers": triggers, "all_conditions_met": all_met,
            "note": "udoc_clients_3plus counts registered SaaS clients; this schema does not yet "
                    "separately track paid vs. trial tier — treat as a lower bound, not confirmation "
                    "of paying status, until billing state is modelled."}

class MilestoneReq(BaseModel):
    achieved: bool
    evidence_note: str = ""

@router.post("/milestones/{key}")
def set_milestone(key: str, req: MilestoneReq, db: Session = Depends(get_db),
                   _=Depends(require_role("admin"))):
    m = db.execute(select(InstitutionalMilestone).where(InstitutionalMilestone.key == key)).scalar_one_or_none()
    if not m:
        m = InstitutionalMilestone(key=key)
        db.add(m)
    m.achieved = req.achieved
    m.evidence_note = req.evidence_note
    m.achieved_at = datetime.now(timezone.utc) if req.achieved else None
    db.commit()
    return {"key": key, "achieved": m.achieved, "evidence_note": m.evidence_note}
