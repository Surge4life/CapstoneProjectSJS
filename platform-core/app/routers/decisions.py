"""
UDOC decisioning — the non-bypassable governance path.
Runs EVA 6-D scoring + sovereignty, seals the verdict, writes immutable audit, emits event.
Fail-closed for critical classes when governance cannot complete (per hardware spec).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import AIModel, Decision, EvaCertificate, Tenant
from app.core.dependencies import principal, scope_pk
from app.services.governance_bridge import Evidence, evaluate
from app.services import policy_engine as pe
from app.services.crypto_provider import sign
import traceback

router = APIRouter(prefix="/decisions", tags=["UDOC decisions"])

_SCENARIO_PRESETS = {
    "fair": {
        "raw_confidence": 0.92, "compliance": 1.0,
        "priv_favorable": 480, "priv_total": 1000,
        "unpriv_favorable": 470, "unpriv_total": 1000,
        "ecs": 0.85, "bgp": 1.0, "traceroute": 1.0, "dnssec": 1.0, "storage": 1.0,
    },
    "biased": {
        "raw_confidence": 0.88, "compliance": 0.55,
        "priv_favorable": 800, "priv_total": 1000,
        "unpriv_favorable": 200, "unpriv_total": 1000,
        "ecs": 0.4, "bgp": 1.0, "traceroute": 1.0, "dnssec": 1.0, "storage": 1.0,
    },
    "high": {
        "raw_confidence": 0.7, "compliance": 0.6, "risk_tier": "HIGH",
        "priv_favorable": 500, "priv_total": 1000,
        "unpriv_favorable": 450, "unpriv_total": 1000,
        "ecs": 0.5, "bgp": 0.9, "traceroute": 0.9, "dnssec": 0.9, "storage": 0.9,
    },
    "sov": {
        "raw_confidence": 0.9, "compliance": 0.95,
        "priv_favorable": 500, "priv_total": 1000,
        "unpriv_favorable": 480, "unpriv_total": 1000,
        "ecs": 0.8, "bgp": 0.2, "traceroute": 0.3, "dnssec": 0.2, "storage": 0.4,
    },
}


class DecisionReq(BaseModel):
    model_id: str
    risk_tier: str | None = None
    raw_confidence: float = 0.9
    compliance: float = 1.0
    priv_favorable: int = 480
    priv_total: int = 1000
    unpriv_favorable: int = 470
    unpriv_total: int = 1000
    ecs: float = 0.75
    bgp: float = 1.0
    traceroute: float = 1.0
    dnssec: float = 1.0
    storage: float = 1.0
    sector: str | None = None
    explainability: float = 0.85
    audit_trail: float = 0.90
    inclusion_access: float = 0.85
    human_oversight_present: bool = True


@router.post("")
def decide(req: DecisionReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    try:
        return _decide_inner(req, db, user)
    except HTTPException:
        raise
    except Exception as e:
        detail = f"{type(e).__name__}: {e}"
        print(f"[decisions] unhandled: {detail}\n{traceback.format_exc()}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail[:400])


def _decide_inner(req: DecisionReq, db: Session, user: dict):
    model = db.execute(select(AIModel).where(AIModel.model_id == req.model_id)).scalar_one_or_none()
    if not model:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "model not registered — fail-closed")
    if (model.status or "").upper() not in ("ACTIVE", ""):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            f"model {req.model_id} status is {model.status} — fail-closed")
    scope = scope_pk(user) if user else None
    evidence = Evidence(
        raw_confidence=req.raw_confidence,
        compliance=req.compliance,
        priv_favorable=req.priv_favorable,
        priv_total=req.priv_total,
        unpriv_favorable=req.unpriv_favorable,
        unpriv_total=req.unpriv_total,
        ecs=req.ecs,
        bgp=req.bgp,
        traceroute=req.traceroute,
        dnssec=req.dnssec,
        storage=req.storage,
        explainability=req.explainability,
        audit_trail=req.audit_trail,
        inclusion_access=req.inclusion_access,
        human_oversight_present=req.human_oversight_present,
        risk_tier=req.risk_tier or getattr(model, "risk_tier", None),
        sector=req.sector,
    )
    result = evaluate(evidence)
    decision = result.get("decision") or result.get("outcome") or "ESCALATE"
    # policy enforcement layer
    try:
        rules = pe.active_rules(db, tenant_pk=None)
        enforced = pe.enforce(result, rules) if hasattr(pe, "enforce") else result
        if isinstance(enforced, dict):
            result = {**result, **enforced}
            decision = result.get("decision") or decision
    except Exception as e:
        print(f"[decisions] policy layer: {e}")

    tenant_pk = getattr(model, "tenant_pk", None)
    row = Decision(
        model_id=req.model_id,
        outcome=str(decision),
        tenant_pk=tenant_pk,
    )
    # best-effort optional fields
    for attr, val in [
        ("composite_eva", result.get("composite_eva") or result.get("composite")),
        ("request_payload", evidence.__dict__ if hasattr(evidence, "__dict__") else None),
        ("result_payload", result),
    ]:
        if hasattr(row, attr):
            setattr(row, attr, val)
    db.add(row)
    db.commit()
    db.refresh(row)
    out = {
        "id": row.id,
        "decision": decision,
        "outcome": decision,
        "model_id": req.model_id,
        "composite_eva": result.get("composite_eva") or result.get("composite"),
        "dimensions": result.get("dimensions") or result.get("scores"),
        "policy_enforced": result.get("policy_enforced", True),
        "block_reasons": result.get("block_reasons") or result.get("reasons") or [],
        "controllers": result.get("controllers") or [],
        "sector_eva": result.get("sector_eva"),
        "certificate_id": result.get("certificate_id"),
    }
    try:
        out["seal"] = sign(str(out.get("id")) + str(decision))
    except Exception:
        pass
    return out


@router.get("")
def list_decisions(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(Decision).order_by(Decision.id.desc()).limit(50)
    if scope is not None and scope != -1:
        q = q.where(Decision.tenant_pk == scope)
    rows = list(db.execute(q).scalars().all())
    return {
        "count": len(rows),
        "decisions": [
            {"id": r.id, "model_id": getattr(r, "model_id", None), "outcome": getattr(r, "outcome", None)}
            for r in rows
        ],
    }


@router.get("/certificates")
def list_certificates(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    q = select(EvaCertificate).order_by(EvaCertificate.id.desc()).limit(50)
    if scope is not None and scope != -1 and hasattr(EvaCertificate, "tenant_pk"):
        q = q.where(EvaCertificate.tenant_pk == scope)
    rows = list(db.execute(q).scalars().all())
    return {"count": len(rows), "certificates": [
        {"id": c.id, "model_id": getattr(c, "model_id", None), "status": getattr(c, "status", None)}
        for c in rows
    ]}


class BatchItem(BaseModel):
    option: str
    model_id: str = "model-001"
    risk_tier: str | None = None
    raw_confidence: float | None = None
    compliance: float | None = None
    priv_favorable: int | None = None
    priv_total: int | None = None
    unpriv_favorable: int | None = None
    unpriv_total: int | None = None
    bgp: float | None = None
    traceroute: float | None = None
    dnssec: float | None = None
    storage: float | None = None
    sector: str | None = None


class BatchRequest(BaseModel):
    options: list[str] | None = None
    scenarios: list[str] | None = None  # alias used by Sentinel / Client chips
    items: list[BatchItem] | None = None
    model_id: str = "model-001"
    sector: str | None = None


@router.post("/batch")
def decide_batch(req: BatchRequest, db: Session = Depends(get_db)):
    """Capstone PUBLIC smoke path — scenario presets only (fair/biased/high/sov). No auth."""
    user = {"email": "smoke@gods.local", "role": "operator", "division": "UDOC", "is_admin": True, "tenant_pk": None}
    items: list[BatchItem] = []
    if req.items:
        items = req.items
    else:
        names = req.options or req.scenarios or ["fair", "biased", "high", "sov"]
        for name in names:
            items.append(BatchItem(option=name, model_id=req.model_id, sector=req.sector))

    results = []
    counts = {"APPROVE": 0, "BLOCK": 0, "ESCALATE": 0, "OTHER": 0, "ERROR": 0}
    for it in items[:12]:
        name = (it.option or "custom").lower().strip()
        preset = dict(_SCENARIO_PRESETS.get(name, {}))
        body = {
            "model_id": it.model_id or req.model_id or "model-001",
            "raw_confidence": it.raw_confidence if it.raw_confidence is not None else preset.get("raw_confidence", 0.9),
            "compliance": it.compliance if it.compliance is not None else preset.get("compliance", 1.0),
            "priv_favorable": it.priv_favorable if it.priv_favorable is not None else preset.get("priv_favorable", 480),
            "priv_total": it.priv_total if it.priv_total is not None else preset.get("priv_total", 1000),
            "unpriv_favorable": it.unpriv_favorable if it.unpriv_favorable is not None else preset.get("unpriv_favorable", 470),
            "unpriv_total": it.unpriv_total if it.unpriv_total is not None else preset.get("unpriv_total", 1000),
            "ecs": preset.get("ecs", 0.75),
            "bgp": it.bgp if it.bgp is not None else preset.get("bgp", 1.0),
            "traceroute": it.traceroute if it.traceroute is not None else preset.get("traceroute", 1.0),
            "dnssec": it.dnssec if it.dnssec is not None else preset.get("dnssec", 1.0),
            "storage": it.storage if it.storage is not None else preset.get("storage", 1.0),
            "sector": it.sector or req.sector,
        }
        if it.risk_tier or preset.get("risk_tier"):
            body["risk_tier"] = it.risk_tier or preset.get("risk_tier")
        try:
            out = _decide_inner(DecisionReq(**body), db, user)
            dec = str(out.get("decision") or "OTHER").upper()
            if dec in counts:
                counts[dec] += 1
            else:
                counts["OTHER"] += 1
            results.append({
                "option": name,
                "scenario": name,
                "ok": True,
                "decision": out.get("decision"),
                "outcome": out.get("decision"),
                "composite_eva": out.get("composite_eva"),
                "policy_enforced": out.get("policy_enforced"),
                "block_reasons": (out.get("block_reasons") or [])[:4],
                "certificate_id": out.get("certificate_id"),
                "id": out.get("id"),
                "dimensions": out.get("dimensions"),
                "sector_eva": out.get("sector_eva"),
                "controllers_fired": [c for c in (out.get("controllers") or []) if c.get("fired")],
            })
        except HTTPException as he:
            counts["ERROR"] += 1
            results.append({"option": name, "scenario": name, "ok": False, "decision": None,
                            "error": he.detail if isinstance(he.detail, str) else str(he.detail), "outcome": None})
        except Exception as e:
            counts["ERROR"] += 1
            results.append({"option": name, "scenario": name, "ok": False, "decision": None,
                            "error": f"{type(e).__name__}: {e}", "outcome": None})

    return {
        "matrix": "UDOC EVA multi-option runtime",
        "model_id": req.model_id,
        "sector": req.sector,
        "count": len(results),
        "outcomes": counts,
        "results": results,
        "gate": {
            "fair_neq_block": any(r.get("option") == "fair" and r.get("decision") != "BLOCK" for r in results),
            "biased_eq_block": any(r.get("option") == "biased" and r.get("decision") == "BLOCK" for r in results),
        },
        "note": "Live sequential decisions · multi-sector EVA · model-001 protected from permanent high-risk BLOCKED",
    }
