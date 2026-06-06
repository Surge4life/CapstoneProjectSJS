"""
Policy-to-Code API — UDOC governance protocol layer.

A client uploads passed/applicable legislation (PDF/DOCX/TXT). UDOC compiles candidate
machine-enforceable rules (transparent, editable). A compliance officer reviews and ACTIVATES
the pack; from then on the rules are enforced inside the non-bypassable EVA decision path.
"""
import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import PolicyPack, PolicyRule, AIModel
from app.core.dependencies import current_user, principal, scope_pk
from app.core.config import settings
from app.services import policy_engine as pe
from app.services.governance_bridge import Evidence, evaluate
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
    db.commit(); db.refresh(r)
    return _rule_out(r)


@router.post("/packs/{pack_id}/activate")
def activate(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    p.status = "ACTIVE"; p.activated_at = datetime.now(timezone.utc)
    db.commit()
    enabled = db.execute(select(PolicyRule).where(
        PolicyRule.pack_id == pack_id, PolicyRule.enabled == True)).scalars().all()  # noqa: E712
    append_audit(db, "POLICY_ACTIVATE", {"pack": pack_id, "name": p.name, "active_rules": len(enabled)},
                 classification="GOVERNANCE", actor_class=user.get("role", "SYSTEM"))
    return {"pack": _pack_out(p), "active_rules": len(enabled),
            "note": "Pack is now ENFORCED in the live EVA decision path."}


@router.post("/packs/{pack_id}/archive")
def archive(pack_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    _require_write(user)
    p = db.get(PolicyPack, pack_id)
    if not p:
        raise HTTPException(404, "pack not found")
    p.status = "ARCHIVED"; db.commit()
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
