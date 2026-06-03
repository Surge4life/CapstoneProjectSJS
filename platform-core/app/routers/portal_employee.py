"""Employee Portal API — profile, timesheet submission/approval, payslip view."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Employee, TimesheetEntry
from app.core.dependencies import current_user, require_role
from app.services import analytics_engine as ae
from datetime import datetime, timezone

router = APIRouter(prefix="/portal/employee", tags=["Portal · Employee"])

@router.get("/{employee_ref}")
def profile(employee_ref: str, db: Session = Depends(get_db)):
    e = db.execute(select(Employee).where(Employee.employee_ref == employee_ref)).scalar_one_or_none()
    if not e: raise HTTPException(404, "employee not found")
    ts = db.execute(select(TimesheetEntry).where(TimesheetEntry.employee_id == e.id)).scalars().all()
    return {"employee_ref": e.employee_ref, "full_name": e.full_name, "division": e.division,
            "spv_id": e.spv_id, "role": e.role, "monthly_salary": e.monthly_salary, "status": e.status,
            "timesheets": [{"period": t.period, "hours": t.hours, "approved": t.approved} for t in ts]}

class TimesheetReq(BaseModel):
    hours: float
    period: str = ""

@router.post("/{employee_ref}/timesheet")
def submit_timesheet(employee_ref: str, req: TimesheetReq, db: Session = Depends(get_db), _=Depends(current_user)):
    e = db.execute(select(Employee).where(Employee.employee_ref == employee_ref)).scalar_one_or_none()
    if not e: raise HTTPException(404, "employee not found")
    period = req.period or datetime.now(timezone.utc).strftime("%Y-%m")
    t = TimesheetEntry(employee_id=e.id, period=period, hours=req.hours)
    db.add(t); db.commit()
    ae.record(db, "TS", "TIMESHEET", entity_ref=employee_ref, metric_name="hours",
              metric_value=req.hours, period=period)
    return {"employee_ref": employee_ref, "period": period, "hours": req.hours, "approved": False}

@router.post("/timesheet/{timesheet_id}/approve")
def approve(timesheet_id: int, db: Session = Depends(get_db), _=Depends(require_role("operator", "admin"))):
    t = db.get(TimesheetEntry, timesheet_id)
    if not t: raise HTTPException(404, "timesheet not found")
    t.approved = True; db.commit()
    return {"timesheet_id": timesheet_id, "approved": True}

@router.get("/{employee_ref}/payslip")
def payslip(employee_ref: str, db: Session = Depends(get_db)):
    e = db.execute(select(Employee).where(Employee.employee_ref == employee_ref)).scalar_one_or_none()
    if not e: raise HTTPException(404, "employee not found")
    period = datetime.now(timezone.utc).strftime("%Y-%m")
    hours = db.execute(select(func.coalesce(func.sum(TimesheetEntry.hours), 0.0))
            .where(TimesheetEntry.employee_id == e.id, TimesheetEntry.period == period,
                   TimesheetEntry.approved == True)).scalar() or 0.0
    gross = e.monthly_salary
    uif = round(gross * 0.01, 2)           # SA UIF 1%
    paye = round(max(0.0, (gross - 7000) * 0.18), 2)  # simplified PAYE band
    net = round(gross - uif - paye, 2)
    return {"employee_ref": employee_ref, "period": period, "approved_hours": hours,
            "gross": gross, "uif": uif, "paye": paye, "net": net}
