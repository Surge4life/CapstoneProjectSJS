"""UDOC sovereignty — SVS posture across recent decisions (BGP/traceroute/DNSSEC/storage)."""
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Decision
from app.core.dependencies import require_role

router = APIRouter(prefix="/sovereignty", tags=["UDOC sovereignty"])

@router.get("/posture")
def posture(db: Session = Depends(get_db), _=Depends(require_role("operator", "auditor", "admin"))):
    total = db.execute(select(func.count(Decision.id))).scalar() or 0
    breaches = db.execute(select(func.count(Decision.id)).where(Decision.sovereign == False)).scalar() or 0
    return {"decisions": total, "sovereignty_breaches": breaches,
            "sovereign_rate": round((total - breaches) / total, 3) if total else 1.0}
