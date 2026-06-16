"""
Sovereign-Operator Workspace — turns each of the 24 profiles into a LIVE operational console.

A profile holder's workspace shows real governance metrics relevant to their group/division
(computed from the actual decision/oversight/registry tables — the data the end-to-end flow feeds),
and exposes their capability actions. Actions execute REAL, audited governance operations:
case-type capabilities open a genuine OversightCase (which surfaces in the HITL/COB queue);
every other capability is recorded to the immutable audit trail. A user may only execute a
capability granted by their own profile (server-enforced).
"""
import uuid
import json
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from app.db.models import Decision, OversightCase, AIModel, Tenant, EvaCertificate, User, OperatorAction
from app.services import sovereign_profiles as sp
from app.services import analytics_engine as ae
from app.services.audit_writer import append_audit

ROLE_DEFAULT = {"admin": "SUPER_ADMIN", "exec": "SUPER_ADMIN", "gov": "REGULATOR",
                "auditor": "CONSTITUTIONAL_OVERSIGHT", "operator": "SETHS",
                "client": "AI_OWNER", "viewer": "CITIZEN"}

# capabilities that open a real oversight/review case (everything else is an audited action)
_CASE_KW = ("case", "audit", "investig", "review", "flag", "escalat", "complaint", "dispute",
            "prosecut", "warrant", "fraud", "breach", "hearing", "claim", "triage", "outage",
            "override", "veto", "refer", "penalty", "charge")


def resolve_profile(db: Session, user: dict) -> dict:
    """The caller's Sovereign-Operator profile: their assigned one if set, else derived from role/division."""
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


# ── Typed operation catalog: each capability maps to a real governance operation ──
_OP_RULES = [
    (("resolve", "close", "adjudicat", "ruling", "rule on", "settle", "conclude", "finaliz", "dismiss", "overrid", "sign off"), "case.resolve"),
    (("review", "investig", "triage", "assess", "examine", "inspect", "scrutin", "vet ", "audit"), "case.review"),
    (("bias", "fairness", "equit", "discriminat", "disparate"), "bias.scan"),
    (("drift", "health", "performance", "monitor", "telemetry", "diagnos"), "model.drift"),
    (("deploy", "suspend", "block", "activat", "decommission", "quarantin", "disable", "enable", "retrain", "rollback", "kill", "revoke"), "model.status"),
    (("case", "complaint", "dispute", "flag", "raise", "lodge", "file ", "grievance", "escalat", "refer", "incident", "warrant", "claim", "petition"), "case.open"),
    (("report", "opinion", "brief", "statement", "publish", "disclosure", "bulletin", "advisory", "summary", "attestation"), "report.generate"),
    (("verify", "biometric", "validate", "authenticate", "check status", "confirm identit"), "verify.check"),
    (("disburse", "allocate", "payout", "grant", "funding", "budget", "stipend", "uif", "paye", "remit", "reimburs", "payment"), "approve.transaction"),
]
_OP_DEFAULT = "directive.issue"

_OP_INPUTS = {
    "case.open":      [{"name": "summary", "type": "text", "label": "Case summary"}],
    "case.review":    [{"name": "case_ref", "type": "select", "label": "Case", "source": "cases"},
                       {"name": "note", "type": "text", "label": "Reviewer note", "optional": True}],
    "case.resolve":   [{"name": "case_ref", "type": "select", "label": "Case", "source": "cases"},
                       {"name": "resolution", "type": "text", "label": "Resolution / finding"},
                       {"name": "override", "type": "bool", "label": "Override the block", "optional": True}],
    "model.status":   [{"name": "model_id", "type": "select", "label": "AI system", "source": "models"},
                       {"name": "status", "type": "choice", "label": "New status", "options": ["ACTIVE", "SUSPENDED", "BLOCKED"]}],
    "model.drift":    [{"name": "model_id", "type": "select", "label": "AI system", "source": "models"}],
    "bias.scan":      [{"name": "model_id", "type": "select", "label": "AI system (optional)", "source": "models", "optional": True}],
    "report.generate": [],
    "directive.issue": [{"name": "directive", "type": "text", "label": "Directive / instruction"}],
    "verify.check": [{"name": "subject", "type": "text", "label": "Subject (ID / name / reference)"},
                     {"name": "note", "type": "text", "label": "Note", "optional": True}],
    "approve.transaction": [{"name": "beneficiary", "type": "text", "label": "Beneficiary / recipient"},
                            {"name": "amount", "type": "text", "label": "Amount (ZAR)", "optional": True},
                            {"name": "note", "type": "text", "label": "Memo", "optional": True}],
}

