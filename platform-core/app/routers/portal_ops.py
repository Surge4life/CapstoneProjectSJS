"""
Portal Operations API — turns each of the 24 Sovereign-Operator portals into a LIVE, operable console.

- GET  /portal/{key}            → enriched portal + controls + activity + live oversight when applicable
- POST /portal/{key}/control    → operate a control (audit-linked) + dual-path live Core for case-bearing portals
- GET  /portal/{key}/activity   → recent operations

Access is server-authoritative: admin/exec may operate any portal; otherwise the caller must hold the
portal's base_role. Neon-light: reuses OversightCase only — no new tables.
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

# Portals that dual-path into OversightCase (or audit-only for AI_OWNER)
LIVE_CASE_PORTALS = {
    "HITL_REVIEW", "REGULATOR", "INFO_REGULATOR", "SAHRC",
    "CASE_MANAGER", "WELFARE", "SARS", "CONSTITUTIONAL_OVERSIGHT",
}
LIVE_AUDIT_PORTALS = {"AI_OWNER", "PRIVATE_COMPLIANCE"}


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


def _oversight_list(db: Session, limit: int = 12) -> list[dict]:
    rows = db.execute(
        select(OversightCase).order_by(OversightCase.id.desc()).limit(limit)
    ).scalars().all()
    return [{
        "case_ref": c.case_ref, "model_id": c.model_id, "reason": (c.reason or "")[:120],
        "state": c.state, "assigned_to": c.assigned_to,
    } for c in rows]


def _open_case(db: Session, user: dict, model_id: str, reason: str, audit_evt: str) -> dict:
    mid = (model_id or "model-001")[:64]
    if mid.upper().startswith("COB-"):
        mid = "model-001"
    oc = OversightCase(
        case_ref=f"COB-{uuid.uuid4().hex[:8]}",
        model_id=mid,
        reason=reason[:500] if reason else "portal action",
    )
    db.add(oc)
    db.commit()
    db.refresh(oc)
    append_audit(db, audit_evt, {"case": oc.case_ref, "model": mid, "reason": reason[:200]},
                 classification="GOVERNANCE", actor_class=user.get("role", "operator"))
    return {"case_ref": oc.case_ref, "state": oc.state, "model_id": mid}


def _resolve_case(db: Session, user: dict, case_ref: str, control: str, note: str) -> dict | None:
    case = db.execute(
        select(OversightCase).where(OversightCase.case_ref == case_ref)
    ).scalar_one_or_none()
    if not case:
        return None
    case.state = "OVERRIDDEN" if "Override" in control or "Withdraw" in control else "RESOLVED"
    case.resolution = note or control
    case.assigned_to = user.get("sub", "")
    db.commit()
    append_audit(db, "PORTAL_RESOLVE", {"case": case.case_ref, "control": control, "state": case.state},
                 classification="GOVERNANCE", actor_class=user.get("role", "operator"))
    return {"case_ref": case.case_ref, "state": case.state, "action": control}


def _live_side_effect(db: Session, user: dict, key: str, control: str, target: str, note: str) -> dict | None:
    """Map selected portal controls onto real Core tables (Neon-light)."""
    k = (key or "").upper()
    c = (control or "").strip()

    # —— HITL: resolve by case_ref or open ——
    if k == "HITL_REVIEW":
        if c in ("Approve AI Decision", "Override", "Release", "Flag for Training"):
            if target and target.upper().startswith("COB-"):
                resolved = _resolve_case(db, user, target, c, note)
                if resolved:
                    return {"oversight": resolved}
            o = _open_case(db, user, target or "model-001", note or f"HITL · {c}", "HITL_OPEN")
            o["action"] = c
            return {"oversight": o}

    # —— Regulator family: open case ——
    if k == "REGULATOR" and c in ("Start Audit", "Review Submission", "Impose Penalty", "Issue Directive"):
        o = _open_case(db, user, target or "model-001", f"REGULATOR · {c}" + (f" — {note}" if note else ""), "REGULATOR_ACTION")
        o["action"] = c
        return {"oversight": o}

    if k == "INFO_REGULATOR" and c in ("Open Investigation", "Issue PAIA Notice", "Assess Breach", "Close Case"):
        if c == "Close Case" and target and target.upper().startswith("COB-"):
            resolved = _resolve_case(db, user, target, c, note)
            if resolved:
                return {"oversight": resolved}
        o = _open_case(db, user, target or "model-001", f"INFO_REG · {c}" + (f" — {note}" if note else ""), "INFO_REG_ACTION")
        o["action"] = c
        return {"oversight": o}

    if k == "CONSTITUTIONAL_OVERSIGHT" and c in ("Constitutional Review", "Issue Opinion", "Refer to Court", "Close Matter"):
        if c == "Close Matter" and target and target.upper().startswith("COB-"):
            resolved = _resolve_case(db, user, target, c, note)
            if resolved:
                return {"oversight": resolved}
        o = _open_case(db, user, target or "model-001", f"COB · {c}" + (f" — {note}" if note else ""), "COB_ACTION")
        o["action"] = c
        return {"oversight": o}

    if k == "SAHRC" and c in ("Log Complaint", "Start Investigation", "Schedule Hearing", "Publish Finding"):
        if c == "Publish Finding" and target and target.upper().startswith("COB-"):
            resolved = _resolve_case(db, user, target, c, note)
            if resolved:
                return {"oversight": resolved}
        o = _open_case(db, user, target or "model-001", f"SAHRC · {c}" + (f" — {note}" if note else ""), "SAHRC_ACTION")
        o["action"] = c
        return {"oversight": o}

    if k == "CASE_MANAGER" and c in ("Open Case", "Assign Worker", "Update Status", "Close Case"):
        if c == "Close Case" and target and target.upper().startswith("COB-"):
            resolved = _resolve_case(db, user, target, c, note)
            if resolved:
                return {"oversight": resolved}
        o = _open_case(db, user, target or "model-001", f"CASE_MGR · {c}" + (f" — {note}" if note else ""), "CASE_MGR_ACTION")
        o["action"] = c
        return {"oversight": o}

    if k == "WELFARE" and c in ("Approve Grant", "Verify Beneficiary", "Investigate Fraud", "Disburse"):
        if c == "Disburse" and target and target.upper().startswith("COB-"):
            resolved = _resolve_case(db, user, target, c, note)
            if resolved:
                return {"oversight": resolved}
        o = _open_case(db, user, target or "model-001", f"WELFARE · {c}" + (f" — {note}" if note else ""), "WELFARE_ACTION")
        o["action"] = c
        return {"oversight": o}

    if k == "SARS" and c in ("Initiate Audit", "Verify Return", "Issue Assessment", "Close Case"):
        if c == "Close Case" and target and target.upper().startswith("COB-"):
            resolved = _resolve_case(db, user, target, c, note)
            if resolved:
                return {"oversight": resolved}
        o = _open_case(db, user, target or "model-001", f"SARS · {c}" + (f" — {note}" if note else ""), "SARS_ACTION")
        o["action"] = c
        return {"oversight": o}

    if k in LIVE_AUDIT_PORTALS:
        live = {"audit": {"portal": k, "control": c, "model_id": target or "model-001", "note": note or ""}}
        append_audit(db, f"{k}_CONTROL", live["audit"], classification="OPERATIONS",
                     actor_class=user.get("role", "client"))
        return live

    return None


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
    if k in LIVE_CASE_PORTALS:
        out["live"]["oversight_cases"] = _oversight_list(db)
        out["live"]["mode"] = "oversight"
    elif k in LIVE_AUDIT_PORTALS:
        out["live"]["mode"] = "audit"
        out["live"]["tip"] = "Target = model id (prefer model-001). Controls write audit on Core."
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
