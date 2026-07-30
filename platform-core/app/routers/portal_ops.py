"""
Portal Operations API — turns each of the 24 Sovereign-Operator portals into a LIVE, operable console.

- GET  /portal/{key}            → enriched portal + controls + activity
- POST /portal/{key}/control    → operate a control (audit-linked) + dual-path live Core for HITL/Regulator/AI_OWNER
- GET  /portal/{key}/activity   → recent operations

Access is server-authoritative: admin/exec may operate any portal; otherwise the caller must hold the
portal's base_role.
"""
from datetime import datetime, timezone
import json, uuid
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.dependencies import current_user
from app.db.session import get_db
from app.db.models import OperatorAction, OversightCase
from app.services import sovereign_profiles as sp
from app.services.audit_writer import append_audit

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


def _live_side_effect(db: Session, user: dict, key: str, control: str, target: str, note: str) -> dict | None:
    """Map selected portal controls onto real Core tables/APIs (Neon-light)."""
    k = (key or "").upper()
    c = (control or "").strip()
    live: dict = {}

    if k == "HITL_REVIEW":
        if c in ("Approve AI Decision", "Override", "Release", "Flag for Training"):
            # Prefer resolve existing open case by target (= case_ref); else open new oversight case
            case = None
            if target:
                case = db.execute(
                    select(OversightCase).where(OversightCase.case_ref == target)
                ).scalar_one_or_none()
            if case and c in ("Approve AI Decision", "Override", "Release"):
                case.state = "OVERRIDDEN" if c == "Override" else "RESOLVED"
                case.resolution = note or c
                case.assigned_to = user.get("sub", "")
                db.commit()
                append_audit(db, "HITL_RESOLVE", {"case": case.case_ref, "control": c, "state": case.state},
                             classification="GOVERNANCE", actor_class=user.get("role", "operator"))
                live = {"oversight": {"case_ref": case.case_ref, "state": case.state, "action": c}}
            else:
                model_id = target if target and not target.upper().startswith("COB-") else (target or "model-001")
                if model_id.upper().startswith("COB-"):
                    model_id = "model-001"
                oc = OversightCase(
                    case_ref=f"COB-{uuid.uuid4().hex[:8]}",
                    model_id=model_id[:64],
                    reason=note or f"HITL · {c}",
                )
                db.add(oc)
                db.commit()
                db.refresh(oc)
                append_audit(db, "HITL_OPEN", {"case": oc.case_ref, "model": model_id, "control": c},
                             classification="GOVERNANCE")
                live = {"oversight": {"case_ref": oc.case_ref, "state": oc.state, "action": c, "model_id": model_id}}

    elif k == "REGULATOR":
        if c in ("Start Audit", "Review Submission", "Impose Penalty", "Issue Directive"):
            model_id = target or "model-001"
            oc = OversightCase(
                case_ref=f"COB-{uuid.uuid4().hex[:8]}",
                model_id=model_id[:64],
                reason=f"REGULATOR · {c}" + (f" — {note}" if note else ""),
            )
            db.add(oc)
            db.commit()
            db.refresh(oc)
            append_audit(db, "REGULATOR_ACTION", {"case": oc.case_ref, "control": c, "model": model_id},
                         classification="GOVERNANCE")
            live = {"oversight": {"case_ref": oc.case_ref, "state": oc.state, "action": c}}

    elif k == "AI_OWNER":
        # Record intent against registry model id in detail; no heavy writes
        live = {"ai_owner": {"control": c, "model_id": target or "model-001", "note": note or ""}}
        append_audit(db, "AI_OWNER_CONTROL", live["ai_owner"], classification="OPERATIONS",
                     actor_class=user.get("role", "client"))

    return live or None


@router.get("/{key}", summary="A portal: what it is, its controls, and recent activity")
def portal_detail(key: str, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    prof = sp.get(key)
    if not prof:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"unknown portal '{key}'")
    out = {
        "portal": prof,
        "may_operate": _may_operate(user, prof),
        "operator_role": (user.get("role") or ""),
        "activity": _activity(db, prof["key"]),
        "live": {},
    }
    k = prof["key"].upper()
    if k in ("HITL_REVIEW", "REGULATOR"):
        rows = db.execute(
            select(OversightCase).order_by(OversightCase.id.desc()).limit(12)
        ).scalars().all()
        out["live"]["oversight_cases"] = [{
            "case_ref": c.case_ref, "model_id": c.model_id, "reason": (c.reason or "")[:120],
            "state": c.state, "assigned_to": c.assigned_to,
        } for c in rows]
    return out


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

    live = None
    try:
        live = _live_side_effect(db, user, prof["key"], control, target, note)
    except Exception as e:
        live = {"error": str(e)[:200]}

    if live and live.get("oversight", {}).get("case_ref"):
        summary += f" · case {live['oversight']['case_ref']}"

    op = OperatorAction(
        ref=ref, actor_email=user.get("sub", ""), profile_key=prof["key"], capability=control,
        op_type=sp.op_type_for(control), target=target, result_ref=ref, result_summary=summary,
        detail_json=json.dumps({"portal": prof["title"], "control": control, "note": note,
                                "by_role": user.get("role", ""), "group": prof["group"],
                                "live": live}),
        status="EXECUTED",
    )
    db.add(op); db.commit(); db.refresh(op)
    return {
        "ref": ref, "portal": prof["title"], "portal_key": prof["key"], "control": control,
        "op_type": op.op_type, "status": "EXECUTED",
        "at": op.created_at.isoformat() if op.created_at else datetime.now(timezone.utc).isoformat(),
        "message": f"{control} executed on {prof['title']}.",
        "live": live,
    }