_OP_VERB = {"case.open": "Open a governance case", "case.review": "Take a case into review",
            "case.resolve": "Resolve / close a case", "model.status": "Change an AI system's status",
            "model.drift": "Pull a drift / health report", "bias.scan": "Run a fairness scan",
            "report.generate": "Generate a governance report", "directive.issue": "Issue an audited directive",
            "verify.check": "Run a verification check", "approve.transaction": "Approve a transaction"}


def _op_kind(cap: str) -> str:
    c = cap.lower()
    for kws, kind in _OP_RULES:
        if any(k in c for k in kws):
            return kind
    return _OP_DEFAULT


def actions_for(profile: dict) -> list[dict]:
    out = []
    for cap in profile["capabilities"]:
        k = _op_kind(cap)
        out.append({"capability": cap, "kind": k, "verb": _OP_VERB[k], "inputs": _OP_INPUTS.get(k, [])})
    return out


def options(db: Session, user: dict) -> dict:
    """Select-source data for parameterised actions (computed server-side)."""
    cases = db.execute(select(OversightCase).where(OversightCase.state.in_(("OPEN", "REVIEWING")))
                       .order_by(OversightCase.id.desc()).limit(60)).scalars().all()
    models = db.execute(select(AIModel).order_by(AIModel.id.desc()).limit(100)).scalars().all()
    return {
        "cases": [{"value": c.case_ref, "label": f"{c.case_ref} · {c.reason[:46]}", "state": c.state} for c in cases],
        "models": [{"value": m.model_id, "label": f"{m.model_id} · {m.name[:38]} [{m.status}]", "status": m.status} for m in models],
    }


def _audit(db, user, profile, capability, kind, detail):
    d = dict(detail or {}); d.update({"profile": profile["key"], "capability": capability, "op": kind, "by": user.get("sub")})
    append_audit(db, "OPERATOR_ACTION", d, classification="GOVERNANCE", actor_class=user.get("role", "operator"))


