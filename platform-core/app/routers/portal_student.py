"""Student Portal API (SETHS) — self-service: register, track progress, browse & apply."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.db.session import get_db
from app.db.models import Student, Opportunity, Application, Employer
from app.core.dependencies import current_user
from app.services import analytics_engine as ae
import uuid

router = APIRouter(prefix="/portal/student", tags=["Portal · Student"])

class StudentReg(BaseModel):
    full_name: str
    email: EmailStr
    qualification: str = "Software Developer 118707"
    nqf_level: int = 5

@router.post("/register")
def register(req: StudentReg, db: Session = Depends(get_db)):
    s = Student(student_ref=f"STU-{uuid.uuid4().hex[:8]}", full_name=req.full_name,
                email=req.email, qualification=req.qualification, nqf_level=req.nqf_level)
    db.add(s); db.commit(); db.refresh(s)
    ae.record(db, "SETHS", "STUDENT_REGISTER", entity_ref=s.student_ref, metric_name="enrolled", metric_value=1)
    return {"student_ref": s.student_ref, "status": s.status}

@router.get("/{student_ref}")
def profile(student_ref: str, db: Session = Depends(get_db)):
    s = db.execute(select(Student).where(Student.student_ref == student_ref)).scalar_one_or_none()
    if not s: raise HTTPException(404, "student not found")
    apps = db.execute(select(Application).where(Application.student_id == s.id)).scalars().all()
    return {"student_ref": s.student_ref, "full_name": s.full_name, "qualification": s.qualification,
            "nqf_level": s.nqf_level, "progress_pct": s.progress_pct, "status": s.status,
            "applications": [{"opportunity_id": a.opportunity_id, "state": a.state} for a in apps]}

@router.post("/{student_ref}/progress")
def update_progress(student_ref: str, pct: float, db: Session = Depends(get_db), _=Depends(current_user)):
    s = db.execute(select(Student).where(Student.student_ref == student_ref)).scalar_one_or_none()
    if not s: raise HTTPException(404, "student not found")
    s.progress_pct = max(0.0, min(100.0, pct))
    s.status = "COMPLETED" if s.progress_pct >= 100 else ("IN_PROGRESS" if s.progress_pct > 0 else "ENROLLED")
    db.commit()
    if s.status == "COMPLETED":
        ae.record(db, "SETHS", "COMPLETE", entity_ref=student_ref, metric_name="completed", metric_value=1)
    return {"student_ref": student_ref, "progress_pct": s.progress_pct, "status": s.status}

@router.get("/opportunities/open")
def open_opportunities(db: Session = Depends(get_db)):
    rows = db.execute(select(Opportunity).where(Opportunity.status == "OPEN")).scalars().all()
    out = []
    for o in rows:
        emp = db.get(Employer, o.employer_id)
        out.append({"id": o.id, "title": o.title, "sector": o.sector, "positions": o.positions,
                    "monthly_stipend": o.monthly_stipend, "employer": emp.org_name if emp else "—"})
    return out

@router.post("/{student_ref}/apply/{opportunity_id}")
def apply(student_ref: str, opportunity_id: int, db: Session = Depends(get_db), _=Depends(current_user)):
    s = db.execute(select(Student).where(Student.student_ref == student_ref)).scalar_one_or_none()
    o = db.get(Opportunity, opportunity_id)
    if not s or not o: raise HTTPException(404, "student or opportunity not found")
    existing = db.execute(select(Application).where(Application.student_id == s.id,
               Application.opportunity_id == opportunity_id)).scalar_one_or_none()
    if existing: raise HTTPException(409, "already applied")
    a = Application(student_id=s.id, opportunity_id=opportunity_id)
    db.add(a); db.commit()
    ae.record(db, "SETHS", "APPLICATION", entity_ref=student_ref, metric_name="applications", metric_value=1)
    return {"student_ref": student_ref, "opportunity_id": opportunity_id, "state": "SUBMITTED"}
