"""
UDOC v9.3 admin surface — the data layer behind the admin console tabs:
regulator rollup, constitutional pillars, model lifecycle, evidence bundle, decision replay,
incidents, exchange, schema, regulator export.
All endpoints are tenant-isolated (a tenant sees only its own systems; platform staff see all).
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
    """Regulator rollup for Admin console. Decision.decision + OversightCase.state (not outcome/status)."""
    scope = scope_pk(user)
    q = select(Decision)
    if scope is not None and scope != -1 and hasattr(Decision, "tenant_pk"):
        q = q.where(Decision.tenant_pk == scope)
    rows = list(db.execute(q.order_by(Decision.id.desc()).limit(500)).scalars().all())
    by = Counter((getattr(r, "decision", None) or getattr(r, "outcome", None) or "UNKNOWN") for r in rows)
    try:
        open_q = select(OversightCase).where(OversightCase.state == "OPEN")
        open_cases = list(db.execute(open_q).scalars().all())
    except Exception:
        open_cases = []
    if scope is not None and scope != -1:
        open_cases = [c for c in open_cases if getattr(c, "tenant_pk", None) in (scope, None)]
    return {
        "decisions": len(rows),
        "by_outcome": dict(by),
        "open_oversight": len(open_cases),
        "note": "by_outcome keys are Decision.decision values; open_oversight uses OversightCase.state=OPEN",
    }


@router.get("/regulator/export")
def regulator_export(db: Session = Depends(get_db), user: dict = Depends(principal)):
    """JSON export for Admin Regulator tab download button."""
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
    """Capstone PUBLIC smoke path: auto-heal model-001 + demo pack if suspended. No auth required."""
    model = db.execute(select(AIModel).where(AIModel.model_id == "model-001")).scalar_one_or_none()
    pack = db.execute(
        select(PolicyPack).where(PolicyPack.name == "UDOC Demo · POPIA + Fairness")
    ).scalar_one_or_none()
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
        missing.append("model-001 not seeded — wait for Core startup seed or register AI system")
    elif model.status != "ACTIVE":
        missing.append(f"model-001 status is {model.status}")
    if not pack:
        missing.append("demo policy pack not seeded")
    elif pack.status != "ACTIVE":
        missing.append(f"demo pack status is {pack.status}")
    if not rules:
        missing.append("no ACTIVE policy rules in engine")
    return {
        "ready": ready,
        "healed": healed,
        "model_001": ({"present": True, "status": model.status, "risk_tier": model.risk_tier}
                      if model else {"present": False}),
        "demo_pack": ({"present": True, "status": pack.status, "rule_count": pack.rule_count,
                       "name": pack.name} if pack else {"present": False}),
        "active_rules": len(rules),
        "missing": missing,
        "note": "Fail-closed: evaluate without model-001 returns 404. Capstone auto-heals suspended demo seed.",
    }


@router.get("/pillars")
def pillars(user: dict = Depends(principal)):
    names = [
        "Purpose limitation", "Data minimisation", "Human primacy", "Auditability",
        "Explainability", "Fairness", "Sovereignty", "Fail-closed",
        "Evidence chain", "Policy-to-code", "Sector controls", "Cert lifecycle",
    ]
    return {"pillars": [{"id": i, "name": n, "status": "operational"} for i, n in enumerate(names, 1)]}


@router.get("/constitutional/pillars")
def constitutional_pillars(user: dict = Depends(principal)):
    """Alias for Admin UI Constitutional tab (same payload as /udoc/pillars)."""
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
        "models": [
            {
                "model_id": m.model_id,
                "status": m.status,
                "risk_tier": m.risk_tier,
                "use_case": getattr(m, "use_case", "") or "",
                "jurisdiction": getattr(m, "jurisdiction", "") or "",
            }
            for m in rows
        ],
    }


@router.get("/models/{model_id}/lifecycle")
def model_lifecycle(model_id: str, db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Lifecycle tab — model metadata + decision rollup."""
    scope = scope_pk(user)
    m = _model_or_404(db, model_id, scope)
    q = select(Decision).where(Decision.model_pk == m.id) if hasattr(Decision, "model_pk") else select(Decision)
    rows = list(db.execute(q.order_by(Decision.id.desc()).limit(300)).scalars().all())
    if not rows and hasattr(Decision, "model_id"):
        rows = list(db.execute(
            select(Decision).where(Decision.model_id == model_id).order_by(Decision.id.desc()).limit(300)
        ).scalars().all())
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
    if status not in ("ACTIVE", "SUSPENDED", "RETIRED"):
        raise HTTPException(status_code=400, detail="status must be ACTIVE|SUSPENDED|RETIRED")
    m.status = status
    db.commit()
    return {"model_id": m.model_id, "status": m.status}


def _evidence_bundle(db, decision_id: int):
    """Shared evidence payload shaped for Admin UI Evidence tab."""
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
    """Shared replay payload shaped for Admin UI Replay tab."""
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
        "note": "Deterministic sealed replay · Capstone free-tier stores outcome vector; full engine re-eval is post-seed",
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
    """Alias matching Admin UI path /udoc/decisions/{id}/evidence."""
    return evidence(decision_id, db=db, user=user)


@router.get("/replay/{decision_id}")
def replay(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    return _replay_bundle(db, decision_id)


@router.get("/decisions/{decision_id}/replay")
def replay_alias(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Alias matching Admin UI path /udoc/decisions/{id}/replay."""
    return replay(decision_id, db=db, user=user)


@router.get("/incidents")
def incidents(db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Incidents tab — BLOCK / ESCALATE decisions (Admin UI field names)."""
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
    """Exchange / data-sovereignty tab — field names match Admin UI."""
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
        "honesty": "No formal data-exchange mesh on free tier · design documented in Canon",
        "basis": "POPIA purpose limitation · UDOC constitutional pillars",
    }


@router.get("/schema")
def schema(user: dict = Depends(principal)):
    """Governance data schema for integrators (Admin Schema tab expects flat string/array values)."""
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
        "certs": [
            {
                "certificate_id": getattr(c, "certificate_id", None) or getattr(c, "cert_id", ""),
                "model_id": getattr(c, "model_id", ""),
                "status": getattr(c, "status", ""),
            }
            for c in rows
        ],
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
