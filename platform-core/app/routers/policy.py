"""
Policy-to-Code API — UDOC governance protocol layer.

A client uploads passed/applicable legislation (PDF/DOCX/TXT). UDOC compiles candidate
machine-enforceable rules (transparent, editable). A compliance officer reviews and ACTIVATES
the pack; from then on the rules are enforced inside the non-bypassable EVA decision path.
"""
import hashlib, json, time
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import PolicyPack, PolicyRule, AIModel, PolicyVersion, Tenant
from app.core.dependencies import current_user, principal, scope_pk
from app.core.config import settings
from app.services import policy_engine as pe
from app.services.governance_bridge import Evidence, evaluate, seal_payload, verify_payload
from app.core.tiers import tier_info
from app.services.audit_writer import append_audit

router = APIRouter(prefix="/policy", tags=["Policy-to-Code · UDOC governance"])

_WRITE = {"admin", "operator", "gov"}


def _require_write(user: dict):
    if user.get("role") not in _WRITE and not (user.get("tenant_pk") and user.get("role") != "viewer"):
        raise HTTPException(403, "policy authoring requires a tenant client or operator / gov / admin role")


def _pack_out(p: PolicyPack) -> dict:
    return {"id": p.id, "name": p.name, "source_filename": p.source_filename, "jurisdiction": p.jurisdiction,
            "sector": p.sector, "status": p.status, "uploaded_by": p.uploaded_by, "sha256": p.sha256,
            "summary": p.summary, "rule_count": p.rule_count, "created_at": p.created_at.isoformat() if p.created_at else None,
            "activated_at": p.activated_at.isoformat() if p.activated_at else None}


def _rule_out(r: PolicyRule) -> dict:
    return {"id": r.id, "pack_id": r.pack_id, "code": r.code, "kind": r.kind, "severity": r.severity,
            "operator": r.operator, "threshold": r.threshold, "target": r.target, "description": r.description,
            "source_excerpt": r.source_excerpt, "confidence": r.confidence, "enabled": r.enabled}


