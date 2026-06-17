"""
Portal Operations API — turns each of the 24 Sovereign-Operator portals into a LIVE, operable console.

- GET  /portal/{key}            → the enriched portal (what it is, what it does) + its controls + recent activity
- POST /portal/{key}/control    → operate a control: server-checks the caller may run it, records a real
                                   operator action (queryable + audit-linked), and returns a reference
- GET  /portal/{key}/activity   → recent operations recorded against this portal

Access is server-authoritative: admin/exec may operate any portal; otherwise the caller must hold the
portal's base_role. This is the institutional persona layer on top of access_control enforcement.
"""
from datetime import datetime, timezone
import json, uuid
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy import select
from app.core.dependencies import current_user
from app.db.session import get_db
from app.db.models import OperatorAction
from app.services import sovereign_profiles as sp
from sqlalchemy.orm import Session

router = APIRouter(prefix="/portal", tags=["Portals"])


def _may_operate(user: dict, profile: dict) -> bool:
    role = (user.get("role") or "").lower()
    return role in ("admin", "exec") or role == (profile.get("base_role") or "").lower()


def _activity(db: Session, key: str, limit: int = 10) -> list[dict]:
    rows = db.execute(
        select(OperatorAction).where(OperatorAction.profile_key == key)
        .order_by(OperatorAction.created_at.desc()).limit(limit)
    ).scalars().all()
    return [{
        "ref": r.ref, "control": r.capability, "op_type": r.op_type,
        "actor": r.actor_email, "summary": r.result_summary, "status": r.status,
        "at": r.created_at.isoformat() if r.created_at else None,
    } for r in rows]


@router.get("/{key}", summary="A portal: what it is, its controls, and recent activity")
def portal_detail(key: str, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    prof = sp.get(key)
    if not prof:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"unknown portal '{key}'")
    return {
        "portal": prof,
        "may_operate": _may_operate(user, prof),
        "operator_role": (user.get("role") or ""),
        "activity": _activity(db, prof["key"]),
    }


@router.get("/{key}/activity", summary="Recent operations recorded against this portal")
def portal_activity(key: str, limit: int = 20, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    prof = sp.get(key)
    if not prof:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"unknown portal '{key}'")
    return {"portal": prof["key"], "title": prof["title"], "activity": _activity(db, prof["key"], min(limit, 100))}


@router.post("/{key}/control", summary="Operate a control on this portal (records a real, audit-linked action)")
def operate_control(key: str, payload: dict = Body(...),
                    db: Session = Depends(get_db), user: dict = Depends(current_user)):
    prof = sp.get(key)
    if not prof:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"unknown portal '{key}'")
    if not _may_operate(user, prof):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            f"This portal is operated by the '{prof['base_role']}' role; you are '{user.get('role')}'.")
    control = (payload.get("control") or "").strip()
    valid = {c["name"] for c in prof["controls"]}
    if control not in valid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"'{control}' is not a control on this portal")
    note = (payload.get("note") or "").strip()
    target = (payload.get("target") or "").strip()
    ref = "PA-" + uuid.uuid4().hex[:8].upper()
    summary = f"{prof['title']} · {control}" + (f" — {note}" if note else "")
    op = OperatorAction(
        ref=ref, actor_email=user.get("sub", ""), profile_key=prof["key"], capability=control,
        op_type=sp.op_type_for(control), target=target, result_ref=ref, result_summary=summary,
        detail_json=json.dumps({"portal": prof["title"], "control": control, "note": note,
                                "by_role": user.get("role", ""), "group": prof["group"]}),
        status="EXECUTED",
    )
    db.add(op); db.commit(); db.refresh(op)
    return {
        "ref": ref, "portal": prof["title"], "portal_key": prof["key"], "control": control,
        "op_type": op.op_type, "status": "EXECUTED",
        "at": op.created_at.isoformat() if op.created_at else datetime.now(timezone.utc).isoformat(),
        "message": f"{control} executed on {prof['title']}.",
    }
