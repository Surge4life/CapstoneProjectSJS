"""UDOC compliance — POPIA/regulatory checks surfaced as a sweep over registered models."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import AIModel, Decision
from app.core.dependencies import current_user

router = APIRouter(prefix="/compliance", tags=["UDOC compliance"])

# Frameworks the platform enforces (from GODS_POPIA_Compliance_Framework + spec)
FRAMEWORKS = ["POPIA", "SA NAIFP", "FICA", "FSCA", "PFMA/MFMA", "EU AI Act", "NIST PQC", "FIPS 140-3"]

@router.get("/frameworks")
def frameworks(_: dict = Depends(current_user)):
    return {"frameworks": FRAMEWORKS}

@router.get("/sweep")
def sweep(db: Session = Depends(get_db), _: dict = Depends(current_user)):
    models = db.execute(select(AIModel)).scalars().all()
    out = []
    for m in models:
        last = db.execute(select(Decision).where(Decision.model_pk == m.id)
                          .order_by(Decision.id.desc()).limit(1)).scalar_one_or_none()
        out.append({"model_id": m.model_id, "risk_tier": m.risk_tier, "status": m.status,
                    "last_compliance": last.compliance if last else None,
                    "compliant": (last.compliance >= 0.70) if last else None})
    return {"checked": len(out), "results": out}
