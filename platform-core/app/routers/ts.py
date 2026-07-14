"""TS Industries — production SPVs absorbing SETHS-placed workers."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import TSProject, TSWorkerAssignment, Learner
from app.core.dependencies import require_role
from app.services import analytics_engine as ae
import uuid

router = APIRouter(prefix="/ts", tags=["TS Industries"])

SUBSIDIARIES = ("ENERGY", "CONSTRUCTION", "AGRITECH", "WATER",
                "DIGITAL_INFRASTRUCTURE", "MANUFACTURING", "LOGISTICS")


class ProjectReq(BaseModel):
    sector: str
    name: str
    subsidiary: str = "ENERGY"
    equity_pct: float = 0.30
    workers_deployed: int = 0
    monthly_revenue: float = 0.0
    operating_margin: float = 0.30

@router.post("/projects")
def deploy(req: ProjectReq, db: Session = Depends(get_db), _=Depends(require_role("operator", "admin"))):
    if req.subsidiary not in SUBSIDIARIES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"subsidiary must be one of {SUBSIDIARIES}")
    if not 0.20 <= req.equity_pct <= 0.60:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "equity_pct must be 0.20-0.60 per the SPV co-ownership model")
    p = TSProject(spv_id=f"SPV-{req.sector}-{uuid.uuid4().hex[:8]}", **req.model_dump())
    db.add(p); db.commit(); db.refresh(p)
    ae.record(db, "TS", "DEPLOY_SPV", entity_ref=p.spv_id, metric_name="workers", metric_value=p.workers_deployed)
    ae.record(db, "TS", "REVENUE", entity_ref=p.spv_id, metric_name="revenue", metric_value=p.monthly_revenue)
    ae.record(db, "TS", "PROFIT", entity_ref=p.spv_id, metric_name="profit", metric_value=p.monthly_revenue*p.operating_margin)
    return {"spv_id": p.spv_id, "sector": p.sector, "subsidiary": p.subsidiary, "equity_pct": p.equity_pct, "active": p.active}

@router.get("/subsidiaries")
def subsidiaries():
    return {"subsidiaries": list(SUBSIDIARIES)}

class AssignWorkerReq(BaseModel):
    learner_ref: str
    role: str = ""
    monthly_wage: float = 0.0

@router.post("/projects/{spv_id}/assign-worker")
def assign_worker(spv_id: str, req: AssignWorkerReq, db: Session = Depends(get_db),
                   _=Depends(require_role("operator", "admin"))):
    """Real FK-backed placement: only a Learner already in PLACED status can
    be assigned, closing the SETHS→TS loop with an actual relationship
    instead of two independent counters."""
    project = db.execute(select(TSProject).where(TSProject.spv_id == spv_id)).scalar_one_or_none()
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "SPV not found")
    learner = db.execute(select(Learner).where(Learner.ref == req.learner_ref)).scalar_one_or_none()
    if not learner:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "learner not found")
    if learner.status != "PLACED":
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                             f"learner status is {learner.status}, must be PLACED before TS assignment")
    existing = db.execute(select(TSWorkerAssignment).where(
        TSWorkerAssignment.learner_pk == learner.id, TSWorkerAssignment.ts_project_pk == project.id
    )).scalar_one_or_none()
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "learner already assigned to this SPV")
    a = TSWorkerAssignment(ts_project_pk=project.id, learner_pk=learner.id,
                           role=req.role, monthly_wage=req.monthly_wage or learner.monthly_value)
    db.add(a)
    project.workers_deployed = db.execute(
        select(func.count(TSWorkerAssignment.id)).where(TSWorkerAssignment.ts_project_pk == project.id)
    ).scalar() + 1
    db.commit()
    ae.record(db, "TS", "WORKER_ASSIGNED", entity_ref=spv_id, metric_name="workers", metric_value=project.workers_deployed)
    return {"spv_id": spv_id, "learner_ref": req.learner_ref, "workers_deployed": project.workers_deployed}

@router.get("/projects/{spv_id}/workers")
def project_workers(spv_id: str, db: Session = Depends(get_db)):
    project = db.execute(select(TSProject).where(TSProject.spv_id == spv_id)).scalar_one_or_none()
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "SPV not found")
    rows = db.execute(select(TSWorkerAssignment).where(TSWorkerAssignment.ts_project_pk == project.id)).scalars().all()
    return [{"learner_ref": a.learner.ref, "role": a.role, "monthly_wage": a.monthly_wage} for a in rows]

@router.get("/projects")
def projects(db: Session = Depends(get_db)):
    rows = db.execute(select(TSProject)).scalars().all()
    return [{"spv_id": p.spv_id, "sector": p.sector, "subsidiary": p.subsidiary, "equity_pct": p.equity_pct,
             "name": p.name, "workers": p.workers_deployed, "monthly_revenue": p.monthly_revenue,
             "operating_margin": p.operating_margin} for p in rows]

@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    rows = db.execute(select(TSProject)).scalars().all()
    profit = sum(p.monthly_revenue * p.operating_margin for p in rows)
    by_subsidiary = {}
    for p in rows:
        by_subsidiary.setdefault(p.subsidiary, {"projects": 0, "workers": 0})
        by_subsidiary[p.subsidiary]["projects"] += 1
        by_subsidiary[p.subsidiary]["workers"] += p.workers_deployed
    return {"projects": len(rows), "workers_absorbed": sum(p.workers_deployed for p in rows),
            "monthly_operating_profit": round(profit, 2), "by_subsidiary": by_subsidiary}
