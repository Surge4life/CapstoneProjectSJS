"""User & access management (admin / exec only) — grant, re-grant and revoke access at runtime.

Create staff users, assign role + division, reset passwords, and activate/deactivate (revoke access
without deleting). The role decides what a user may open; access_control.py + the routers enforce it
server-side, so this is real granted access control, not just UI state. Every change is audited.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User, Tenant
from app.core.dependencies import require_role
from app.core.security import hash_password
from app.services.audit_writer import append_audit
from app.services.access_control import systems_for

router = APIRouter(prefix="/users", tags=["User & access management"])

ROLES = ["admin", "exec", "operator", "gov", "auditor", "viewer", "client"]
DIVISIONS = ["GODS", "SETHS", "MADIBA", "TS", "UDOC"]
ADMIN = require_role("admin", "exec")  # admin is always allowed; exec too


class NewUser(BaseModel):
    email: str
    password: str
    role: str = "viewer"
    division: str = "GODS"
    tenant_id: str = ""


class UserPatch(BaseModel):
    role: str | None = None
    division: str | None = None
    active: bool | None = None
    password: str | None = None


def _out(u: User) -> dict:
    return {"id": u.id, "email": u.email, "role": u.role, "division": u.division,
            "tenant_id": u.tenant_id or "", "active": bool(u.active),
            "created_at": u.created_at.isoformat() if u.created_at else None}


@router.get("", summary="List all users (admin/exec)")
def list_users(db: Session = Depends(get_db), user: dict = Depends(ADMIN)):
    rows = db.execute(select(User).order_by(User.id)).scalars().all()
    return {"count": len(rows), "users": [_out(u) for u in rows]}


@router.get("/roles", summary="Grantable roles and what each one can open (admin/exec)")
def role_catalog(user: dict = Depends(ADMIN)):
    cat = [{"role": r, "grants_systems": [s["key"] for s in systems_for(r, "GODS")],
            "is_admin": r in ("admin", "exec")} for r in ROLES]
    return {"roles": cat, "divisions": DIVISIONS,
            "note": "A division-bound operator (division != GODS) is further scoped to that division's system only."}


@router.post("", summary="Create a user and grant a role + division (admin/exec)")
def create_user(req: NewUser, db: Session = Depends(get_db), user: dict = Depends(ADMIN)):
    email = req.email.strip().lower()
    if not email or "@" not in email:
        raise HTTPException(400, "a valid email is required")
    if req.role not in ROLES:
        raise HTTPException(400, f"role must be one of {ROLES}")
    if req.division not in DIVISIONS:
        raise HTTPException(400, f"division must be one of {DIVISIONS}")
    if not req.password or len(req.password) < 6:
        raise HTTPException(400, "password must be at least 6 characters")
    if db.execute(select(User).where(User.email == email)).scalar_one_or_none():
        raise HTTPException(409, "a user with that email already exists")
    tid, tpk = (req.tenant_id or ""), None
    if tid:
        t = db.execute(select(Tenant).where(Tenant.tenant_id == tid)).scalar_one_or_none()
        if not t:
            raise HTTPException(400, f"unknown tenant_id '{tid}'")
        tpk = t.id
    u = User(email=email, password_hash=hash_password(req.password), role=req.role,
             division=req.division, tenant_id=tid, tenant_pk=tpk, active=True)
    db.add(u); db.commit(); db.refresh(u)
    append_audit(db, "USER_CREATE",
                 {"email": email, "role": req.role, "division": req.division, "by": user.get("sub")},
                 classification="GOVERNANCE", actor_class=user.get("role", "admin"))
    return {"created": True, "user": _out(u)}


@router.patch("/{uid}", summary="Re-grant role/division, reset password, or activate/deactivate (admin/exec)")
def update_user(uid: int, req: UserPatch, db: Session = Depends(get_db), user: dict = Depends(ADMIN)):
    u = db.get(User, uid)
    if not u:
        raise HTTPException(404, "user not found")
    is_self = (u.email == (user.get("sub") or "").lower())
    changes: dict = {}
    if req.role is not None:
        if req.role not in ROLES:
            raise HTTPException(400, f"role must be one of {ROLES}")
        if is_self and u.role in ("admin", "exec") and req.role not in ("admin", "exec"):
            raise HTTPException(400, "you cannot remove your own admin access (avoid lock-out)")
        changes["role"] = req.role; u.role = req.role
    if req.division is not None:
        if req.division not in DIVISIONS:
            raise HTTPException(400, f"division must be one of {DIVISIONS}")
        changes["division"] = req.division; u.division = req.division
    if req.active is not None:
        if is_self and req.active is False:
            raise HTTPException(400, "you cannot deactivate your own account")
        changes["active"] = bool(req.active); u.active = bool(req.active)
    if req.password is not None:
        if len(req.password) < 6:
            raise HTTPException(400, "password must be at least 6 characters")
        u.password_hash = hash_password(req.password); changes["password"] = "reset"
    if not changes:
        raise HTTPException(400, "no changes supplied")
    db.commit(); db.refresh(u)
    append_audit(db, "USER_UPDATE",
                 {"email": u.email, "changes": changes, "by": user.get("sub")},
                 classification="GOVERNANCE", actor_class=user.get("role", "admin"))
    return {"updated": True, "user": _out(u)}
