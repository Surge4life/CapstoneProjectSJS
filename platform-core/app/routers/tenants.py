"""
SaaS tenancy + commercial layer — tenant orgs, six-tier plans, API keys, usage.
Platform staff (admin/operator) manage tenants; a tenant can read its own plan + usage.
"""
import hashlib
import secrets
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Tenant, ApiKey, AIModel
from app.core.dependencies import current_user, principal, require_role, scope_pk
from app.core.tiers import TIERS, ORDER, tier_info
from app.services.audit_writer import append_audit

router = APIRouter(prefix="/tenants", tags=["SaaS · tenancy & commercial"])


def _tenant_out(t: Tenant) -> dict:
    ti = tier_info(t.tier)
    return {"id": t.id, "tenant_id": t.tenant_id, "name": t.name, "sector": t.sector,
            "tier": t.tier, "tier_name": ti["name"], "status": t.status,
            "decision_quota": t.decision_quota, "usage_decisions": t.usage_decisions,
            "quota_remaining": (None if t.decision_quota < 0 else max(0, t.decision_quota - t.usage_decisions)),
            "entitlements": ti, "period_start": t.period_start.isoformat(), "created_at": t.created_at.isoformat()}


@router.get("/tiers")
def tiers(_: dict = Depends(current_user)):
    return {"order": ORDER, "tiers": TIERS}


class TenantReq(BaseModel):
    tenant_id: str
    name: str
    sector: str = "GENERAL"
    tier: str = "SANDBOX"


@router.post("")
def create_tenant(req: TenantReq, db: Session = Depends(get_db), user: dict = Depends(require_role("admin", "operator"))):
    if db.execute(select(Tenant).where(Tenant.tenant_id == req.tenant_id)).scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "tenant_id exists")
    ti = tier_info(req.tier)
    t = Tenant(tenant_id=req.tenant_id, name=req.name, sector=req.sector.upper(),
               tier=req.tier.upper(), status="ACTIVE", decision_quota=ti["decision_quota"])
    db.add(t); db.commit(); db.refresh(t)
    append_audit(db, "TENANT_CREATE", {"tenant": t.tenant_id, "tier": t.tier}, classification="GOVERNANCE",
                 actor_class=user.get("role", "SYSTEM"))
    return _tenant_out(t)


@router.get("")
def list_tenants(db: Session = Depends(get_db), _: dict = Depends(require_role("admin", "operator", "auditor"))):
    return [_tenant_out(t) for t in db.execute(select(Tenant).order_by(Tenant.id)).scalars().all()]


class KeyReq(BaseModel):
    name: str = "default"


@router.get("/me")
def my_tenant(db: Session = Depends(get_db), user: dict = Depends(principal)):
    pk = user.get("tenant_pk")
    if not pk:
        return {"tenant": None, "note": "platform staff — not tenant-scoped", "role": user.get("role")}
    t = db.get(Tenant, pk)
    if not t:
        raise HTTPException(404, "tenant not found")
    return _tenant_out(t)


