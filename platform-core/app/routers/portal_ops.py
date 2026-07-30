"""
Portal Operations API — 24 Sovereign-Operator portals as LIVE operable consoles.

- GET  /portal/{key}            → profile + controls + activity + live panel
- POST /portal/{key}/control    → audit-linked action + dual-path OversightCase / audit
- GET  /portal/{key}/activity   → recent operations

Neon-light: reuses OversightCase only — no new tables, no new Render services.
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

# Case-bearing portals: every control opens OversightCase unless it is a resolve control + COB- target
LIVE_CASE_PORTALS = {
    "HITL_REVIEW", "REGULATOR", "INFO_REGULATOR", "SAHRC", "CASE_MANAGER",
    "WELFARE", "SARS", "CONSTITUTIONAL_OVERSIGHT",
    "BORDER", "DHA", "SERVICE_DELIVERY", "MUNICIPAL", "JUSTICE", "NPA", "HEALTH",
    "SETHS", "EMPLOYER", "MADIBA", "INSURANCE", "DCDT_POLICY", "SUPER_ADMIN",
}

# Resolve when Target is an existing COB- case_ref
RESOLVE_CONTROLS = {
    "Approve AI Decision", "Override", "Release", "Close Case", "Close Matter",
    "Publish Finding", "Disburse", "Withdraw Case", "Archive Case", "Resolve",
    "Close Feedback", "Release Hold", "Approve Payout", "Certify",
}

# Audit-only (no OversightCase row)
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
        reason=(reason or "portal action")[:500],
    )
    db.add(oc)
    db.commit()
    db.refresh(oc)
    append_audit(
        db, audit_evt,
        {"case": oc.case_ref, "model": mid, "reason": (reason or "")[:200]},
        classification="GOVERNANCE", actor_class=user.get("role", "operator"),
    )
    return {"case_ref": oc.case_ref, "state": oc.state, "model_id": mid}


def _resolve_case(db: Session, user: dict, case_ref: str, control: str, note: str) -> dict | None:
    case = db.execute(
        select(OversightCase).where(OversightCase.case_ref == case_ref)
    ).scalar_one_or_none()
    if not case:
        return None
    if any(x in control for x in ("Override", "Withdraw")):
        case.state = "OVERRIDDEN"
    else:
        case.state = "RESOLVED"
    case.resolution = note or control
    case.assigned_to = user.get("sub", "")
    db.commit()
    append_audit(
        db, "PORTAL_RESOLVE",
        {"case": case.case_ref, "control": control, "state": case.state},
        classification="GOVERNANCE", actor_class=user.get("role", "operator"),
    )
    return {"case_ref": case.case_ref, "state": case.state, "action": control}


def _live_side_effect(db: Session, user: dict, key: str, control: str, target: str, note: str) -> dict | None:
    """Map portal controls onto OversightCase or audit (Neon-light)."""
    k = (key or "").upper()
    c = (control or "").strip()

    if k in LIVE_CASE_PORTALS:
        # Resolve existing case when Target is COB-… and control is a close/resolve verb
        if c in RESOLVE_CONTROLS and target and target.upper().startswith("COB-"):
            resolved = _resolve_case(db, user, target, c, note)
            if resolved:
                return {"oversight": resolved}
            # fall through to open if case_ref unknown

        reason = f"{k} · {c}" + (f" — {note}" if note else "")
        o = _open_case(db, user, target or "model-001", reason, f"{k}_ACTION")
        o["action"] = c
        return {"oversight": o}

    if k in LIVE_AUDIT_PORTALS:
        live = {
            "audit": {
                "portal": k,
                "control": c,
                "model_id": target or "model-001",
                "note": note or "",
            }
        }
        append_audit(
            db, f"{k}_CONTROL", live["audit"],
            classification="OPERATIONS", actor_class=user.get("role", "client"),
        )
        return live

    # CITIZEN is UI-only; remaining unknown keys stay OperatorAction-only
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
        out["live"]["resolve_hint"] = (
            "Target = COB-… + resolve control (Close Case / Override / Resolve / …) closes the case. "
            "Otherwise every control opens a new OversightCase."
        )
    elif k in LIVE_AUDIT_PORTALS:
        out["live"]["mode"] = "audit"
        out["live"]["tip"] = "Target = model id (prefer model-001). Controls write audit on Core."
    elif k == "CITIZEN":
        out["live"]["mode"] = "citizen_ui"
        out["live"]["tip"] = "Use the Citizen interface — public /citizen/* APIs, not control forms."
    return out


@router.get("/{key}/activity", summary="Recent operations recorded against this portal")
def portal_activity(key: str, limit: int = 20, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    prof = sp.get(key)
    if not prof:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"unknown portal '{key}'")
    return {
        "portal": prof["key"],
        "title": prof["title"],
        "activity": _activity(db, prof["key"], min(limit, 100)),
    }


@router.post("/{key}/control", summary="Operate a control (audit-linked + live dual-path)")
def operate_control(
    key: str,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: dict = Depends(current_user),
):
    prof = sp.get(key)
    if not prof:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"unknown portal '{key}'")
    if not _may_operate(user, prof):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"This portal is operated by the '{prof['base_role']}' role; you are '{user.get('role')}'.",
        )
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
        ref=ref,
        actor_email=user.get("sub", ""),
        profile_key=prof["key"],
        capability=control,
        op_type=sp.op_type_for(control),
        target=target,
        result_ref=ref,
        result_summary=summary,
        detail_json=json.dumps({
            "portal": prof["title"], "control": control, "note": note,
            "by_role": user.get("role", ""), "group": prof["group"], "live": live,
        }),
        status="EXECUTED",
    )
    db.add(op)
    db.commit()
    db.refresh(op)
    return {
        "ref": ref,
        "portal": prof["title"],
        "portal_key": prof["key"],
        "control": control,
        "op_type": op.op_type,
        "status": "EXECUTED",
        "at": op.created_at.isoformat() if op.created_at else datetime.now(timezone.utc).isoformat(),
        "message": f"{control} executed on {prof['title']}.",
        "live": live,
    }
