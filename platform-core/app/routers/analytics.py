"""
UDOC Analytics API — the data-record-and-analytics layer for every division.
Each division platform reads its KPIs, time-series, totals, and record feed from here.
Records are written by the division routers (seths/madiba/ts) as events occur.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import current_user
from app.services import analytics_engine as ae

router = APIRouter(prefix="/analytics", tags=["UDOC analytics"])

VALID = {"SETHS", "MADIBA", "TS", "UDOC"}

@router.get("/{division}/kpis")
def kpis(division: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    division = division.upper()
    return ae.kpis(db, division) if division in VALID else {"error": "unknown division"}

@router.get("/{division}/totals")
def totals(division: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    return ae.totals(db, division.upper())

@router.get("/{division}/timeseries")
def timeseries(division: str, metric: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    return {"division": division.upper(), "metric": metric,
            "series": ae.timeseries(db, division.upper(), metric)}

@router.get("/{division}/records")
def records(division: str, limit: int = 50, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    return {"division": division.upper(), "records": ae.recent(db, division.upper(), limit)}
