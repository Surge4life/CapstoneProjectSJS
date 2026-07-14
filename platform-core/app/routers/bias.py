"""UDOC bias/fairness — disparate impact + statistical parity surfaced from decisions."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import AIModel, Decision
from app.core.dependencies import current_user

router = APIRouter(prefix="/bias", tags=["UDOC bias"])

@router.get("/scan")
def scan(db: Session = Depends(get_db), _: dict = Depends(current_user)):
    rows = db.execute(select(Decision).order_by(Decision.id.desc()).limit(200)).scalars().all()
    flagged = [d for d in rows if "Disparate impact" in (d.block_reasons or "") or "parity" in (d.block_reasons or "")]
    return {"decisions_scanned": len(rows), "fairness_flagged": len(flagged),
            "flag_rate": round(len(flagged) / len(rows), 3) if rows else 0.0}
