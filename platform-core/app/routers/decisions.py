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
from app.db.models import AIModel, Decision
from app.core.dependencies import current_user
from app.core.config import settings
from app.services.governance_bridge import Evidence, evaluate
from app.services.audit_writer import append_audit
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

    # Persist decision
    d = Decision(model_pk=model.id, decision=v.decision, svs=v.svs, risk=v.risk,
                 compliance=v.compliance, sovereign=v.sovereign, seal=v.seal,
                 latency_ms=v.latency_ms, block_reasons=" | ".join(v.block_reasons))
    db.add(d)
    # If blocked, reflect on model status for critical tiers
    if v.decision == "BLOCK" and ev.risk_tier in ("HIGH", "UNACCEPTABLE"):
        model.status = "BLOCKED"
    db.commit(); db.refresh(d)

    # Immutable audit + event
    append_audit(db, "AI_DECISION", {"model_id": req.model_id, "decision": v.decision,
                 "svs": v.svs, "seal": v.seal[:16]}, classification="GOVERNANCE",
                 actor_class=user.get("role", "SYSTEM"))
    bus.emit("decisions", {"model_id": req.model_id, "decision": v.decision, "svs": v.svs})

    return {
        "model_id": v.model_id, "decision": v.decision, "svs": v.svs, "risk": v.risk,
        "compliance": v.compliance, "stability": v.stability, "disparate_impact": v.disparate_impact,
        "spd": v.spd, "ecs": v.ecs, "sovereign": v.sovereign, "sovereign_svs": v.sovereign_svs,
        "seal": v.seal, "latency_ms": v.latency_ms, "budget_ms": settings.governance_overhead_budget_ms,
        "within_budget": v.latency_ms <= settings.governance_overhead_budget_ms,
        "block_reasons": v.block_reasons,
    }

@router.get("")
def list_decisions(db: Session = Depends(get_db), _: dict = Depends(current_user)):
    rows = db.execute(select(Decision).order_by(Decision.id.desc()).limit(100)).scalars().all()
    return [{"id": d.id, "decision": d.decision, "svs": d.svs, "sovereign": d.sovereign,
             "latency_ms": d.latency_ms, "created_at": d.created_at.isoformat()} for d in rows]
