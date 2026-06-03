"""
SaaS client API (UDOC .apk) — client orgs register, get an API key, and govern THEIR AIs:
register models, run governance decisions, see their audit trail, suspend/override.
Scoped so a client sees only their own models (operator_id == client_ref).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.db.session import get_db
from app.db.models import SaaSClient, AIModel, Decision
from app.core.dependencies import current_user
from app.services.audit_writer import append_audit
import uuid, secrets

router = APIRouter(prefix="/saas", tags=["UDOC SaaS clients"])

class ClientReg(BaseModel):
    org_name: str
    contact_email: EmailStr
    tier: str = "STANDARD"

@router.post("/register")
def register(req: ClientReg, db: Session = Depends(get_db)):
    c = SaaSClient(client_ref=f"CLI-{uuid.uuid4().hex[:8]}", org_name=req.org_name,
                   contact_email=req.contact_email, tier=req.tier, api_key=secrets.token_hex(20))
    db.add(c); db.commit(); db.refresh(c)
    return {"client_ref": c.client_ref, "api_key": c.api_key, "tier": c.tier}

@router.get("/{client_ref}/models")
def my_models(client_ref: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    rows = db.execute(select(AIModel).where(AIModel.operator_id == client_ref)).scalars().all()
    return [{"model_id": m.model_id, "name": m.name, "risk_tier": m.risk_tier, "status": m.status} for m in rows]

@router.post("/{client_ref}/suspend/{model_id}")
def suspend(client_ref: str, model_id: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    m = db.execute(select(AIModel).where(AIModel.model_id == model_id,
                   AIModel.operator_id == client_ref)).scalar_one_or_none()
    if not m: raise HTTPException(404, "model not found for this client")
    m.status = "SUSPENDED"; db.commit()
    append_audit(db, "CLIENT_SUSPEND", {"client": client_ref, "model": model_id}, classification="GOVERNANCE")
    return {"model_id": model_id, "status": "SUSPENDED", "control": "client-initiated kill switch"}

@router.post("/{client_ref}/resume/{model_id}")
def resume(client_ref: str, model_id: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    m = db.execute(select(AIModel).where(AIModel.model_id == model_id,
                   AIModel.operator_id == client_ref)).scalar_one_or_none()
    if not m: raise HTTPException(404, "model not found for this client")
    m.status = "ACTIVE"; db.commit()
    append_audit(db, "CLIENT_RESUME", {"client": client_ref, "model": model_id}, classification="GOVERNANCE")
    return {"model_id": model_id, "status": "ACTIVE"}

@router.get("/{client_ref}/dashboard")
def dashboard(client_ref: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    models = db.execute(select(AIModel).where(AIModel.operator_id == client_ref)).scalars().all()
    ids = [m.id for m in models]
    decisions = []
    if ids:
        decisions = db.execute(select(Decision).where(Decision.model_pk.in_(ids))
                    .order_by(Decision.id.desc()).limit(50)).scalars().all()
    blocked = sum(1 for d in decisions if d.decision == "BLOCK")
    return {"client_ref": client_ref, "models": len(models),
            "active": sum(1 for m in models if m.status == "ACTIVE"),
            "suspended": sum(1 for m in models if m.status == "SUSPENDED"),
            "recent_decisions": len(decisions), "recent_blocks": blocked,
            "control": "you are always in control of your deployed AIs"}
