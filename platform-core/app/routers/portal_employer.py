"""Employer Portal API — register, post opportunities, review applicants, offer → placement."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.db.session import get_db
from app.db.models import Employer, Opportunity, Application, Student, Employee
from app.core.dependencies import current_user
from app.services import analytics_engine as ae
import uuid

router = APIRouter(prefix="/portal/employer", tags=["Portal · Employer"])

class EmployerReg(BaseModel):
    org_name: str
    contact_email: EmailStr
    sector: str = ""
    bbbee_level: int = 4

@router.post("/register")
def register(req: EmployerReg, db: Session = Depends(get_db)):
    e = Employer(org_name=req.org_name, contact_email=req.contact_email,
                 sector=req.sector, bbbee_level=req.bbbee_level, verified=True)
    db.add(e); db.commit(); db.refresh(e)
    return {"employer_id": e.id, "org_name": e.org_name, "verified": e.verified}

class OppReq(BaseModel):
    employer_id: int
    title: str
    description: str = ""
    sector: str = ""
    positions: int = 1
    monthly_stipend: float = 0.0

@router.post("/opportunities")
def post_opportunity(req: OppReq, db: Session = Depends(get_db), _=Depends(current_user)):
    if not db.get(Employer, req.employer_id): raise HTTPException(404, "employer not found")
    o = Opportunity(**req.model_dump())
    db.add(o); db.commit(); db.refresh(o)
    ae.record(db, "SETHS", "OPPORTUNITY_POSTED", entity_ref=f"OPP-{o.id}",
              metric_name="opportunities", metric_value=req.positions)
    return {"id": o.id, "title": o.title, "status": o.status}

@router.get("/{employer_id}/opportunities")
def my_opportunities(employer_id: int, db: Session = Depends(get_db)):
    rows = db.execute(select(Opportunity).where(Opportunity.employer_id == employer_id)).scalars().all()
    return [{"id": o.id, "title": o.title, "positions": o.positions, "status": o.status} for o in rows]

@router.get("/opportunities/{opportunity_id}/applicants")
def applicants(opportunity_id: int, db: Session = Depends(get_db), _=Depends(current_user)):
    apps = db.execute(select(Application).where(Application.opportunity_id == opportunity_id)).scalars().all()
    out = []
    for a in apps:
        s = db.get(Student, a.student_id)
        out.append({"application_id": a.id, "student_ref": s.student_ref if s else "—",
                    "full_name": s.full_name if s else "—", "progress_pct": s.progress_pct if s else 0,
                    "state": a.state})
    return out

@router.post("/applications/{application_id}/offer")
def make_offer(application_id: int, db: Session = Depends(get_db), _=Depends(current_user)):
    a = db.get(Application, application_id)
    if not a: raise HTTPException(404, "application not found")
    a.state = "PLACED"
    s = db.get(Student, a.student_id); o = db.get(Opportunity, a.opportunity_id)
    if s: s.status = "PLACED"
    # Placement creates an Employee record (the student becomes an employee — loop step)
    emp = Employee(employee_ref=f"EMP-{uuid.uuid4().hex[:8]}", full_name=s.full_name if s else "",
                   email=s.email if s else "", division="TS", role=o.title if o else "",
                   monthly_salary=o.monthly_stipend if o else 0.0)
    db.add(emp)
    if o:
        filled = db.execute(select(Application).where(Application.opportunity_id == o.id,
                 Application.state == "PLACED")).scalars().all()
        if len(filled) + 1 >= o.positions: o.status = "FILLED"
    db.commit(); db.refresh(emp)
    ae.record(db, "SETHS", "PLACE", entity_ref=s.student_ref if s else "", metric_name="placed", metric_value=1)
    if s: ae.record(db, "SETHS", "OUTPUT", entity_ref=s.student_ref, metric_name="monthly_value",
                    metric_value=o.monthly_stipend if o else 0.0)
    return {"application_id": application_id, "state": "PLACED", "employee_ref": emp.employee_ref}
