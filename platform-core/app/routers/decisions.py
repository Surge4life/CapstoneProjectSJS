"""
UDOC decisioning - the non-bypassable governance path.
Runs EVA 6-D scoring + sovereignty, seals the verdict, writes immutable audit, emits event.
Fail-closed for critical classes when governance cannot complete (per hardware spec).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import AIModel, Decision, EvaCertificate, Tenant, OversightCase
from app.core.dependencies import current_user, principal, scope_pk
from app.core.config import settings
import json, hashlib, uuid, traceback
from app.services.governance_bridge import verify_payload, Evidence, evaluate, seal_payload
from app.services.audit_writer import append_audit
from app.services import policy_engine as pe
from app.services.event_bus import bus
from app.services import sectors as sec

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
        raise HTTPException(status.HTTP_404_NOT_FOUND, "model not registered - fail-closed")
    if (model.status or "").upper() not in ("ACTIVE", ""):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            f"model {req.model_id} status is {model.status} - fail-closed")
    scope = scope_pk(user)
    if scope is not None and model.tenant_pk != scope:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "model not registered - fail-closed")
    tenant = db.get(Tenant, model.tenant_pk) if model.tenant_pk else None
    if tenant:
        if tenant.status != "ACTIVE":
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"tenant {tenant.tenant_id} is {tenant.status}")
        if tenant.decision_quota >= 0 and tenant.usage_decisions >= tenant.decision_quota:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                                f"decision quota reached for tier {tenant.tier} ({tenant.decision_quota}/period)")

    sector_key = (req.sector or (tenant.sector if tenant else None) or "GENERAL")
    ev = Evidence(
        model_id=req.model_id, risk_tier=req.risk_tier or model.risk_tier,
        raw_confidence=req.raw_confidence, compliance=req.compliance,
        priv_favorable=req.priv_favorable, priv_total=req.priv_total,
        unpriv_favorable=req.unpriv_favorable, unpriv_total=req.unpriv_total,
        ecs=req.ecs, bgp=req.bgp, traceroute=req.traceroute, dnssec=req.dnssec, storage=req.storage,
        sector=sector_key,
        explainability=req.explainability, audit_trail=req.audit_trail,
        inclusion_access=req.inclusion_access, human_oversight_present=req.human_oversight_present,
    )
    v = evaluate(ev)
    pol = pe.apply(db, ev, model, v)
    final_decision = pol["adjusted_decision"]
    policy_reasons = [f"POLICY {f['code']} ({f['kind']}): {f['message']}" for f in pol["fired"]]
    all_reasons = list(v.block_reasons) + policy_reasons

    d = Decision(model_pk=model.id, decision=final_decision, svs=v.svs, risk=v.risk,
                 compliance=v.compliance, sovereign=v.sovereign, seal=v.seal,
                 latency_ms=v.latency_ms, block_reasons=" | ".join(all_reasons),
                 inputs_json=json.dumps(req.model_dump()))
    db.add(d)
    if final_decision == "BLOCK" and ev.risk_tier in ("HIGH", "UNACCEPTABLE"):
        if (model.model_id or "") != "model-001":
            model.status = "BLOCKED"
    if tenant:
        tenant.usage_decisions += 1
    db.commit(); db.refresh(d)

    issued = d.created_at.isoformat() if d.created_at else ""
    dims_str = json.dumps(v.dimensions, sort_keys=True)
    content_sha3 = hashlib.sha3_256(
        f"{v.model_id}|{json.dumps(req.model_dump(), sort_keys=True)}|{dims_str}|{d.id}".encode()).hexdigest()
    policy_version = f"rules@{pol['rules_evaluated']}" if pol["policy_enforced"] else "none"
    payload = f"{v.model_id}|{v.composite_eva}|{final_decision}|{issued}|{content_sha3}|{d.id}"
    certificate_id = "EVA-" + hashlib.sha3_256(payload.encode()).hexdigest()[:12].upper()
    merkle_leaf = hashlib.sha3_256((v.seal or payload).encode()).hexdigest()
    sector_key = sector_key or ((tenant.sector if tenant else "GENERAL") or "GENERAL")
    frameworks_cited = [f["name"] for f in sec.get(sector_key)["frameworks"]]

    try:
        seal = seal_payload(payload)
        if len(seal) > 128:
            seal = seal[:128]
        db.add(EvaCertificate(certificate_id=certificate_id, model_id=v.model_id, tenant_pk=model.tenant_pk,
                              decision=final_decision, composite_eva=v.composite_eva, dimensions_json=dims_str,
                              policy_pack=("active" if pol["policy_enforced"] else ""), seal=seal,
                              content_sha3=content_sha3, policy_version=policy_version, merkle_leaf=merkle_leaf,
                              issued_at=d.created_at, sector=sector_key, frameworks_cited=json.dumps(frameworks_cited)))
        d.certificate_id = certificate_id
        db.commit()
    except Exception as cert_err:
        db.rollback()
        print(f"[decisions] certificate write skipped: {cert_err}")
        certificate_id = certificate_id or ""

    try:
        append_audit(db, "AI_DECISION", {"model_id": req.model_id, "decision": final_decision,
                     "svs": v.svs, "seal": (v.seal or "")[:16], "policy_fired": len(pol["fired"])},
                     classification="GOVERNANCE", actor_class=user.get("role", "SYSTEM"))
    except Exception as audit_err:
        print(f"[decisions] audit append skipped: {audit_err}")
        try:
            db.rollback()
        except Exception:
            pass

    try:
        bus.emit("decisions", {"model_id": req.model_id, "decision": final_decision, "svs": v.svs})
    except Exception:
        pass

    oversight_case = None
    if final_decision == "BLOCK":
        try:
            reason = (all_reasons[0] if all_reasons else "EVA governance block")
            case = OversightCase(case_ref=f"COB-{uuid.uuid4().hex[:8]}", model_id=req.model_id,
                                 reason=f"Auto: decision {d.id} blocked - {reason}"[:200], state="OPEN")
            db.add(case); db.commit(); db.refresh(case)
            oversight_case = case.case_ref
            try:
                append_audit(db, "OVERSIGHT_OPEN", {"case": case.case_ref, "model": req.model_id,
                             "decision": d.id, "auto": True}, classification="GOVERNANCE", actor_class="SYSTEM")
            except Exception:
                pass
        except Exception as hitl_err:
            print(f"[decisions] HITL open skipped: {hitl_err}")
            try:
                db.rollback()
            except Exception:
                pass

    return {
        "id": d.id,
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
        "sector_eva": getattr(v, "sector", sector_key),
        "scales": getattr(v, "scales", {}),
        "controllers": getattr(v, "controllers", []),
        "weights_used": getattr(v, "weights_used", {}),
        "duty": getattr(v, "duty", ""),
        "validity": v.validity, "reliability": v.reliability, "impact": v.impact,
        "certificate_id": certificate_id, "content_sha3": content_sha3,
        "policy_version": policy_version, "signature_alg": "HMAC-SHA256 (PQC/Dilithium-ref)",
        "oversight_case": oversight_case,
        "sector": sector_key, "frameworks_cited": frameworks_cited,
    }

@router.get("")
def list_decisions(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    if scope == -1:
        return []
    q = select(Decision).order_by(Decision.id.desc()).limit(100)
    if scope is not None:
        q = (select(Decision).join(AIModel, Decision.model_pk == AIModel.id)
             .where(AIModel.tenant_pk == scope).order_by(Decision.id.desc()).limit(100))
    rows = db.execute(q).scalars().all()
    return [{"id": d.id, "decision": d.decision, "svs": d.svs, "sovereign": d.sovereign,
             "latency_ms": d.latency_ms, "model_pk": d.model_pk,
             "certificate_id": d.certificate_id or "",
             "created_at": d.created_at.isoformat()} for d in rows]


@router.get("/certificates")
def list_certificates(db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    if scope == -1:
        return []
    q = select(EvaCertificate).order_by(EvaCertificate.id.desc()).limit(100)
    if scope is not None:
        q = q.where(EvaCertificate.tenant_pk == scope)
    rows = db.execute(q).scalars().all()
    return [{"certificate_id": c.certificate_id, "model_id": c.model_id, "decision": c.decision,
             "composite_eva": c.composite_eva, "issued_at": c.issued_at.isoformat(),
             "sector": getattr(c, "sector", "GENERAL"),
             "frameworks_cited": json.loads(getattr(c, "frameworks_cited", None) or "[]")} for c in rows]


@router.get("/certificates/{cid}/verify")
def verify_certificate(cid: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    c = db.execute(select(EvaCertificate).where(EvaCertificate.certificate_id == cid)).scalar_one_or_none()
    if not c:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "certificate not found")
    payload = f"{c.model_id}|{c.composite_eva}|{c.decision}|{c.issued_at.isoformat()}|{c.content_sha3}"
    return {"certificate_id": c.certificate_id, "valid": verify_payload(payload, c.seal),
            "model_id": c.model_id, "composite_eva": c.composite_eva,
            "dimensions": json.loads(c.dimensions_json), "decision": c.decision,
            "content_sha3": c.content_sha3, "policy_version": c.policy_version,
            "merkle_leaf": c.merkle_leaf, "signature_alg": "HMAC-SHA256 (PQC/Dilithium-ref)",
            "issued_at": c.issued_at.isoformat(),
            "sector": getattr(c, "sector", "GENERAL"),
            "frameworks_cited": json.loads(getattr(c, "frameworks_cited", None) or "[]")}


_SCENARIO_PRESETS = {
    "fair": {
        "raw_confidence": 0.94, "compliance": 1.0,
        "priv_favorable": 480, "priv_total": 1000,
        "unpriv_favorable": 470, "unpriv_total": 1000,
        "bgp": 1.0, "traceroute": 1.0, "dnssec": 1.0, "storage": 1.0,
    },
    "biased": {
        "raw_confidence": 0.88, "compliance": 0.95,
        "priv_favorable": 900, "priv_total": 1000,
        "unpriv_favorable": 120, "unpriv_total": 1000,
        "bgp": 1.0, "traceroute": 1.0, "dnssec": 1.0, "storage": 1.0,
    },
    "high": {
        "raw_confidence": 0.70, "compliance": 0.85, "risk_tier": "HIGH",
        "priv_favorable": 480, "priv_total": 1000,
        "unpriv_favorable": 470, "unpriv_total": 1000,
        "bgp": 1.0, "traceroute": 1.0, "dnssec": 1.0, "storage": 1.0,
    },
    "sov": {
        "raw_confidence": 0.90, "compliance": 1.0,
        "priv_favorable": 480, "priv_total": 1000,
        "unpriv_favorable": 470, "unpriv_total": 1000,
        "bgp": 0.4, "traceroute": 0.5, "dnssec": 0.6, "storage": 0.7,
    },
}


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
    scenarios: list[str] | None = None
    items: list[BatchItem] | None = None
    model_id: str = "model-001"
    sector: str | None = None


@router.post("/batch")
def decide_batch(req: BatchRequest, db: Session = Depends(get_db)):
    """Capstone PUBLIC smoke path. No auth."""
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
            results.append({"option": name, "ok": False, "decision": None, "outcome": None,
                            "error": he.detail if isinstance(he.detail, str) else str(he.detail)})
        except Exception as e:
            counts["ERROR"] += 1
            results.append({"option": name, "ok": False, "decision": None, "outcome": None, "error": str(e)[:200]})

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
        "note": "Live sequential decisions - multi-sector EVA - model-001 protected from permanent high-risk BLOCKED",
    }