@router.get("/me/apikeys")
def my_keys(db: Session = Depends(get_db), user: dict = Depends(principal)):
    pk = user.get("tenant_pk")
    if not pk:
        return []
    rows = db.execute(select(ApiKey).where(ApiKey.tenant_pk == pk)).scalars().all()
    return [{"id": k.id, "prefix": k.prefix, "name": k.name, "active": k.active,
             "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None} for k in rows]


@router.post("/me/apikeys")
def issue_my_key(req: KeyReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    pk = user.get("tenant_pk")
    if not pk:
        raise HTTPException(400, "not a tenant-scoped caller")
    t = db.get(Tenant, pk)
    existing = db.execute(select(ApiKey).where(ApiKey.tenant_pk == pk, ApiKey.active == True)).scalars().all()  # noqa: E712
    if len(existing) >= tier_info(t.tier)["api_keys"]:
        raise HTTPException(402, f"tier {t.tier} allows {tier_info(t.tier)['api_keys']} active key(s)")
    raw = f"gods_{t.tenant_id}_{secrets.token_urlsafe(24)}"
    ak = ApiKey(tenant_pk=pk, name=req.name, prefix=raw[:12],
                key_hash=hashlib.sha256(raw.encode()).hexdigest(), active=True)
    db.add(ak); db.commit()
    append_audit(db, "APIKEY_ISSUE", {"tenant": t.tenant_id, "prefix": ak.prefix, "self": True},
                 classification="GOVERNANCE", actor_class=user.get("role", "CLIENT"))
    return {"api_key": raw, "prefix": ak.prefix, "name": ak.name,
            "note": "Store this now — shown once. Send as X-API-Key."}


@router.get("/{tid}")
def get_tenant(tid: int, db: Session = Depends(get_db), _: dict = Depends(require_role("admin", "operator", "auditor"))):
    t = db.get(Tenant, tid)
    if not t:
        raise HTTPException(404, "tenant not found")
    return _tenant_out(t)


@router.post("/{tid}/tier")
def set_tier(tid: int, tier: str, db: Session = Depends(get_db), user: dict = Depends(require_role("admin", "operator"))):
    t = db.get(Tenant, tid)
    if not t:
        raise HTTPException(404, "tenant not found")
    if tier.upper() not in TIERS:
        raise HTTPException(400, f"unknown tier; choose {ORDER}")
    t.tier = tier.upper(); t.decision_quota = tier_info(tier)["decision_quota"]; db.commit()
    append_audit(db, "TENANT_TIER", {"tenant": t.tenant_id, "tier": t.tier}, classification="GOVERNANCE",
                 actor_class=user.get("role", "SYSTEM"))
    return _tenant_out(t)


@router.post("/{tid}/status")
def set_status(tid: int, status_value: str, db: Session = Depends(get_db), user: dict = Depends(require_role("admin", "operator"))):
    t = db.get(Tenant, tid)
    if not t:
        raise HTTPException(404, "tenant not found")
    t.status = status_value.upper(); db.commit()
    return _tenant_out(t)


@router.post("/{tid}/apikeys")
def issue_key(tid: int, req: KeyReq, db: Session = Depends(get_db), user: dict = Depends(require_role("admin", "operator"))):
    t = db.get(Tenant, tid)
    if not t:
        raise HTTPException(404, "tenant not found")
    existing = db.execute(select(ApiKey).where(ApiKey.tenant_pk == tid, ApiKey.active == True)).scalars().all()  # noqa: E712
    if len(existing) >= tier_info(t.tier)["api_keys"]:
        raise HTTPException(402, f"tier {t.tier} allows {tier_info(t.tier)['api_keys']} active key(s)")
    raw = f"gods_{t.tenant_id}_{secrets.token_urlsafe(24)}"
    ak = ApiKey(tenant_pk=tid, name=req.name, prefix=raw[:12],
                key_hash=hashlib.sha256(raw.encode()).hexdigest(), active=True)
    db.add(ak); db.commit(); db.refresh(ak)
    append_audit(db, "APIKEY_ISSUE", {"tenant": t.tenant_id, "prefix": ak.prefix}, classification="GOVERNANCE",
                 actor_class=user.get("role", "SYSTEM"))
    return {"api_key": raw, "prefix": ak.prefix, "name": ak.name,
            "note": "Store this now — it is shown only once. Send it as the X-API-Key header."}


@router.get("/{tid}/apikeys")
def list_keys(tid: int, db: Session = Depends(get_db), _: dict = Depends(require_role("admin", "operator", "auditor"))):
    rows = db.execute(select(ApiKey).where(ApiKey.tenant_pk == tid)).scalars().all()
    return [{"id": k.id, "prefix": k.prefix, "name": k.name, "active": k.active,
             "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None} for k in rows]
