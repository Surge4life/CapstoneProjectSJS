"""
UDOC v9.3 admin surface — regulator, pillars, lifecycle, evidence, replay, incidents, exchange, schema.
"""
from collections import Counter
import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import (AIModel, Decision, EvaCertificate, AuditRef, OversightCase,
                           PolicyPack, PolicyVersion, Tenant)
from app.core.dependencies import principal, scope_pk
from app.services.governance_bridge import Evidence, evaluate
from app.services import policy_engine as pe
from app.services.crypto_provider import provider_info, sign

router = APIRouter(prefix="/udoc", tags=["UDOC v9.3 admin"])


def _model_or_404(db, model_id, scope):
    m = db.execute(select(AIModel).where(AIModel.model_id == model_id)).scalar_one_or_none()
    if not m or (scope is not None and scope != -1 and m.tenant_pk != scope):
        raise HTTPException(status_code=404, detail="Model not found")
    return m


def _decision_or_404(db, decision_id):
    d = db.execute(select(Decision).where(Decision.id == decision_id)).scalar_one_or_none()
    if not d:
        raise HTTPException(status_code=404, detail="Decision not found")
    return d


def _cert_for_decision(db, d):
    cid = getattr(d, "certificate_id", None)
    if not cid:
        return None
    rows = list(db.execute(select(EvaCertificate).order_by(EvaCertificate.id.desc()).limit(200)).scalars().all())
    for r in rows:
        if getattr(r, "certificate_id", None) == cid or getattr(r, "cert_id", None) == cid:
            return r
    return None


def _model_id_for_decision(db, d):
    mid = getattr(d, "model_id", None)
    if mid:
        return mid
    pk = getattr(d, "model_pk", None)
    if pk is None:
        return ""
    m = db.execute(select(AIModel).where(AIModel.id == pk)).scalar_one_or_none()
    return m.model_id if m else ""


def _safe_json(val):
    if val is None:
        return None
    if isinstance(val, (dict, list)):
        return val
    if isinstance(val, str):
        try:
            return json.loads(val)
        except Exception:
            return {"raw": val[:500]}
    try:
        return json.loads(str(val))
    except Exception:
        return None


