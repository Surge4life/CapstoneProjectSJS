"""TS Industries — production SPVs absorbing SETHS-placed workers."""
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import TSProject
from app.core.dependencies import require_role
from app.services import analytics_engine as ae
import uuid

router = APIRouter(prefix="/ts", tags=["TS Industries"])

class ProjectReq(BaseModel):
    sector: str
    name: str
    workers_deployed: int = 0
    monthly_revenue: float = 0.0
    operating_margin: float = 0.30

@router.post("/projects")
def deploy(req: ProjectReq, db: Session = Depends(get_db), _=Depends(require_role("operator", "admin"))):
    p = TSProject(spv_id=f"SPV-{req.sector}-{uuid.uuid4().hex[:8]}", **req.model_dump())
    db.add(p); db.commit(); db.refresh(p)
    ae.record(db, "TS", "DEPLOY_SPV", entity_ref=p.spv_id, metric_name="workers", metric_value=p.workers_deployed)
    ae.record(db, "TS", "REVENUE", entity_ref=p.spv_id, metric_name="revenue", metric_value=p.monthly_revenue)
    ae.record(db, "TS", "PROFIT", entity_ref=p.spv_id, metric_name="profit", metric_value=p.monthly_revenue*p.operating_margin)
    return {"spv_id": p.spv_id, "sector": p.sector, "active": p.active}

@router.get("/projects")
def projects(db: Session = Depends(get_db)):
    rows = db.execute(select(TSProject)).scalars().all()
    return [{"spv_id": p.spv_id, "sector": p.sector, "name": p.name,
             "workers": p.workers_deployed, "monthly_revenue": p.monthly_revenue,
             "operating_margin": p.operating_margin} for p in rows]

@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    rows = db.execute(select(TSProject)).scalars().all()
    profit = sum(p.monthly_revenue * p.operating_margin for p in rows)
    return {"projects": len(rows), "workers_absorbed": sum(p.workers_deployed for p in rows),
            "monthly_operating_profit": round(profit, 2)}