@router.post("/upload")
async def upload(file: UploadFile = File(...), name: str = Form(...),
                 jurisdiction: str = Form("ZA"), sector: str = Form("GENERAL"),
                 db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    data = await file.read()
    if len(data) > 5_000_000:
        raise HTTPException(413, "policy file too large (5MB max on free tier)")
    text = pe.extract_text(file.filename or "policy.txt", data)
    rules = pe.extract_rules(text)
    summary = pe.summarise(text, rules)
    sha = hashlib.sha256(data).hexdigest()
    pack = PolicyPack(name=name[:200], source_filename=(file.filename or "policy.txt")[:200],
                      jurisdiction=jurisdiction[:40], sector=sector[:40], status="DRAFT",
                      uploaded_by=user.get("sub", ""), sha256=sha, summary=summary,
                      rule_count=len(rules), tenant_pk=user.get("tenant_pk"))
    db.add(pack); db.flush()
    for r in rules:
        db.add(PolicyRule(pack_id=pack.id, code=r["code"], kind=r["kind"], severity=r["severity"],
                          operator=r.get("operator") or "", threshold=r.get("threshold"),
                          target=r.get("target") or "", description=r.get("description") or "",
                          source_excerpt=r.get("source_excerpt") or "", confidence=r.get("confidence"),
                          enabled=True))
    db.commit(); db.refresh(pack)
    append_audit(db, "POLICY_UPLOAD", {"pack": pack.id, "rules": len(rules), "name": name},
                 actor_class=user.get("role", "SYSTEM"))
    return {"pack": _pack_out(pack), "rules": [_rule_out(r) for r in db.execute(
        select(PolicyRule).where(PolicyRule.pack_id == pack.id)).scalars().all()],
            "note": "Draft compiled from your document. Review/edit rules, then activate to enforce."}


@router.get("/packs")
def list_packs(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(PolicyPack).order_by(PolicyPack.id.desc())
    if scope == -1:
        q = q.where(PolicyPack.tenant_pk.is_(None))
    elif scope is not None:
        q = q.where(or_(PolicyPack.tenant_pk == scope, PolicyPack.tenant_pk.is_(None)))
    return [_pack_out(p) for p in db.execute(q).scalars().all()]


@router.get("/packs/{pack_id}")
def get_pack(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    rules = db.execute(select(PolicyRule).where(PolicyRule.pack_id == pack_id)).scalars().all()
    return {"pack": _pack_out(p), "rules": [_rule_out(r) for r in rules]}


class RulePatch(BaseModel):
    enabled: bool = None
    severity: str = None
    threshold: float = None
    description: str = None


@router.patch("/rules/{rule_id}")
def patch_rule(rule_id: int, patch: RulePatch, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    r = db.get(PolicyRule, rule_id)
    if not r:
        raise HTTPException(404, "rule not found")
    if patch.enabled is not None:
        r.enabled = patch.enabled
    if patch.severity is not None:
        r.severity = patch.severity[:20]
    if patch.threshold is not None:
        r.threshold = patch.threshold
    if patch.description is not None:
        r.description = patch.description[:400]
    pe.invalidate()
    db.commit(); db.refresh(r)
    return _rule_out(r)


@router.post("/packs/{pack_id}/activate")
def activate(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    if _requires_cob(db, p) and user.get("role") not in _COB:
        raise HTTPException(409, "this tier requires COB sign-off — POST /policy/packs/{id}/submit, "
                            "then POST /policy/versions/{vid}/approve as gov/admin")
    p.status = "ACTIVE"
    p.activated_at = datetime.now(timezone.utc)
    pe.invalidate()
    db.commit(); db.refresh(p)
    cnt = db.execute(select(PolicyRule).where(PolicyRule.pack_id == pack_id, PolicyRule.enabled == True)).scalars().all()  # noqa: E712
    append_audit(db, "POLICY_ACTIVATE", {"pack": pack_id, "active_rules": len(cnt)},
                 actor_class=user.get("role", "SYSTEM"))
    return {"pack": _pack_out(p), "active_rules": len(cnt),
            "note": "Pack ACTIVE — policy-to-code enforced on next EVA decision (hot-reload)."}


@router.post("/packs/{pack_id}/archive")
def archive(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    p.status = "ARCHIVED"
    pe.invalidate()
    db.commit(); db.refresh(p)
    append_audit(db, "POLICY_ARCHIVE", {"pack": pack_id}, actor_class=user.get("role", "SYSTEM"))
    return {"pack": _pack_out(p)}


@router.get("/active")
def active(db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Active packs + enforced rule set (dicts from policy_engine — never ORM attributes)."""
    scope = scope_pk(user)
    pq = select(PolicyPack).where(PolicyPack.status == "ACTIVE")
    if scope == -1:
        pq = pq.where(PolicyPack.tenant_pk.is_(None))
    elif scope is not None:
        pq = pq.where(or_(PolicyPack.tenant_pk == scope, PolicyPack.tenant_pk.is_(None)))
    packs = db.execute(pq).scalars().all()
    rules = pe.active_rules(db, tenant_pk=(scope if scope and scope != -1 else None))
    kinds: dict = {}
    for r in rules:
        kind = (r.get("kind") if isinstance(r, dict) else getattr(r, "kind", None)) or "UNKNOWN"
        kinds[kind] = kinds.get(kind, 0) + 1
    return {
        "active_packs": [_pack_out(p) for p in packs],
        "enforced_rules": len(rules),
        "by_kind": kinds,
        "rules": [
            {
                "code": r.get("code") if isinstance(r, dict) else getattr(r, "code", ""),
                "kind": r.get("kind") if isinstance(r, dict) else getattr(r, "kind", ""),
                "severity": r.get("severity") if isinstance(r, dict) else getattr(r, "severity", ""),
                "description": (r.get("description") if isinstance(r, dict) else getattr(r, "description", "")) or "",
                "threshold": r.get("threshold") if isinstance(r, dict) else getattr(r, "threshold", None),
            }
            for r in rules
        ],
        "hot_reload": pe.hot_reload_stats(),
        "note": "Rules compiled from uploaded packs (policy-to-code). EVA matrix uses apply() at decision time.",
    }


class PolicyTestReq(BaseModel):
    model_id: str = "model-001"
    scenario: str = "fair"  # fair | biased | high | sov | healthy | breach


def _scenario_evidence(model_id: str, risk_tier: str, scenario: str) -> Evidence:
    """Build Evidence matching EVA matrix chips used by /decisions/batch."""
    kw = {"model_id": model_id, "risk_tier": risk_tier or "NOTABLE", "raw_confidence": 0.92, "compliance": 1.0}
    sc = (scenario or "fair").lower()
    if sc in ("fair", "healthy"):
        kw.update(raw_confidence=0.94, compliance=1.0)
    elif sc == "biased":
        kw.update(raw_confidence=0.88, compliance=0.95,
                  priv_favorable=900, priv_total=1000, unpriv_favorable=120, unpriv_total=1000)
    elif sc == "high":
        kw.update(risk_tier="HIGH", raw_confidence=0.7, compliance=0.85)
    elif sc in ("sov", "breach", "sovereignty"):
        kw.update(bgp=0.4, traceroute=0.5, dnssec=0.6, storage=0.7)
    return Evidence(**kw)


@router.post("/test")
def test(req: PolicyTestReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Dry-run: EVA + active policy on one scenario WITHOUT persisting a decision."""
    model = db.execute(select(AIModel).where(AIModel.model_id == req.model_id)).scalar_one_or_none()
    if not model:
        raise HTTPException(404, "model not registered")
    ev = _scenario_evidence(req.model_id, model.risk_tier, req.scenario)
    v = evaluate(ev)
    pol = pe.apply(db, ev, model, v)
    return {
        "model_id": req.model_id,
        "scenario": req.scenario,
        "base_decision": v.decision,
        "final_decision": pol["adjusted_decision"],
        "composite_eva": getattr(v, "composite_eva", None),
        "dimensions": getattr(v, "dimensions", None),
        "rules_evaluated": pol["rules_evaluated"],
        "policy_enforced": pol["policy_enforced"],
        "fired": pol["fired"],
        "findings": pol["findings"],
    }


class RuntimeMatrixReq(BaseModel):
    model_id: str = "model-001"
    options: list = None  # default fair/biased/high/sov


@router.post("/runtime-matrix")
def runtime_matrix(req: RuntimeMatrixReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Full EVA × policy-to-code matrix against ACTIVE uploaded packs (no decision rows written).

    Shows how each scenario is scored by EVA and which compiled rules fire — the runtime
    link between policy upload → extract_rules → activate → apply() at decision time.
    """
    model = db.execute(select(AIModel).where(AIModel.model_id == req.model_id)).scalar_one_or_none()
    if not model:
        raise HTTPException(404, "model not registered — fail-closed")
    opts = req.options or ["fair", "biased", "high", "sov"]
    rules = pe.active_rules(db, jurisdiction=getattr(model, "jurisdiction", "ZA"),
                            tenant_pk=getattr(model, "tenant_pk", None))
    results = []
    for sc in opts:
        try:
            ev = _scenario_evidence(req.model_id, model.risk_tier, str(sc))
            v = evaluate(ev)
            pol = pe.apply(db, ev, model, v)
            fired = pol.get("fired") or []
            results.append({
                "option": sc,
                "ok": True,
                "base_decision": v.decision,
                "decision": pol["adjusted_decision"],
                "composite_eva": getattr(v, "composite_eva", None),
                "policy_enforced": pol["policy_enforced"],
                "rules_evaluated": pol["rules_evaluated"],
                "fired_count": len(fired),
                "fired": fired,
                "block_reasons": [f.get("message") or f.get("msg") or str(f) for f in fired][:6],
            })
        except Exception as e:
            results.append({"option": sc, "ok": False, "error": str(e)[:200]})
    outcomes = {"APPROVE": 0, "BLOCK": 0, "ESCALATE": 0, "OTHER": 0, "ERROR": 0}
    for r in results:
        if not r.get("ok"):
            outcomes["ERROR"] += 1
            continue
        d = str(r.get("decision") or "").upper()
        if d in outcomes:
            outcomes[d] += 1
        else:
            outcomes["OTHER"] += 1
    fair = next((r for r in results if r.get("option") == "fair"), None)
    biased = next((r for r in results if r.get("option") == "biased"), None)
    gate = {
        "fair_neq_block": bool(fair and fair.get("ok") and str(fair.get("decision")).upper() != "BLOCK"),
        "biased_eq_block": bool(biased and biased.get("ok") and str(biased.get("decision")).upper() == "BLOCK"),
    }
    return {
        "model_id": req.model_id,
        "active_rule_count": len(rules),
        "active_rule_kinds": sorted({(r.get("kind") if isinstance(r, dict) else "") for r in rules}),
        "results": results,
        "outcomes": outcomes,
        "gate": gate,
        "hot_reload": pe.hot_reload_stats(),
        "note": "Dry-run matrix: EVA evaluate() + policy_engine.apply() on ACTIVE packs. "
                "Upload → extract_rules → activate → this matrix. Persist via POST /decisions/batch.",
    }


# ─────────────────── Policy versioning + COB approval workflow + hot-reload ───────────────────
_COB = {"gov", "admin"}


def _requires_cob(db: Session, pack: PolicyPack) -> bool:
    if pack.tenant_pk is None:
        return True  # platform / sovereign packs always require COB sign-off
    return False


def _next_version(db: Session, pack_id: int) -> int:
    rows = db.execute(select(PolicyVersion).where(PolicyVersion.pack_id == pack_id)).scalars().all()
    return (max((v.version for v in rows), default=0) + 1)


def _freeze(db: Session, pack: PolicyPack, user: dict, state: str, reviewed_by: str = "", note: str = ""):
    ver = PolicyVersion(pack_id=pack.id, version=_next_version(db, pack.id), state=state,
                        author=user.get("sub", ""), reviewed_by=reviewed_by, note=note[:400])
    db.add(ver); db.commit(); db.refresh(ver)
    return ver


def _version_out(v: PolicyVersion) -> dict:
    return {"id": v.id, "pack_id": v.pack_id, "version": v.version, "state": v.state,
            "author": v.author, "reviewed_by": v.reviewed_by, "note": v.note,
            "created_at": v.created_at.isoformat() if v.created_at else None}


@router.post("/packs/{pack_id}/submit")
def submit_pack(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    ver = _freeze(db, p, user, "PROPOSED")
    append_audit(db, "POLICY_SUBMIT", {"pack": pack_id, "version": ver.version}, actor_class=user.get("role", "SYSTEM"))
    return {"pack": _pack_out(p), "version": _version_out(ver)}


@router.post("/versions/{vid}/approve")
def approve_version(vid: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    if user.get("role") not in _COB:
        raise HTTPException(403, "COB approval requires gov or admin")
    v = db.get(PolicyVersion, vid)
    if not v:
        raise HTTPException(404, "version not found")
    p = db.get(PolicyPack, v.pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    v.state = "APPROVED"; v.reviewed_by = user.get("sub", "")
    p.status = "ACTIVE"; p.current_version = v.version; p.activated_at = datetime.now(timezone.utc)
    pe.invalidate()
    db.commit(); db.refresh(v); db.refresh(p)
    append_audit(db, "POLICY_APPROVE", {"pack": p.id, "version": v.version}, actor_class=user.get("role", "SYSTEM"))
    return {"pack": _pack_out(p), "version": _version_out(v)}


class VetoReq(BaseModel):
    note: str = ""


@router.post("/versions/{vid}/veto")
def veto_version(vid: int, body: VetoReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    if user.get("role") not in _COB:
        raise HTTPException(403, "COB veto requires gov or admin")
    v = db.get(PolicyVersion, vid)
    if not v:
        raise HTTPException(404, "version not found")
    v.state = "VETOED"; v.reviewed_by = user.get("sub", ""); v.note = (body.note or "")[:400]
    p = db.get(PolicyPack, v.pack_id)
    if p:
        p.status = "DRAFT"
    pe.invalidate()
    db.commit(); db.refresh(v)
    append_audit(db, "POLICY_VETO", {"version": vid, "note": body.note}, actor_class=user.get("role", "SYSTEM"))
    return {"version": _version_out(v)}


@router.get("/versions")
def list_versions(pack_id: int = None, db: Session = Depends(get_db), user: dict = Depends(principal)):
    q = select(PolicyVersion).order_by(PolicyVersion.id.desc())
    if pack_id is not None:
        q = q.where(PolicyVersion.pack_id == pack_id)
    return [_version_out(v) for v in db.execute(q).scalars().all()]


@router.get("/versions/{vid}")
def get_version(vid: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    v = db.get(PolicyVersion, vid)
    if not v:
        raise HTTPException(404, "version not found")
    return _version_out(v)


@router.post("/hot-reload")
def hotreload(user: dict = Depends(principal)):
    pe.invalidate()
    return {"ok": True, "stats": pe.hot_reload_stats(), "note": "Active rule cache cleared — next decision reloads from Neon."}