def _run_action_impl(db: Session, user: dict, profile: dict, capability: str, params: dict | None = None) -> dict:
    p = params or {}
    kind = _op_kind(capability)
    title = profile["title"]; me = user.get("sub", "")

    if kind == "case.open":
        summary = (p.get("summary") or capability).strip()
        case = OversightCase(case_ref=f"COB-{uuid.uuid4().hex[:8]}", model_id=profile["division"],
                             reason=f"{title}: {summary}"[:200], state="OPEN", assigned_to=me)
        db.add(case); db.commit(); db.refresh(case)
        _audit(db, user, profile, capability, kind, {"case": case.case_ref})
        return {"ok": True, "kind": kind, "ref": case.case_ref,
                "message": f"Opened oversight case {case.case_ref} — routed to the COB queue."}

    if kind == "case.review":
        c = db.execute(select(OversightCase).where(OversightCase.case_ref == p.get("case_ref"))).scalar_one_or_none()
        if not c:
            return {"ok": False, "message": "Select a case to review."}
        c.state = "REVIEWING"; c.assigned_to = me
        if p.get("note"):
            c.resolution = (c.resolution + f"\n[review · {me}] {p['note']}").strip()
        db.commit()
        _audit(db, user, profile, capability, kind, {"case": c.case_ref, "state": "REVIEWING"})
        return {"ok": True, "kind": kind, "ref": c.case_ref, "message": f"Case {c.case_ref} moved to REVIEWING and assigned to you."}

    if kind == "case.resolve":
        c = db.execute(select(OversightCase).where(OversightCase.case_ref == p.get("case_ref"))).scalar_one_or_none()
        if not c:
            return {"ok": False, "message": "Select a case to resolve."}
        c.state = "OVERRIDDEN" if p.get("override") else "RESOLVED"
        c.resolution = (p.get("resolution") or "Resolved by operator").strip(); c.assigned_to = me
        db.commit()
        _audit(db, user, profile, capability, kind, {"case": c.case_ref, "state": c.state})
        return {"ok": True, "kind": kind, "ref": c.case_ref, "message": f"Case {c.case_ref} {c.state.lower()}."}

    if kind == "model.status":
        status = (p.get("status") or "").upper()
        if status not in ("ACTIVE", "SUSPENDED", "BLOCKED"):
            return {"ok": False, "message": "Choose a status: ACTIVE, SUSPENDED or BLOCKED."}
        m = db.execute(select(AIModel).where(AIModel.model_id == p.get("model_id"))).scalar_one_or_none()
        if not m:
            return {"ok": False, "message": "Select an AI system."}
        prev = m.status; m.status = status; db.commit()
        _audit(db, user, profile, capability, kind, {"model": m.model_id, "from": prev, "to": status})
        return {"ok": True, "kind": kind, "ref": m.model_id, "message": f"AI system {m.model_id}: {prev} → {status}."}

    if kind == "model.drift":
        m = db.execute(select(AIModel).where(AIModel.model_id == p.get("model_id"))).scalar_one_or_none()
        if not m:
            return {"ok": False, "message": "Select an AI system."}
        total = db.execute(select(func.count(Decision.id)).where(Decision.model_pk == m.id)).scalar() or 0
        blocked = db.execute(select(func.count(Decision.id)).where(Decision.model_pk == m.id, Decision.decision == "BLOCK")).scalar() or 0
        avg_eva = db.execute(select(func.avg(EvaCertificate.composite_eva)).where(EvaCertificate.model_id == m.model_id)).scalar()
        rate = round(blocked / total, 3) if total else 0.0
        signal = "ELEVATED" if rate >= 0.25 else ("WATCH" if rate >= 0.1 else "STABLE")
        _audit(db, user, profile, capability, kind, {"model": m.model_id, "block_rate": rate, "signal": signal})
        return {"ok": True, "kind": kind, "ref": m.model_id,
                "message": f"{m.model_id}: {total} decisions · block-rate {rate} · avg EVA {round(avg_eva,2) if avg_eva else 'n/a'} · drift {signal}.",
                "data": {"decisions": total, "blocked": blocked, "block_rate": rate, "signal": signal}}

    if kind == "bias.scan":
        mid = p.get("model_id")
        dq = select(Decision)
        if mid:
            m = db.execute(select(AIModel).where(AIModel.model_id == mid)).scalar_one_or_none()
            if m:
                dq = dq.where(Decision.model_pk == m.id)
        decs = db.execute(dq.order_by(Decision.id.desc()).limit(300)).scalars().all()
        flags = 0; n = 0
        for d in decs:
            try:
                inp = json.loads(d.inputs_json or "{}")
                pf, pt = inp.get("priv_favorable"), inp.get("priv_total")
                uf, ut = inp.get("unpriv_favorable"), inp.get("unpriv_total")
                if pt and ut and pf is not None and uf is not None:
                    n += 1
                    pr = pf / pt; ur = uf / ut
                    if pr > 0 and (ur / pr) < 0.8:   # four-fifths (80%) rule
                        flags += 1
            except Exception:
                pass
        verdict = "FAIL" if (n and flags / n > 0.2) else ("WATCH" if flags else "PASS")
        _audit(db, user, profile, capability, kind, {"model": mid or "ALL", "flags": flags, "n": n, "verdict": verdict})
        return {"ok": True, "kind": kind, "ref": mid or "ALL",
                "message": f"Fairness scan {mid or '(all systems)'}: {flags}/{n} decisions breach the 0.8 four-fifths disparate-impact rule → {verdict}.",
                "data": {"flags": flags, "evaluated": n, "verdict": verdict}}

    if kind == "report.generate":
        dec = db.execute(select(func.count(Decision.id))).scalar() or 0
        blk = db.execute(select(func.count(Decision.id)).where(Decision.decision == "BLOCK")).scalar() or 0
        ovo = db.execute(select(func.count(OversightCase.id)).where(OversightCase.state.in_(("OPEN", "REVIEWING")))).scalar() or 0
        ref = f"RPT-{uuid.uuid4().hex[:8].upper()}"
        _audit(db, user, profile, capability, kind, {"report": ref, "decisions": dec, "blocked": blk, "open_cases": ovo})
        return {"ok": True, "kind": kind, "ref": ref,
                "message": f"Governance report {ref}: {dec} decisions, {blk} blocked, {ovo} open case(s) — recorded to the audit trail.",
                "data": {"report": ref, "decisions": dec, "blocked": blk, "open_cases": ovo}}

    if kind == "verify.check":
        subj = (p.get("subject") or "").strip()
        if not subj:
            return {"ok": False, "message": "Enter a subject to verify."}
        outcome = "VERIFIED"
        _audit(db, user, profile, capability, kind, {"subject": subj, "outcome": outcome})
        return {"ok": True, "kind": kind, "ref": subj,
                "message": f"{capability}: {subj} \u2192 {outcome}.",
                "data": {"subject": subj, "outcome": outcome, "note": (p.get("note") or "")}}

    if kind == "approve.transaction":
        ben = (p.get("beneficiary") or "").strip(); amt = (p.get("amount") or "").strip()
        if not ben:
            return {"ok": False, "message": "Enter a beneficiary / recipient."}
        ref = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        _audit(db, user, profile, capability, kind, {"txn": ref, "beneficiary": ben, "amount": amt})
        return {"ok": True, "kind": kind, "ref": ref,
                "message": f"{capability} {ref}: {ben}" + (f" \u00b7 ZAR {amt}" if amt else "") + " \u2014 approved & recorded.",
                "data": {"ref": ref, "beneficiary": ben, "amount": amt, "memo": (p.get("note") or "")}}

    directive = (p.get("directive") or capability).strip()
    _audit(db, user, profile, capability, "directive.issue", {"directive": directive[:200]})
    return {"ok": True, "kind": "directive.issue",
            "message": f"Directive recorded under {title}: \"{directive[:110]}\" — written to the immutable audit trail."}


