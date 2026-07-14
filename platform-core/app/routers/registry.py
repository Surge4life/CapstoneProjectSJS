"""UDOC AI model registry — register, list, set status. Tenant-isolated."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import AIModel, Tenant
from app.core.dependencies import principal, scope_pk
from app.core.tiers import tier_info

router = APIRouter(prefix="/registry", tags=["UDOC registry"])


class ModelReq(BaseModel):
    model_id: str
    name: str
    operator_id: str
    risk_tier: str = "NOTABLE"
    use_case: str = ""
    jurisdiction: str = "ZA"


@router.post("/models")
def register_model(req: ModelReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    if user.get("role") == "viewer":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "viewers cannot register models")
    if db.execute(select(AIModel).where(AIModel.model_id == req.model_id)).scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "model_id exists")
    scope = scope_pk(user)
    tenant_pk = scope if (scope and scope != -1) else None
    # per-tier model cap for tenant-scoped callers
    if tenant_pk:
        t = db.get(Tenant, tenant_pk)
        if t and t.status != "ACTIVE":
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"tenant {t.tenant_id} is {t.status}")
        cap = tier_info(t.tier)["max_models"] if t else 0
        if cap >= 0:
            count = len(db.execute(select(AIModel).where(AIModel.tenant_pk == tenant_pk)).scalars().all())
            if count >= cap:
                raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED,
                                    f"tier {t.tier} allows {cap} model(s); upgrade to register more")
    m = AIModel(**req.model_dump(), tenant_pk=tenant_pk)
    db.add(m); db.commit(); db.refresh(m)
    return {"id": m.id, "model_id": m.model_id, "status": m.status, "tenant_pk": tenant_pk}


@router.get("/models")
def list_models(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(AIModel)
    if scope == -1:
        return []
    if scope is not None:
        q = q.where(AIModel.tenant_pk == scope)
    rows = db.execute(q).scalars().all()
    return [{"model_id": m.model_id, "name": m.name, "operator_id": m.operator_id, "risk_tier": m.risk_tier,
             "status": m.status, "jurisdiction": m.jurisdiction, "tenant_pk": m.tenant_pk} for m in rows]


@router.post("/models/{model_id}/status")
def set_status(model_id: str, new_status: str, db: Session = Depends(get_db), user: dict = Depends(principal)):
    if user.get("role") == "viewer":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "viewers cannot change status")
    m = db.execute(select(AIModel).where(AIModel.model_id == model_id)).scalar_one_or_none()
    if not m:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "model not found")
    scope = scope_pk(user)
    if scope is not None and m.tenant_pk != scope:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "model not found")  # isolation: don't leak existence
    m.status = new_status; db.commit()
    return {"model_id": model_id, "status": m.status}
