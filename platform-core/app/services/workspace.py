"""
Sovereign-Operator Workspace — turns each of the 24 profiles into a LIVE operational console.

resolve_profile() maps the authenticated user to one of the 24 sovereign-operator profiles
(via their stored `profile` key, falling back to role/division defaults). tiles_for() renders
live KPI tiles for that profile's group, sourced from the real governance tables / analytics
engine. actions_for()/run_action() expose the profile's capabilities as server-enforced,
audited actions — case-like capabilities open a real OversightCase (HITL/COB queue), the rest
are recorded to the immutable audit trail.
"""
import uuid
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.models import Decision, OversightCase, AIModel, Tenant, EvaCertificate, User
from app.services import sovereign_profiles as sp
from app.services import analytics_engine as ae
from app.services.audit_writer import append_audit

ROLE_DEFAULT = {"admin": "SUPER_ADMIN", "exec": "SUPER_ADMIN", "gov": "REGULATOR",
                "auditor": "CONSTITUTIONAL_OVERSIGHT", "operator": "SETHS",
                "client": "AI_OWNER", "viewer": "CITIZEN"}

_CASE_KW = ("case", "audit", "investig", "review", "flag", "escalat", "complaint", "dispute",
            "prosecut", "warrant", "fraud", "breach", "hearing", "claim", "triage", "outage",
            "override", "veto", "refer", "penalty", "charge")


def resolve_profile(db: Session, user: dict) -> dict:
    u = db.execute(select(User).where(User.email == user.get("sub"))).scalar_one_or_none()
    pkey = (u.profile if u and u.profile else "") or ""
    if pkey.upper() in sp.PROFILES:
        return sp.PROFILES[pkey.upper()]
    role = (user.get("role") or "viewer"); div = (user.get("division") or "GODS")
    if role == "operator":
        for p in sp.PROFILES.values():
            if p["base_role"] == "operator" and p["division"] == div:
                return p
    return sp.PROFILES.get(ROLE_DEFAULT.get(role, "CITIZEN"), next(iter(sp.PROFILES.values())))


def _counts(db: Session) -> dict:
    g = lambda q: db.execute(q).scalar() or 0
    return {
        "decisions": g(select(func.count(Decision.id))),
        "blocked": g(select(func.count(Decision.id)).where(Decision.decision == "BLOCK")),
        "oversight_open": g(select(func.count(OversightCase.id)).where(OversightCase.state == "OPEN")),
        "models": g(select(func.count(AIModel.id))),
        "tenants": g(select(func.count(Tenant.id))),
        "certificates": g(select(func.count(EvaCertificate.id))),
    }


def tiles_for(db: Session, profile: dict) -> list[dict]:
    c = _counts(db); grp = profile["group"]; div = profile["division"]
    T = lambda k, v: {"k": k, "v": v}
    if grp == "GOVERNANCE":
        return [T("AI decisions", c["decisions"]), T("Blocked", c["blocked"]),
                T("Open oversight", c["oversight_open"]), T("Registered systems", c["models"]),
                T("EVA certificates", c["certificates"])]
    if grp == "OPERATIONS":
        k = ae.kpis(db, div if div in ("SETHS", "MADIBA", "TS", "UDOC") else "UDOC")
        tiles = [T(a, b) for a, b in list(k.items())[:4] if not isinstance(b, dict)]
        tiles.append(T("Open oversight", c["oversight_open"]))
        return tiles
    if grp == "PEOPLE":
        k = ae.kpis(db, "SETHS")
        tiles = [T(a, b) for a, b in list(k.items())[:3] if not isinstance(b, dict)]
        tiles += [T("Open oversight", c["oversight_open"]), T("AI decisions", c["decisions"])]
        return tiles
    # BUSINESS
    return [T("Registered systems", c["models"]), T("Tenants", c["tenants"]),
            T("AI decisions", c["decisions"]), T("EVA certificates", c["certificates"]),
            T("Blocked", c["blocked"])]


def _kind(cap: str) -> str:
    return "oversight" if any(k in cap.lower() for k in _CASE_KW) else "audited"


def actions_for(profile: dict) -> list[dict]:
    return [{"capability": cap, "kind": _kind(cap)} for cap in profile["capabilities"]]


def run_action(db: Session, user: dict, profile: dict, capability: str) -> dict:
    kind = _kind(capability)
    if kind == "oversight":
        case = OversightCase(case_ref=f"COB-{uuid.uuid4().hex[:8]}",
                             model_id=profile["division"],
                             reason=f"{profile['title']} · {capability}"[:200], state="OPEN")
        db.add(case); db.commit(); db.refresh(case)
        append_audit(db, "OPERATOR_ACTION",
                     {"profile": profile["key"], "capability": capability,
                      "case": case.case_ref, "by": user.get("sub")},
                     classification="GOVERNANCE", actor_class=user.get("role", "operator"))
        return {"ok": True, "kind": "oversight", "ref": case.case_ref,
                "message": f"Opened oversight case {case.case_ref} for '{capability}' — routed to the COB queue."}
    append_audit(db, "OPERATOR_ACTION",
                 {"profile": profile["key"], "capability": capability, "by": user.get("sub")},
                 classification="GOVERNANCE", actor_class=user.get("role", "operator"))
    return {"ok": True, "kind": "audited",
            "message": f"'{capability}' recorded to the immutable audit trail under {profile['title']}."}
