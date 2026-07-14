"""TS Industries project submission + partner-build application API (TS .apk)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import ProjectSubmission, PartnerApplication
from app.core.dependencies import current_user
from app.services import analytics_engine as ae
import uuid

router = APIRouter(prefix="/ts/submit", tags=["TS submissions"])
STAGES = ["SUBMITTED", "SCREENING", "APPROVED", "IN_BUILD", "DECLINED"]

class SubmitReq(BaseModel):
    submitter_name: str
    submitter_type: str = "PRIVATE"
    sector: str = ""
    title: str
    description: str = ""
    capex_estimate: float = 0.0

@router.post("/project")
def submit_project(req: SubmitReq, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    p = ProjectSubmission(submission_ref=f"SUB-{uuid.uuid4().hex[:8]}", **req.model_dump())
    db.add(p); db.commit(); db.refresh(p)
    ae.record(db, "TS", "SUBMISSION", entity_ref=p.submission_ref,
              metric_name="pipeline_capex", metric_value=req.capex_estimate)
    return {"submission_ref": p.submission_ref, "stage": p.stage}

@router.get("/project/{ref}")
def track(ref: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    p = db.execute(select(ProjectSubmission).where(ProjectSubmission.submission_ref == ref)).scalar_one_or_none()
    if not p: raise HTTPException(404, "submission not found")
    return {"submission_ref": p.submission_ref, "title": p.title, "stage": p.stage,
            "sector": p.sector, "capex_estimate": p.capex_estimate}

@router.post("/project/{ref}/advance")
def advance(ref: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    p = db.execute(select(ProjectSubmission).where(ProjectSubmission.submission_ref == ref)).scalar_one_or_none()
    if not p: raise HTTPException(404, "submission not found")
    i = STAGES.index(p.stage)
    if i < 3: p.stage = STAGES[i + 1]
    db.commit()
    return {"submission_ref": ref, "stage": p.stage}

class PartnerReq(BaseModel):
    org_name: str
    capability: str = ""
    sector: str = ""
    bbbee_level: int = 4

@router.post("/partner")
def apply_partner(req: PartnerReq, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    a = PartnerApplication(app_ref=f"PTR-{uuid.uuid4().hex[:8]}", **req.model_dump())
    db.add(a); db.commit(); db.refresh(a)
    ae.record(db, "TS", "PARTNER_APP", entity_ref=a.app_ref, metric_name="partner_apps", metric_value=1)
    return {"app_ref": a.app_ref, "state": a.state}

@router.get("/projects")
def all_projects(db: Session = Depends(get_db), _: dict = Depends(current_user)):
    rows = db.execute(select(ProjectSubmission).order_by(ProjectSubmission.id.desc())).scalars().all()
    return [{"ref": p.submission_ref, "title": p.title, "type": p.submitter_type,
             "sector": p.sector, "capex": p.capex_estimate, "stage": p.stage} for p in rows]