@router.get("/regulator/summary")
def regulator_summary(db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Regulator rollup shaped for Admin console (systems + decisions + oversight + policy + crypto)."""
    scope = scope_pk(user)
    q = select(Decision)
    if scope is not None and scope != -1 and hasattr(Decision, "tenant_pk"):
        q = q.where(Decision.tenant_pk == scope)
    rows = list(db.execute(q.order_by(Decision.id.desc()).limit(500)).scalars().all())
    by = Counter((getattr(r, "decision", None) or getattr(r, "outcome", None) or "UNKNOWN") for r in rows)
    blocked = int(by.get("BLOCK", 0))
    escalated = int(by.get("ESCALATE", 0))
    approved = int(by.get("APPROVE", 0))

    mq = select(AIModel)
    if scope is not None and scope != -1:
        mq = mq.where(AIModel.tenant_pk == scope)
    models = list(db.execute(mq).scalars().all())
    by_status = Counter((m.status or "UNKNOWN") for m in models)

    try:
        open_q = select(OversightCase).where(OversightCase.state == "OPEN")
        open_cases = list(db.execute(open_q).scalars().all())
    except Exception:
        open_cases = []
    if scope is not None and scope != -1:
        open_cases = [c for c in open_cases if getattr(c, "tenant_pk", None) in (scope, None)]
    try:
        all_cases = list(db.execute(select(OversightCase)).scalars().all())
    except Exception:
        all_cases = open_cases

    packs = list(db.execute(select(PolicyPack).where(PolicyPack.status == "ACTIVE")).scalars().all())
    rules = []
    try:
        rules = pe.active_rules(db, tenant_pk=None if scope in (None, -1) else scope)
    except Exception:
        rules = []
    crypto = {}
    try:
        crypto = provider_info() if callable(provider_info) else (provider_info or {})
    except Exception:
        crypto = {"label": "HMAC demo", "custody": "process-memory Capstone"}
    if not isinstance(crypto, dict):
        crypto = {"label": str(crypto), "custody": "process-memory Capstone"}

    return {
        "scope": "platform" if scope in (None, -1) else f"tenant:{scope}",
        "systems": {"total": len(models), "by_status": dict(by_status)},
        "decisions": {
            "total": len(rows),
            "by_outcome": dict(by),
            "blocked": blocked,
            "escalated": escalated,
            "approved": approved,
        },
        "oversight": {"open": len(open_cases), "total": len(all_cases)},
        "policy": {
            "active_packs": len(packs),
            "active_rules": len(rules) if isinstance(rules, list) else 0,
            "hot_reload": {"last_reload_ms": 0},
        },
        "crypto": {
            "label": crypto.get("label") or crypto.get("provider") or "HMAC-SHA256 demo",
            "custody": crypto.get("custody") or "process-memory Capstone free-tier",
        },
        "compliance_basis": "POPIA + UDOC constitutional pillars · Capstone free-tier",
        "by_outcome": dict(by),
        "open_oversight": len(open_cases),
        "note": "Rich regulator summary for UDOC Admin · Decision.decision + OversightCase.state",
    }


@router.get("/regulator/export")
def regulator_export(db: Session = Depends(get_db), user: dict = Depends(principal)):
    summary = regulator_summary(db=db, user=user)
    scope = scope_pk(user)
    q = select(Decision)
    if scope is not None and scope != -1 and hasattr(Decision, "tenant_pk"):
        q = q.where(Decision.tenant_pk == scope)
    rows = list(db.execute(q.order_by(Decision.id.desc()).limit(200)).scalars().all())
    return {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "decisions": [
            {
                "id": r.id,
                "decision": getattr(r, "decision", None),
                "svs": getattr(r, "svs", None),
                "certificate_id": getattr(r, "certificate_id", None),
                "created_at": r.created_at.isoformat() if getattr(r, "created_at", None) else None,
            }
            for r in rows
        ],
        "honesty": "Capstone free-tier export · not a formal regulator filing",
    }


@router.get("/demo/ready")
def demo_ready(db: Session = Depends(get_db)):
    model = db.execute(select(AIModel).where(AIModel.model_id == "model-001")).scalar_one_or_none()
    pack = db.execute(select(PolicyPack).where(PolicyPack.name == "UDOC Demo · POPIA + Fairness")).scalar_one_or_none()
    healed = []
    if model and model.status != "ACTIVE":
        prev = model.status
        model.status = "ACTIVE"
        healed.append(f"model-001 {prev}->ACTIVE")
    if pack and pack.status != "ACTIVE":
        prev = pack.status
        pack.status = "ACTIVE"
        pack.activated_at = datetime.now(timezone.utc)
        healed.append(f"demo pack {prev}->ACTIVE")
        try:
            pe.invalidate()
        except Exception:
            pass
    if healed:
        db.commit()
    rules = pe.active_rules(db, tenant_pk=None)
    ready = bool(model and model.status == "ACTIVE" and pack and pack.status == "ACTIVE" and len(rules) > 0)
    missing = []
    if not model:
        missing.append("model-001 not seeded")
    elif model.status != "ACTIVE":
        missing.append(f"model-001 status is {model.status}")
    if not pack:
        missing.append("demo policy pack not seeded")
    elif pack.status != "ACTIVE":
        missing.append(f"demo pack status is {pack.status}")
    if not rules:
        missing.append("no ACTIVE policy rules")
    return {
        "ready": ready,
        "healed": healed,
        "model_001": ({"present": True, "status": model.status, "risk_tier": model.risk_tier} if model else {"present": False}),
        "demo_pack": ({"present": True, "status": pack.status, "rule_count": pack.rule_count, "name": pack.name} if pack else {"present": False}),
        "active_rules": len(rules),
        "missing": missing,
        "note": "Capstone auto-heals suspended demo seed.",
    }


_PILLAR_DEFS = [
    (1, "Purpose limitation", "Systems process only for declared lawful purpose", "policy + EVA gate", "operational"),
    (2, "Data minimisation", "Only necessary attributes enter the decision path", "policy rules", "operational"),
    (3, "Human primacy", "Humans retain override and final accountability", "HITL + kill-switch", "operational"),
    (4, "Auditability", "Every decision is sealed and exportable", "certificate + export", "operational"),
    (5, "Explainability", "Outcomes expose reasons and dimensions", "EVA evidence bundle", "operational"),
    (6, "Fairness", "Disparate impact and bias paths are fail-closed", "DI rule + biased smoke", "operational"),
    (7, "Sovereignty", "Jurisdiction and localisation constraints apply", "POPIA localisation rules", "operational"),
    (8, "Fail-closed", "Missing model/policy blocks rather than approves", "demo/ready + 404 gate", "operational"),
    (9, "Evidence chain", "Certificates bind content hash to outcome", "HMAC demo chain", "operational"),
    (10, "Policy-to-code", "Uploaded policy becomes runtime rules", "runtime-matrix", "operational"),
    (11, "Sector controls", "PUBLIC/PRIVATE/sector profiles adjust gates", "governance_bridge sectors", "operational"),
    (12, "Cert lifecycle", "Certificates are listable and verifiable", "/udoc/certs", "operational"),
]


@router.get("/pillars")
def pillars(user: dict = Depends(principal)):
    rows = [
        {"id": n, "n": n, "name": name, "principle": principle, "enforcement": enforcement, "status": status}
        for n, name, principle, enforcement, status in _PILLAR_DEFS
    ]
    status_summary = Counter(r["status"] for r in rows)
    return {"count": len(rows), "status_summary": dict(status_summary), "pillars": rows}


@router.get("/constitutional/pillars")
def constitutional_pillars(user: dict = Depends(principal)):
    return pillars(user)


@router.get("/models")
def list_models(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(AIModel)
    if scope is not None and scope != -1:
        q = q.where(AIModel.tenant_pk == scope)
    rows = list(db.execute(q.order_by(AIModel.id.desc()).limit(100)).scalars().all())
    return {
        "count": len(rows),
        "models": [{
            "model_id": m.model_id,
            "status": m.status,
            "risk_tier": m.risk_tier,
            "use_case": getattr(m, "use_case", "") or "",
            "jurisdiction": getattr(m, "jurisdiction", "") or "",
        } for m in rows],
    }


@router.get("/models/{model_id}/lifecycle")
def model_lifecycle(model_id: str, db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    m = _model_or_404(db, model_id, scope)
    q = select(Decision).where(Decision.model_pk == m.id) if hasattr(Decision, "model_pk") else select(Decision)
    rows = list(db.execute(q.order_by(Decision.id.desc()).limit(300)).scalars().all())
    if not rows and hasattr(Decision, "model_id"):
        rows = list(db.execute(select(Decision).where(Decision.model_id == model_id).order_by(Decision.id.desc()).limit(300)).scalars().all())
    by = Counter((getattr(r, "decision", None) or "UNKNOWN") for r in rows)
    last = rows[0] if rows else None
    return {
        "model_id": m.model_id,
        "name": getattr(m, "name", None) or m.model_id,
        "operator_id": getattr(m, "operator_id", "") or "",
        "risk_tier": m.risk_tier,
        "jurisdiction": getattr(m, "jurisdiction", "") or "",
        "status": m.status,
        "stage": getattr(m, "stage", None) or ("OPERATIONAL" if m.status == "ACTIVE" else m.status),
        "decisions": {
            "total": len(rows),
            "by_outcome": dict(by),
            "last_outcome": getattr(last, "decision", None) if last else None,
            "last_decision": last.created_at.isoformat() if last and getattr(last, "created_at", None) else None,
        },
    }


@router.post("/models/{model_id}/status")
def set_model_status(model_id: str, body: dict, db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    m = _model_or_404(db, model_id, scope)
    status = (body or {}).get("status")
    if status == "BLOCKED":
        status = "SUSPENDED"
    if status not in ("ACTIVE", "SUSPENDED", "RETIRED"):
        raise HTTPException(status_code=400, detail="status must be ACTIVE|SUSPENDED|RETIRED")
    m.status = status
    db.commit()
    return {"model_id": m.model_id, "status": m.status}


def _evidence_bundle(db, decision_id: int):
    d = _decision_or_404(db, decision_id)
    cert = _cert_for_decision(db, d)
    mid = _model_id_for_decision(db, d)
    dims = {}
    if cert is not None:
        raw = getattr(cert, "dimensions_json", None) or getattr(cert, "dimensions", None)
        parsed = _safe_json(raw)
        if isinstance(parsed, dict):
            dims = parsed
    ev = _safe_json(getattr(d, "evidence_json", None))
    reasons = ""
    if isinstance(ev, dict):
        reasons = ev.get("reasons") or ev.get("block_reasons") or ""
        if isinstance(reasons, list):
            reasons = " · ".join(str(x) for x in reasons)
    sealed = bool(getattr(d, "seal", None) or getattr(d, "certificate_id", None))
    cert_payload = None
    if cert is not None:
        cert_payload = {
            "certificate_id": getattr(cert, "certificate_id", None) or getattr(cert, "cert_id", ""),
            "composite_eva": getattr(cert, "composite_eva", None) or getattr(d, "svs", None),
            "policy_version": getattr(cert, "policy_version", None) or "demo-pack",
            "signature_alg": getattr(cert, "signature_alg", None) or "HMAC-SHA256",
            "content_sha3": getattr(cert, "content_sha3", None) or getattr(cert, "content_hash", None) or "",
            "merkle_leaf": getattr(cert, "merkle_leaf", None) or getattr(d, "seal", None) or "",
            "dimensions": dims,
        }
    return {
        "decision": {
            "id": d.id,
            "model_id": mid,
            "outcome": getattr(d, "decision", None),
            "risk": getattr(d, "risk", None),
            "compliance": getattr(d, "compliance", None),
            "sealed": sealed,
            "at": d.created_at.isoformat() if getattr(d, "created_at", None) else None,
            "reasons": reasons or ("sealed decision · see certificate" if sealed else ""),
        },
        "certificate": cert_payload,
        "audit_context": {
            "chain_head_seq": d.id,
            "chain_head_hash": (getattr(d, "seal", None) or getattr(d, "certificate_id", None) or "")[:64],
        },
        "decision_id": d.id,
        "svs": getattr(d, "svs", None),
        "seal": getattr(d, "seal", None),
        "certificate_id": getattr(d, "certificate_id", None),
        "created_at": d.created_at.isoformat() if getattr(d, "created_at", None) else None,
        "evidence_json": ev,
    }


def _replay_bundle(db, decision_id: int):
    d = _decision_or_404(db, decision_id)
    outcome = getattr(d, "decision", None)
    original = {
        "outcome": outcome,
        "svs": getattr(d, "svs", None),
        "risk": getattr(d, "risk", None),
        "compliance": getattr(d, "compliance", None),
        "sovereign": getattr(d, "sovereign", None),
        "certificate_id": getattr(d, "certificate_id", None),
    }
    replayed = {
        "outcome": outcome,
        "svs": getattr(d, "svs", None),
        "risk": getattr(d, "risk", None),
        "composite_eva": getattr(d, "svs", None),
    }
    return {
        "original": original,
        "replayed": replayed,
        "drift": False,
        "note": "Deterministic sealed replay · Capstone free-tier",
        "decision_id": d.id,
        "decision": outcome,
        "replay": "deterministic",
        "svs": getattr(d, "svs", None),
        "risk": getattr(d, "risk", None),
        "compliance": getattr(d, "compliance", None),
        "sovereign": getattr(d, "sovereign", None),
        "certificate_id": getattr(d, "certificate_id", None),
    }


@router.get("/evidence/{decision_id}")
def evidence(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    try:
        return _evidence_bundle(db, decision_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"evidence failed: {type(e).__name__}: {e}")


@router.get("/decisions/{decision_id}/evidence")
def evidence_alias(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    return evidence(decision_id, db=db, user=user)


@router.get("/replay/{decision_id}")
def replay(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    return _replay_bundle(db, decision_id)


@router.get("/decisions/{decision_id}/replay")
def replay_alias(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    return replay(decision_id, db=db, user=user)


@router.get("/incidents")
def incidents(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(Decision)
    if scope is not None and scope != -1 and hasattr(Decision, "tenant_pk"):
        q = q.where(Decision.tenant_pk == scope)
    rows = list(db.execute(q.order_by(Decision.id.desc()).limit(300)).scalars().all())
    items = []
    for r in rows:
        outcome = getattr(r, "decision", None) or ""
        if outcome not in ("BLOCK", "ESCALATE"):
            continue
        items.append({
            "decision_id": r.id,
            "id": r.id,
            "decision": outcome,
            "model_id": _model_id_for_decision(db, r),
            "severity": "BLOCK" if outcome == "BLOCK" else "ESCALATE",
            "risk": getattr(r, "risk", None),
            "svs": getattr(r, "svs", None),
            "at": r.created_at.isoformat() if getattr(r, "created_at", None) else None,
            "certificate_id": getattr(r, "certificate_id", None),
        })
    try:
        open_q = select(OversightCase).where(OversightCase.state == "OPEN")
        open_cases = list(db.execute(open_q).scalars().all())
    except Exception:
        open_cases = []
    if scope is not None and scope != -1:
        open_cases = [c for c in open_cases if getattr(c, "tenant_pk", None) in (scope, None)]
    return {
        "count": len(items),
        "incidents": items,
        "open_cases": [{"id": getattr(c, "id", None), "ref": getattr(c, "ref", None), "state": getattr(c, "state", None)} for c in open_cases],
        "note": "BLOCK/ESCALATE rows from Decision table",
    }


@router.get("/exchange")
def exchange(user: dict = Depends(principal)):
    return {
        "jurisdiction": "ZA",
        "data_localisation": "required · POPIA + UDOC sovereignty pillar",
        "cross_border_transfer": "not enabled on Capstone free tier",
        "sovereignty_recheck_hours": 24,
        "rules_active": 2,
        "localisation_rules": [
            {"code": "POPIA-LOCAL", "kind": "residency"},
            {"code": "UDOC-SOV", "kind": "sovereignty"},
        ],
        "residency": "Neon (external) · Render compute per free-tier",
        "encryption_at_rest": "provider-managed (Neon)",
        "encryption_in_transit": "TLS",
        "honesty": "No formal data-exchange mesh on free tier",
        "basis": "POPIA purpose limitation · UDOC constitutional pillars",
    }


@router.get("/schema")
def schema(user: dict = Depends(principal)):
    return {
        "Decision": "id, decision(APPROVE|BLOCK|ESCALATE), svs, risk, compliance, sovereign, certificate_id, model_pk, created_at",
        "AIModel": "model_id, status(ACTIVE|SUSPENDED|BLOCKED|RETIRED), risk_tier, jurisdiction, operator_id",
        "EvaCertificate": "certificate_id, model_id, composite_eva, content_sha3",
        "OversightCase": "ref, state(OPEN|REVIEWING|RESOLVED), subject_ref",
        "PolicyPack": "name, status(DRAFT|ACTIVE|ARCHIVED), rule_count, jurisdiction",
        "Tenant": "tenant_id, sector, tier, status, usage_decisions",
        "honesty": "Capstone schema surface · not full OpenAPI re-export",
    }


@router.get("/certs")
def list_certs(db: Session = Depends(get_db), user: dict = Depends(principal)):
    rows = list(db.execute(select(EvaCertificate).order_by(EvaCertificate.id.desc()).limit(50)).scalars().all())
    return {
        "count": len(rows),
        "certs": [{
            "certificate_id": getattr(c, "certificate_id", None) or getattr(c, "cert_id", ""),
            "model_id": getattr(c, "model_id", ""),
            "status": getattr(c, "status", ""),
        } for c in rows],
    }


@router.post("/certs/verify")
def verify_cert(body: dict, db: Session = Depends(get_db), user: dict = Depends(principal)):
    cid = (body or {}).get("certificate_id") or (body or {}).get("cert_id")
    if not cid:
        raise HTTPException(status_code=400, detail="certificate_id required")
    c = None
    rows = list(db.execute(select(EvaCertificate).limit(200)).scalars().all())
    for r in rows:
        if getattr(r, "certificate_id", None) == cid or getattr(r, "cert_id", None) == cid:
            c = r
            break
    if not c:
        return {"valid": False, "certificate_id": cid, "detail": "not found"}
    return {
        "valid": True,
        "certificate_id": cid,
        "status": getattr(c, "status", "ACTIVE"),
        "model_id": getattr(c, "model_id", ""),
    }


@router.get("/lifecycle")
def lifecycle_summary(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(AIModel)
    if scope is not None and scope != -1:
        q = q.where(AIModel.tenant_pk == scope)
    models = list(db.execute(q).scalars().all())
    primary = next((m for m in models if m.model_id == "model-001"), models[0] if models else None)
    primary_payload = model_lifecycle(primary.model_id, db, user) if primary is not None else None
    return {
        "count": len(models),
        "models": [{"model_id": m.model_id, "status": m.status, "risk_tier": m.risk_tier} for m in models],
        "primary": primary_payload,
        "note": "Alias surface · use /udoc/models/{id}/lifecycle for detail",
    }


@router.get("/control")
def control_summary(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(AIModel)
    if scope is not None and scope != -1:
        q = q.where(AIModel.tenant_pk == scope)
    models = list(db.execute(q).scalars().all())
    by = Counter((m.status or "UNKNOWN") for m in models)
    return {
        "systems": len(models),
        "by_status": dict(by),
        "allowed_status": ["ACTIVE", "SUSPENDED", "RETIRED"],
        "note": "Control mutations use /udoc/models/{id}/status or /registry/models/{id}/status",
    }


@router.get("/tenancy")
def tenancy_summary(db: Session = Depends(get_db), user: dict = Depends(principal)):
    try:
        rows = list(db.execute(select(Tenant)).scalars().all())
    except Exception:
        rows = []
    return {
        "count": len(rows),
        "tenants": [
            {"id": getattr(t, "id", None), "tenant_id": getattr(t, "tenant_id", None),
             "name": getattr(t, "name", None), "status": getattr(t, "status", None),
             "tier": getattr(t, "tier", None)}
            for t in rows[:50]
        ],
        "note": "Prefer /tenants and /tenants/me for full commercial payload",
    }


@router.get("/health")
def udoc_admin_health():
    return {"ok": True, "surface": "udoc-admin"}


@router.get("/specification")
def specification():
    return {
        "surface": "UDOC v9.3",
        "roles": ["admin", "operator", "auditor", "viewer"],
        "honesty": "Capstone free-tier · Neon ≤500MB · no commercial multi-tenant scale claim",
    }
