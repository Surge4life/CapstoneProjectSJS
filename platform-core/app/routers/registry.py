"""UDOC AI model registry — register, list, set status."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import AIModel
from app.core.dependencies import require_role

router = APIRouter(prefix="/registry", tags=["UDOC registry"])

class ModelReq(BaseModel):
    model_id: str
    name: str
    operator_id: str
    risk_tier: str = "NOTABLE"
    use_case: str = ""
    jurisdiction: str = "ZA"

@router.post("/models")
def register_model(req: ModelReq, db: Session = Depends(get_db), _=Depends(require_role("operator", "admin"))):
    if db.execute(select(AIModel).where(AIModel.model_id == req.model_id)).scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "model_id exists")
    m = AIModel(**req.model_dump()); db.add(m); db.commit(); db.refresh(m)
    return {"id": m.id, "model_id": m.model_id, "status": m.status}

@router.get("/models")
def list_models(db: Session = Depends(get_db)):
    rows = db.execute(select(AIModel)).scalars().all()
    return [{"model_id": m.model_id, "name": m.name, "operator_id": m.operator_id, "risk_tier": m.risk_tier,
             "status": m.status, "jurisdiction": m.jurisdiction} for m in rows]

@router.post("/models/{model_id}/status")
def set_status(model_id: str, new_status: str, db: Session = Depends(get_db),
               _=Depends(require_role("operator", "admin"))):
    m = db.execute(select(AIModel).where(AIModel.model_id == model_id)).scalar_one_or_none()
    if not m:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "model not found")
    m.status = new_status; db.commit()
    return {"model_id": model_id, "status": m.status}
