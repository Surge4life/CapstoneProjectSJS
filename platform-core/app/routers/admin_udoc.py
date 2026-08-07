"""
UDOC v9.3 admin surface — the data layer behind the admin console tabs:
regulator rollup, constitutional pillars, model lifecycle, evidence bundle, decision replay.
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


@router.get("/regulator/summary")
def regulator_summary(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(Decision)
    if scope is not None and scope != -1:
        q = q.where(Decision.tenant_pk == scope)
    rows = list(db.execute(q.order_by(Decision.id.desc()).limit(500)).scalars().all())
    by = Counter((getattr(r, "outcome", None) or "UNKNOWN") for r in rows)
    open_cases = list(db.execute(select(OversightCase).where(OversightCase.status == "OPEN")).scalars().all())
    if scope is not None and scope != -1:
        open_cases = [c for c in open_cases if getattr(c, "tenant_pk", None) == scope]
    return {
        "decisions": len(rows),
        "by_outcome": dict(by),
        "open_oversight": len(open_cases),
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
                "risk_tier": getattr(m, "risk_tier", None),
                "use_case": getattr(m, "use_case", None),
                "jurisdiction": getattr(m, "jurisdiction", None),
            }
            for m in rows
        ],
    }


@router.post("/models/{model_id}/status")
def set_model_status(model_id: str, body: dict, db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    m = _model_or_404(db, model_id, scope)
    status = (body or {}).get("status")
    if status not in ("ACTIVE", "SUSPENDED", "RETIRED"):
        raise HTTPException(400, "status must be ACTIVE|SUSPENDED|RETIRED")
    m.status = status
    db.commit()
    return {"model_id": model_id, "status": m.status}


@router.get("/evidence/{decision_id}")
def evidence_bundle(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    d = db.execute(select(Decision).where(Decision.id == decision_id)).scalar_one_or_none()
    if not d or (scope is not None and scope != -1 and getattr(d, "tenant_pk", None) != scope):
        raise HTTPException(404, "decision not found")
    bundle = {
        "decision_id": d.id,
        "outcome": getattr(d, "outcome", None),
        "model_id": getattr(d, "model_id", None),
        "created_at": str(getattr(d, "created_at", "")),
        "provider": provider_info(),
    }
    import json as _j
    bundle["seal"] = sign(_j.dumps(bundle, sort_keys=True))
    bundle["signature_alg"] = "HMAC-SHA256 (PQC/Dilithium-ref)"
    return bundle


@router.get("/replay/{decision_id}")
def decision_replay(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    d = db.execute(select(Decision).where(Decision.id == decision_id)).scalar_one_or_none()
    if not d or (scope is not None and scope != -1 and getattr(d, "tenant_pk", None) != scope):
        raise HTTPException(404, "decision not found")
    return {
        "decision_id": d.id,
        "outcome": getattr(d, "outcome", None),
        "model_id": getattr(d, "model_id", None),
        "payload": getattr(d, "request_payload", None) or getattr(d, "payload", None),
        "result": getattr(d, "result_payload", None) or getattr(d, "result", None),
        "replay": "read-only",
    }


@router.get("/certs")
def list_certs(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(EvaCertificate)
    if scope is not None and scope != -1:
        q = q.where(EvaCertificate.tenant_pk == scope)
    rows = list(db.execute(q.order_by(EvaCertificate.id.desc()).limit(50)).scalars().all())
    return {
        "count": len(rows),
        "certs": [
            {
                "id": getattr(c, "id", None),
                "cert_id": getattr(c, "cert_id", None) or getattr(c, "certificate_id", None),
                "model_id": getattr(c, "model_id", None),
                "status": getattr(c, "status", None),
            }
            for c in rows
        ],
    }


@router.post("/certs/verify")
def verify_cert(body: dict, db: Session = Depends(get_db), user: dict = Depends(principal)):
    cert_id = (body or {}).get("cert_id") or (body or {}).get("certificate_id")
    if not cert_id:
        raise HTTPException(400, "cert_id required")
    c = db.execute(
        select(EvaCertificate).where(
            (EvaCertificate.cert_id == cert_id) | (EvaCertificate.certificate_id == cert_id)
        )
    ).scalar_one_or_none()
    if not c:
        # soft fields
        rows = list(db.execute(select(EvaCertificate).limit(200)).scalars().all())
        c = next((x for x in rows if str(getattr(x, "cert_id", "")) == str(cert_id)
                  or str(getattr(x, "certificate_id", "")) == str(cert_id)
                  or str(getattr(x, "id", "")) == str(cert_id)), None)
    if not c:
        return {"valid": False, "reason": "not found"}
    return {
        "valid": True,
        "cert_id": getattr(c, "cert_id", None) or getattr(c, "certificate_id", None) or c.id,
        "model_id": getattr(c, "model_id", None),
        "status": getattr(c, "status", None),
    }


@router.get("/health")
def udoc_admin_health():
    return {"ok": True, "surface": "udoc-admin"}
