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
    return {"id": p.id, "name": p.name, "source_filename": p.source_filename,
            "jurisdiction": p.jurisdiction, "sector": p.sector, "status": p.status,
            "uploaded_by": p.uploaded_by, "sha256": p.sha256, "summary": p.summary,
            "rule_count": p.rule_count, "created_at": p.created_at.isoformat(),
            "activated_at": p.activated_at.isoformat() if p.activated_at else None}


def _rule_out(r: PolicyRule) -> dict:
    return {"id": r.id, "pack_id": r.pack_id, "code": r.code, "kind": r.kind, "target": r.target,
            "operator": r.operator, "threshold": r.threshold, "severity": r.severity,
            "description": r.description, "source_excerpt": r.source_excerpt,
            "confidence": r.confidence, "enabled": r.enabled}


@router.post("/upload")
async def upload(file: UploadFile = File(...), name: str = Form(...),
                 jurisdiction: str = Form("ZA"), sector: str = Form("GENERAL"),
                 db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    data = await file.read()
    if len(data) > 25 * 1024 * 1024:
        raise HTTPException(413, "file exceeds 25MB limit")
    text = pe.extract_text(file.filename or "policy.txt", data)
    rules = pe.extract_rules(text)
    sha = hashlib.sha256(data).hexdigest()
    _scope = scope_pk(user)
    pack = PolicyPack(name=name, source_filename=file.filename or "", jurisdiction=jurisdiction,
                      sector=sector, status="DRAFT", uploaded_by=user.get("sub", ""),
                      sha256=sha, summary=pe.summarise(text, rules), rule_count=len(rules),
                      tenant_pk=(_scope if (_scope and _scope != -1) else None))
    db.add(pack); db.commit(); db.refresh(pack)
    for r in rules:
        db.add(PolicyRule(pack_id=pack.id, **r))
    db.commit()
    append_audit(db, "POLICY_UPLOAD", {"pack": pack.id, "name": name, "rules": len(rules),
                 "sha256": sha[:16]}, classification="GOVERNANCE", actor_class=user.get("role", "SYSTEM"))
    rows = db.execute(select(PolicyRule).where(PolicyRule.pack_id == pack.id)).scalars().all()
    return {"pack": _pack_out(pack), "rules": [_rule_out(r) for r in rows],
            "note": "Draft compiled from your document. Review/edit rules, then activate to enforce."}


@router.get("/packs")
def list_packs(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(PolicyPack).order_by(PolicyPack.id.desc())
    if scope == -1:
        q = q.where(PolicyPack.tenant_pk.is_(None))
    elif scope is not None:
        q = q.where(or_(PolicyPack.tenant_pk == scope, PolicyPack.tenant_pk.is_(None)))
    rows = db.execute(q).scalars().all()
    return [_pack_out(p) for p in rows]


@router.get("/packs/{pack_id}")
def get_pack(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    scope = scope_pk(user)
    if scope is not None and scope != -1 and p.tenant_pk not in (None, scope):
        raise HTTPException(404, "pack not found")
    rows = db.execute(select(PolicyRule).where(PolicyRule.pack_id == pack_id)).scalars().all()
    return {"pack": _pack_out(p), "rules": [_rule_out(r) for r in rows]}


class RulePatch(BaseModel):
    enabled: bool | None = None
    severity: str | None = None
    kind: str | None = None
    threshold: float | None = None
    target: str | None = None
    description: str | None = None


@router.patch("/rules/{rule_id}")
def patch_rule(rule_id: int, patch: RulePatch, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    r = db.get(PolicyRule, rule_id)
    if not r:
        raise HTTPException(404, "rule not found")
    for k, v in patch.model_dump(exclude_none=True).items():
        setattr(r, k, v)
    db.commit(); pe.invalidate(); db.refresh(r)
    return _rule_out(r)


@router.post("/packs/{pack_id}/activate")
def activate(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    if _requires_cob(db, p) and user.get("role") not in _COB:
        raise HTTPException(409, "this tier requires COB sign-off — POST /policy/packs/{id}/submit, "
                                 "then a COB officer approves the version")
    for ov in db.execute(select(PolicyVersion).where(
            PolicyVersion.pack_id == pack_id, PolicyVersion.state == "ACTIVE")).scalars().all():
        ov.state = "SUPERSEDED"
    ver, cnt = _freeze(db, p, user, "ACTIVE", reviewed_by=user.get("sub", ""), note="fast-path activation")
    ver.decided_at = datetime.now(timezone.utc)
    p.status = "ACTIVE"; p.current_version = ver.version; p.activated_at = datetime.now(timezone.utc)
    db.commit(); pe.invalidate()
    append_audit(db, "POLICY_ACTIVATE", {"pack": pack_id, "version": ver.version, "active_rules": cnt,
                 "content_hash": ver.content_hash[:16]}, classification="GOVERNANCE", actor_class=user.get("role", "SYSTEM"))
    return {"pack": _pack_out(p), "version": _version_out(ver), "active_rules": cnt,
            "hot_reload": pe.hot_reload_stats(), "note": "Pack ACTIVE and hot-reloaded into the live EVA path."}


@router.post("/packs/{pack_id}/archive")
def archive(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    p.status = "ARCHIVED"; db.commit(); pe.invalidate()
    append_audit(db, "POLICY_ARCHIVE", {"pack": pack_id}, classification="GOVERNANCE",
                 actor_class=user.get("role", "SYSTEM"))
    return {"pack": _pack_out(p)}


@router.get("/active")
def active(db: Session = Depends(get_db), user: dict = Depends(principal)):
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
        kinds[r.kind] = kinds.get(r.kind, 0) + 1
    return {"active_packs": [_pack_out(p) for p in packs], "enforced_rules": len(rules), "by_kind": kinds}


class PolicyTestReq(BaseModel):
    model_id: str
    scenario: str = "healthy"


@router.post("/test")
def test(req: PolicyTestReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Dry-run: evaluate a model against active policy WITHOUT persisting a decision."""
    model = db.execute(select(AIModel).where(AIModel.model_id == req.model_id)).scalar_one_or_none()
    if not model:
        raise HTTPException(404, "model not registered")
    kw = {"model_id": req.model_id, "risk_tier": model.risk_tier}
    if req.scenario == "biased":
        kw.update(risk_tier="HIGH", priv_favorable=620, unpriv_favorable=300, ecs=0.3)
    if req.scenario == "breach":
        kw.update(traceroute=0.4, dnssec=0.5)
    ev = Evidence(**kw)
    v = evaluate(ev)
    pol = pe.apply(db, ev, model, v)
    return {"model_id": req.model_id, "base_decision": v.decision, "final_decision": pol["adjusted_decision"],
            "rules_evaluated": pol["rules_evaluated"], "policy_enforced": pol["policy_enforced"],
            "fired": pol["fired"], "findings": pol["findings"]}


# ─────────────────── Policy versioning + COB approval workflow + hot-reload ───────────────────
_COB = {"gov", "admin"}


def _requires_cob(db: Session, pack: PolicyPack) -> bool:
    if pack.tenant_pk is None:
        return True  # platform / sovereign packs always require COB sign-off
    t = db.get(Tenant, pack.tenant_pk)
    return bool(tier_info(t.tier)["cob"]) if t else False


def _next_version(db: Session, pack_id: int) -> int:
    last = db.execute(select(PolicyVersion).where(PolicyVersion.pack_id == pack_id)
                      .order_by(PolicyVersion.version.desc())).scalars().first()
    return (last.version + 1) if last else 1


def _freeze(db: Session, pack: PolicyPack, user: dict, state: str, reviewed_by: str = "", note: str = ""):
    rules = db.execute(select(PolicyRule).where(
        PolicyRule.pack_id == pack.id, PolicyRule.enabled == True)).scalars().all()  # noqa: E712
    snap = [{"code": r.code, "kind": r.kind, "target": r.target, "operator": r.operator,
             "threshold": r.threshold, "severity": r.severity} for r in rules]
    rules_json = json.dumps(snap, sort_keys=True)
    content_hash = hashlib.sha3_256(rules_json.encode()).hexdigest()
    version = _next_version(db, pack.id)
    ver = PolicyVersion(pack_id=pack.id, version=version, content_hash=content_hash, rules_json=rules_json,
                        rule_count=len(snap), state=state, proposed_by=user.get("sub", ""),
                        reviewed_by=reviewed_by, review_note=note,
                        signature=seal_payload(f"{pack.id}|{version}|{content_hash}"))
    db.add(ver); db.commit(); db.refresh(ver)
    return ver, len(snap)


def _version_out(v: PolicyVersion) -> dict:
    return {"id": v.id, "pack_id": v.pack_id, "version": v.version, "state": v.state,
            "rule_count": v.rule_count, "content_hash": v.content_hash, "proposed_by": v.proposed_by,
            "reviewed_by": v.reviewed_by, "review_note": v.review_note,
            "created_at": v.created_at.isoformat(),
            "decided_at": v.decided_at.isoformat() if v.decided_at else None}


@router.post("/packs/{pack_id}/submit")
def submit_pack(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    ver, cnt = _freeze(db, p, user, "PROPOSED")
    p.status = "PENDING_APPROVAL"; db.commit()
    append_audit(db, "POLICY_SUBMIT", {"pack": pack_id, "version": ver.version, "rules": cnt},
                 classification="GOVERNANCE", actor_class=user.get("role", "SYSTEM"))
    return {"version": _version_out(ver), "requires_cob": _requires_cob(db, p),
            "note": "Submitted for COB review — a COB officer (gov/admin) must approve or veto this version."}


@router.post("/versions/{vid}/approve")
def approve_version(vid: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    if user.get("role") not in _COB:
        raise HTTPException(403, "COB approval requires a gov/admin (Oversight Board) role")
    v = db.get(PolicyVersion, vid)
    if not v:
        raise HTTPException(404, "version not found")
    if v.state not in ("PROPOSED", "APPROVED"):
        raise HTTPException(409, f"version is {v.state}")
    p = db.get(PolicyPack, v.pack_id)
    if _requires_cob(db, p) and v.proposed_by == user.get("sub") and user.get("role") != "admin":
        raise HTTPException(403, "separation of duties — a different COB officer must approve this version")
    for ov in db.execute(select(PolicyVersion).where(
            PolicyVersion.pack_id == v.pack_id, PolicyVersion.state == "ACTIVE")).scalars().all():
        ov.state = "SUPERSEDED"
    v.state = "ACTIVE"; v.reviewed_by = user.get("sub", ""); v.decided_at = datetime.now(timezone.utc)
    p.status = "ACTIVE"; p.current_version = v.version; p.activated_at = datetime.now(timezone.utc)
    db.commit(); pe.invalidate()
    append_audit(db, "POLICY_APPROVE", {"pack": p.id, "version": v.version, "content_hash": v.content_hash[:16],
                 "by": user.get("sub", "")}, classification="GOVERNANCE", actor_class=user.get("role", "SYSTEM"))
    return {"version": _version_out(v), "pack": _pack_out(p), "hot_reload": pe.hot_reload_stats(),
            "note": "COB-approved — version ACTIVE and hot-reloaded into the live EVA path."}


class VetoReq(BaseModel):
    reason: str = ""


@router.post("/versions/{vid}/veto")
def veto_version(vid: int, body: VetoReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    if user.get("role") not in _COB:
        raise HTTPException(403, "COB veto requires a gov/admin (Oversight Board) role")
    v = db.get(PolicyVersion, vid)
    if not v:
        raise HTTPException(404, "version not found")
    if v.state not in ("PROPOSED", "APPROVED"):
        raise HTTPException(409, f"version is {v.state}")
    v.state = "VETOED"; v.reviewed_by = user.get("sub", ""); v.review_note = body.reason
    v.decided_at = datetime.now(timezone.utc)
    p = db.get(PolicyPack, v.pack_id); p.status = "DRAFT"
    db.commit(); pe.invalidate()
    append_audit(db, "POLICY_VETO", {"pack": p.id, "version": v.version, "reason": body.reason[:80]},
                 classification="GOVERNANCE", actor_class=user.get("role", "SYSTEM"))
    return {"version": _version_out(v), "note": "Vetoed by COB — pack returned to DRAFT (Constitutional veto)."}


@router.get("/versions")
def list_versions(pack_id: int = None, db: Session = Depends(get_db), user: dict = Depends(principal)):
    q = select(PolicyVersion).order_by(PolicyVersion.id.desc())
    if pack_id:
        q = q.where(PolicyVersion.pack_id == pack_id)
    return [_version_out(v) for v in db.execute(q).scalars().all()]


@router.get("/versions/{vid}")
def get_version(vid: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    v = db.get(PolicyVersion, vid)
    if not v:
        raise HTTPException(404, "version not found")
    sig_ok = verify_payload(f"{v.pack_id}|{v.version}|{v.content_hash}", v.signature)
    hash_ok = hashlib.sha3_256(v.rules_json.encode()).hexdigest() == v.content_hash
    return {**_version_out(v), "rules": json.loads(v.rules_json),
            "signature_valid": sig_ok, "content_hash_valid": hash_ok,
            "signature_alg": "HMAC-SHA256 (PQC/Dilithium-ref)"}


@router.get("/hotreload")
def hotreload(user: dict = Depends(principal)):
    return pe.hot_reload_stats()