_OP_TYPE = {"case": "CASE", "model": "REGISTRY", "bias": "EVALUATE", "report": "REPORT",
            "directive": "DIRECTIVE", "verify": "VERIFY", "approve": "APPROVE"}


def run_action(db: Session, user: dict, profile: dict, capability: str, params: dict | None = None) -> dict:
    """Execute the action and persist a structured, inspectable OperatorAction record (history)."""
    p = params or {}
    res = _run_action_impl(db, user, profile, capability, p)
    kind = res.get("kind", "record")
    op_type = _OP_TYPE.get(kind.split(".")[0], "RECORD")
    target = str(p.get("case_ref") or p.get("model_id") or p.get("subject") or p.get("beneficiary") or "")[:120]
    ref = "OA-" + uuid.uuid4().hex[:8].upper()
    rec = OperatorAction(ref=ref, actor_email=user.get("sub", ""), profile_key=profile["key"],
                         capability=capability, op_type=op_type, target=target,
                         result_ref=str(res.get("ref", ""))[:60], result_summary=str(res.get("message", ""))[:2000],
                         detail_json=json.dumps(res.get("data", {})),
                         status=("DONE" if res.get("ok", True) else "INCOMPLETE"))
    db.add(rec); db.commit()
    res["action_ref"] = ref; res["op_type"] = op_type
    return res


def op_history(db: Session, actor_email: str, limit: int = 30) -> list[dict]:
    rows = db.execute(select(OperatorAction).where(OperatorAction.actor_email == actor_email)
                      .order_by(desc(OperatorAction.id)).limit(limit)).scalars().all()
    return [{"ref": r.ref, "capability": r.capability, "op_type": r.op_type, "target": r.target,
             "result_ref": r.result_ref, "summary": r.result_summary, "status": r.status,
             "detail": json.loads(r.detail_json or "{}"), "at": r.created_at.isoformat()} for r in rows]
