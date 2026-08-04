"""MADIBA — capital allocation: pool returns, recycle ≥50% to SETHS (loop-closer).

Honesty: ledger numbers are only what was written via /madiba/allocate (or historical
rows still in Neon). They are NOT claims of real institutional funds under management.
Use POST /madiba/reset-ledger (admin) to clear fabricated / theatre cycles.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, delete
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.db.session import get_db
from app.db.models import CapitalCycle, Learner, TSProject, SaaSClient, InstitutionalMilestone, DivisionRecord
from app.core.dependencies import require_role
from app.services import analytics_engine as ae

router = APIRouter(prefix="/madiba", tags=["MADIBA"])

# Capstone: hard ceiling on single allocate to discourage theatre-scale entries
MAX_DEMO_INFLOW = 5_000_000.0


class AllocateReq(BaseModel):
    month: int = Field(ge=1, le=12)
    total_inflow: float = Field(gt=0, le=MAX_DEMO_INFLOW)
    dfi_pct: float = 0.20
    reserve_pct: float = 0.15
    holdings_pct: float = 0.10
    note: str = "capstone_demo_ledger"


@router.post("/allocate")
def allocate(req: AllocateReq, db: Session = Depends(get_db), _=Depends(require_role("operator", "admin"))):
    """Write one CapitalCycle row. Demo ledger entry — not bank money."""
    recycle_pct = 1 - req.dfi_pct - req.reserve_pct - req.holdings_pct
    if recycle_pct <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "split leaves no recycle share")
    dfi = req.total_inflow * req.dfi_pct
    reserve = req.total_inflow * req.reserve_pct
    opex = req.total_inflow * req.holdings_pct
    recycled = req.total_inflow - dfi - reserve - opex
    c = CapitalCycle(month=req.month, total_inflow=req.total_inflow, dfi_servicing=dfi,
                     reserve=reserve, holdings_opex=opex, recycled_to_seths=recycled)
    db.add(c); db.commit(); db.refresh(c)
    period = f"2026-{req.month:02d}"
    ae.record(db, "MADIBA", "ALLOCATE", metric_name="inflow", metric_value=req.total_inflow, period=period,
              meta={"note": req.note, "demo_ledger": True})
    ae.record(db, "MADIBA", "RECYCLE", metric_name="recycled", metric_value=recycled, period=period,
              meta={"note": req.note, "demo_ledger": True})
    return {"month": req.month, "recycled_to_seths": round(recycled, 2),
            "recycle_pct": round(recycle_pct, 3), "pillar2_ok": recycle_pct > 0.5,
            "honesty": "demo_ledger_entry_not_institutional_AUM"}


@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    """Ledger totals from CapitalCycle only. Zero when empty. Not AUM."""
    rows = db.execute(select(CapitalCycle).order_by(CapitalCycle.month)).scalars().all()
    total_inflow = round(sum(c.total_inflow for c in rows), 2)
    cumulative = round(sum(c.recycled_to_seths for c in rows), 2)
    return {
        "cycles": len(rows),
        "total_inflow": total_inflow,
        "cumulative_recycled": cumulative,
        "recycle_ratio": round(cumulative / total_inflow, 3) if total_inflow else 0.0,
        "series": [{"month": c.month, "inflow": c.total_inflow,
                    "recycled": c.recycled_to_seths} for c in rows],
        "source": "capital_cycle_ledger",
        "honesty": "ledger_only_not_institutional_funds",
        "note": "Figures are sum of /madiba/allocate rows (or legacy theatre rows until reset). "
                "POST /madiba/reset-ledger clears them. Prefer zeros over fiction.",
    }


@router.post("/reset-ledger")
def reset_ledger(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    """Admin: delete all CapitalCycle rows + MADIBA DivisionRecord analytics (theatre purge)."""
    n_cycles = db.execute(select(func.count(CapitalCycle.id))).scalar() or 0
    n_events = db.execute(select(func.count(DivisionRecord.id)).where(
        DivisionRecord.division == "MADIBA")).scalar() or 0
    db.execute(delete(CapitalCycle))
    db.execute(delete(DivisionRecord).where(DivisionRecord.division == "MADIBA"))
    db.commit()
    return {
        "cleared_cycles": n_cycles,
        "cleared_division_records": n_events,
        "metrics_now": {"cycles": 0, "cumulative_recycled": 0, "total_inflow": 0},
        "honesty": "ledger_empty_after_reset",
    }


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
