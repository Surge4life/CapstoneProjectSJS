"""
Sector experience API — drives the genuinely-differentiated Public vs Private console.
GET /sector/profile     -> the caller's sector identity (label, audience, oversight model, terminology, accent)
GET /sector/frameworks  -> the regulatory frameworks that actually apply to that sector
GET /sector/overview    -> KPIs from real decision/oversight data, framed in that sector's language
Clients resolve to their tenant's sector; staff/admin may inspect either via ?sector=PUBLIC|PRIVATE.
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import current_user
from app.db.models import Tenant, Decision, AIModel, OversightCase, EvaCertificate
from app.services import sectors as sec
from app.services.audit_writer import append_audit

router = APIRouter(prefix="/sector", tags=["Sector experience"])
_STAFF = ("admin", "exec", "auditor", "gov", "operator")
_ADMIN = ("admin", "exec")


def _resolve(db: Session, user: dict, override: str | None):
    role = user.get("role"); tpk = user.get("tenant_pk")
    # staff/admin may inspect a sector explicitly
    if override and role in _STAFF:
        return sec.get(override), None
    # a tenant user resolves to their tenant's actual sector
    if tpk:
        t = db.execute(select(Tenant).where(Tenant.id == tpk)).scalar_one_or_none()
        if t:
            return sec.get(t.sector), t
    return sec.get(override or "GENERAL"), None


@router.get("/profile")
def profile(sector: str | None = Query(None), db: Session = Depends(get_db), user: dict = Depends(current_user)):
    s, t = _resolve(db, user, sector)
    return {"sector": s["key"], "label": s["label"], "audience": s["audience"], "accent": s["accent"],
            "tagline": s["tagline"], "summary": s["summary"], "oversight_model": s["oversight_model"],
            "terminology": s["terminology"], "tenant": (t.name if t else None)}


@router.get("/frameworks")
def frameworks(sector: str | None = Query(None), db: Session = Depends(get_db), user: dict = Depends(current_user)):
    s, t = _resolve(db, user, sector)
    return {"sector": s["key"], "label": s["label"], "frameworks": s["frameworks"]}


@router.get("/overview")
def overview(sector: str | None = Query(None), db: Session = Depends(get_db), user: dict = Depends(current_user)):
    s, t = _resolve(db, user, sector)
    tpk = t.id if t else None
    dq = select(func.count(Decision.id)); bq = select(func.count(Decision.id)).where(Decision.decision == "BLOCK")
    if tpk is not None:
        dq = dq.join(AIModel, Decision.model_pk == AIModel.id).where(AIModel.tenant_pk == tpk)
        bq = bq.join(AIModel, Decision.model_pk == AIModel.id).where(AIModel.tenant_pk == tpk)
    dec = db.execute(dq).scalar() or 0
    blk = db.execute(bq).scalar() or 0
    ovo = db.execute(select(func.count(OversightCase.id)).where(OversightCase.state == "OPEN")).scalar() or 0
    rate = round(blk / dec, 3) if dec else 0.0
    subj = s["terminology"]["subjects"].capitalize()
    is_pub = s["key"] == "PUBLIC"
    tiles = [
        {"k": f"{subj}-affecting decisions", "v": dec},
        {"k": "Blocked — rights/risk" if is_pub else "Blocked — fairness/risk", "v": blk},
        {"k": "Block rate", "v": rate},
        {"k": "Open oversight" if is_pub else "Open reviews", "v": ovo},
        {"k": "Frameworks in scope", "v": len(s["frameworks"])},
    ]
    return {"sector": s["key"], "label": s["label"], "audience": s["audience"], "tiles": tiles}


# ─── Admin sector oversight (staff) ───
def _sector_dec_counts(db: Session, tpks: list[int]):
    if not tpks:
        return 0, 0
    base = select(func.count(Decision.id)).join(AIModel, Decision.model_pk == AIModel.id).where(AIModel.tenant_pk.in_(tpks))
    dec = db.execute(base).scalar() or 0
    blk = db.execute(base.where(Decision.decision == "BLOCK")).scalar() or 0
    return dec, blk


@router.get("/admin/breakdown")
def admin_breakdown(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    """Per-sector portfolio view across all tenants — staff only."""
    if user.get("role") not in _STAFF:
        raise HTTPException(403, "staff only")
    out = []
    for key in ("PUBLIC", "PRIVATE", "GENERAL"):
        s = sec.get(key)
        tlist = db.execute(select(Tenant).where(Tenant.sector == key)).scalars().all()
        tpks = [t.id for t in tlist]
        dec, blk = _sector_dec_counts(db, tpks)
        certs = db.execute(select(func.count(EvaCertificate.id)).where(EvaCertificate.sector == key)).scalar() or 0
        tenants = []
        for t in tlist:
            td, tb = _sector_dec_counts(db, [t.id])
            tenants.append({"tenant_id": t.tenant_id, "name": t.name, "status": t.status,
                            "tier": t.tier, "decisions": td, "blocked": tb})
        out.append({
            "sector": key, "label": s["label"], "accent": s["accent"], "audience": s["audience"],
            "tenants": len(tlist), "decisions": dec, "blocked": blk,
            "block_rate": round(blk / dec, 3) if dec else 0.0,
            "certificates": certs, "frameworks": len(s["frameworks"]),
            "tenant_list": tenants,
        })
    open_oversight = db.execute(select(func.count(OversightCase.id)).where(OversightCase.state == "OPEN")).scalar() or 0
    return {"sectors": out, "open_oversight": open_oversight}


class AssignReq(BaseModel):
    tenant_id: str
    sector: str


@router.post("/admin/assign")
def admin_assign(body: AssignReq, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    """Classify a tenant into a sector (PUBLIC|PRIVATE|GENERAL) — admin only."""
    if user.get("role") not in _ADMIN:
        raise HTTPException(403, "admin only")
    key = (body.sector or "").upper()
    if key not in ("PUBLIC", "PRIVATE", "GENERAL"):
        raise HTTPException(422, "sector must be PUBLIC, PRIVATE or GENERAL")
    t = db.execute(select(Tenant).where(Tenant.tenant_id == body.tenant_id)).scalar_one_or_none()
    if not t:
        raise HTTPException(404, f"tenant '{body.tenant_id}' not found")
    prev = t.sector
    t.sector = key
    db.commit()
    append_audit(db, "SECTOR_ASSIGN", {"tenant": t.tenant_id, "from": prev, "to": key, "by": user.get("sub")},
                 classification="GOVERNANCE", actor_class=user.get("role", "admin"))
    return {"ok": True, "tenant_id": t.tenant_id, "name": t.name, "sector": key, "previous": prev}
