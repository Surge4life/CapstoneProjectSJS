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
from app.db.models import AIModel, Decision, EvaCertificate
from app.core.dependencies import current_user
from app.core.config import settings
import json, hashlib
from app.services.governance_bridge import Evidence, evaluate, seal_payload
from app.services.audit_writer import append_audit
from app.services import policy_engine as pe
from app.services.event_bus import bus

router = APIRouter(prefix="/decisions", tags=["UDOC decisions"])

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

@router.post("")
def decide(req: DecisionReq, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    model = db.execute(select(AIModel).where(AIModel.model_id == req.model_id)).scalar_one_or_none()
    if not model:
        # Fail-closed: unknown model is blocked, not allowed.
        raise HTTPException(status.HTTP_404_NOT_FOUND, "model not registered — fail-closed")

    ev = Evidence(
        model_id=req.model_id, risk_tier=req.risk_tier or model.risk_tier,
        raw_confidence=req.raw_confidence, compliance=req.compliance,
        priv_favorable=req.priv_favorable, priv_total=req.priv_total,
        unpriv_favorable=req.unpriv_favorable, unpriv_total=req.unpriv_total,
        ecs=req.ecs, bgp=req.bgp, traceroute=req.traceroute, dnssec=req.dnssec, storage=req.storage,
    )
    v = evaluate(ev)
    # Policy-to-Code layer: enforce active, human-approved rules compiled from uploaded legislation.
    pol = pe.apply(db, ev, model, v)
    final_decision = pol["adjusted_decision"]
    policy_reasons = [f"POLICY {f['code']} ({f['kind']}): {f['message']}" for f in pol["fired"]]
    all_reasons = list(v.block_reasons) + policy_reasons

    # Persist decision (policy-adjusted)
    d = Decision(model_pk=model.id, decision=final_decision, svs=v.svs, risk=v.risk,
                 compliance=v.compliance, sovereign=v.sovereign, seal=v.seal,
                 latency_ms=v.latency_ms, block_reasons=" | ".join(all_reasons))
    db.add(d)
    # If blocked, reflect on model status for critical tiers
    if final_decision == "BLOCK" and ev.risk_tier in ("HIGH", "UNACCEPTABLE"):
        model.status = "BLOCKED"
    db.commit(); db.refresh(d)

    certificate_id = None
    if final_decision == "APPROVE":
        issued = d.created_at.isoformat()
        dims_str = json.dumps(v.dimensions, sort_keys=True)
        payload = f"{v.model_id}|{v.composite_eva}|{final_decision}|{issued}|{dims_str}"
        certificate_id = "EVA-" + hashlib.sha256(payload.encode()).hexdigest()[:12].upper()
        db.add(EvaCertificate(certificate_id=certificate_id, model_id=v.model_id, decision=final_decision,
                              composite_eva=v.composite_eva, dimensions_json=dims_str,
                              policy_pack=("active" if pol["policy_enforced"] else ""),
                              seal=seal_payload(payload), issued_at=d.created_at))
        db.commit()

    # Immutable audit + event
    append_audit(db, "AI_DECISION", {"model_id": req.model_id, "decision": final_decision,
                 "svs": v.svs, "seal": v.seal[:16], "policy_fired": len(pol["fired"])},
                 classification="GOVERNANCE", actor_class=user.get("role", "SYSTEM"))
    bus.emit("decisions", {"model_id": req.model_id, "decision": final_decision, "svs": v.svs})

    return {
        "model_id": v.model_id, "decision": final_decision, "base_decision": v.decision,
        "svs": v.svs, "risk": v.risk,
        "compliance": v.compliance, "stability": v.stability, "disparate_impact": v.disparate_impact,
        "spd": v.spd, "ecs": v.ecs, "sovereign": v.sovereign, "sovereign_svs": v.sovereign_svs,
        "seal": v.seal, "latency_ms": v.latency_ms, "budget_ms": settings.governance_overhead_budget_ms,
        "within_budget": v.latency_ms <= settings.governance_overhead_budget_ms,
        "block_reasons": all_reasons,
        "policy_enforced": pol["policy_enforced"], "policy_rules_evaluated": pol["rules_evaluated"],
        "policy_findings": pol["fired"],
        "composite_eva": v.composite_eva, "dimensions": v.dimensions,
        "validity": v.validity, "reliability": v.reliability, "impact": v.impact,
        "certificate_id": certificate_id,
    }

@router.get("")
def list_decisions(db: Session = Depends(get_db), _: dict = Depends(current_user)):
    rows = db.execute(select(Decision).order_by(Decision.id.desc()).limit(100)).scalars().all()
    return [{"id": d.id, "decision": d.decision, "svs": d.svs, "sovereign": d.sovereign,
             "latency_ms": d.latency_ms, "created_at": d.created_at.isoformat()} for d in rows]


@router.get("/certificates")
def list_certificates(db: Session = Depends(get_db), _: dict = Depends(current_user)):
    rows = db.execute(select(EvaCertificate).order_by(EvaCertificate.id.desc()).limit(100)).scalars().all()
    return [{"certificate_id": c.certificate_id, "model_id": c.model_id, "decision": c.decision,
             "composite_eva": c.composite_eva, "issued_at": c.issued_at.isoformat()} for c in rows]


@router.get("/certificates/{cid}/verify")
def verify_certificate(cid: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    c = db.execute(select(EvaCertificate).where(EvaCertificate.certificate_id == cid)).scalar_one_or_none()
    if not c:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "certificate not found")
    payload = f"{c.model_id}|{c.composite_eva}|{c.decision}|{c.issued_at.isoformat()}|{c.dimensions_json}"
    return {"certificate_id": c.certificate_id, "valid": seal_payload(payload) == c.seal,
            "model_id": c.model_id, "composite_eva": c.composite_eva,
            "dimensions": json.loads(c.dimensions_json), "decision": c.decision,
            "issued_at": c.issued_at.isoformat()}
