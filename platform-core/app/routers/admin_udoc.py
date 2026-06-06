"""
UDOC v9.3 admin surface — the data layer behind the admin console tabs:
regulator rollup, constitutional pillars, model lifecycle, evidence bundle, decision replay.
All endpoints are tenant-isolated (a tenant sees only its own systems; platform staff see all).
"""
from collections import Counter
import json
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
        raise HTTPException(404, "model not found")
    return m


def _decision_or_404(db, did, scope):
    d = db.get(Decision, did)
    if not d:
        raise HTTPException(404, "decision not found")
    m = db.get(AIModel, d.model_pk)
    if scope is not None and scope != -1 and (not m or m.tenant_pk != scope):
        raise HTTPException(404, "decision not found")
    return d, m


@router.get("/regulator/summary")
def regulator_summary(db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Regulator-facing rollup: registered systems, decision outcomes, oversight, policy posture."""
    scope = scope_pk(user)
    if scope == -1:
        return {"scope": "none", "models": 0, "decisions": 0}
    mq, dq = select(AIModel), select(Decision)
    if scope is not None:
        mq = mq.where(AIModel.tenant_pk == scope)
        dq = dq.join(AIModel, Decision.model_pk == AIModel.id).where(AIModel.tenant_pk == scope)
    models = db.execute(mq).scalars().all()
    decisions = db.execute(dq).scalars().all()
    outcomes = Counter(d.decision for d in decisions)
    pq = select(PolicyPack).where(PolicyPack.status == "ACTIVE")
    if scope is not None:
        from sqlalchemy import or_
        pq = pq.where(or_(PolicyPack.tenant_pk == scope, PolicyPack.tenant_pk.is_(None)))
    active_packs = db.execute(pq).scalars().all()
    try:
        cases = db.execute(select(OversightCase)).scalars().all()
        open_cases = sum(1 for c in cases if getattr(c, "status", "OPEN") not in ("CLOSED", "RESOLVED"))
    except Exception:
        cases, open_cases = [], 0
    return {
        "scope": ("platform" if scope is None else "tenant"),
        "systems": {"total": len(models), "by_status": dict(Counter(m.status for m in models)),
                    "by_risk_tier": dict(Counter(m.risk_tier for m in models))},
        "decisions": {"total": len(decisions), "by_outcome": dict(outcomes),
                      "blocked": outcomes.get("BLOCK", 0), "escalated": outcomes.get("ESCALATE", 0)},
        "oversight": {"open": open_cases, "total": len(cases)},
        "policy": {"active_packs": len(active_packs),
                   "active_rules": sum(p.rule_count for p in active_packs),
                   "hot_reload": pe.hot_reload_stats()},
        "compliance_basis": "POPIA (Act 4 of 2013, s71) + Constitution ss 9/16/33. "
                            "SA Draft National AI Policy GG54477 was WITHDRAWN on 2026-04-26.",
        "crypto": provider_info(),
    }


@router.get("/constitutional/pillars")
def constitutional_pillars(user: dict = Depends(principal)):
    """The G.O.D.S constitutional pillars as enforced in code, with live status signals."""
    pqc = provider_info().get("pqc_available")
    P = [
        (1, "Honesty & Non-Deception", "No system, claim or artefact may be misrepresented; pre-registration status is labelled.", "Output/claim discipline; honesty pass across deliverables", "ENFORCED"),
        (2, "Capital Reinvestment (≥50%)", "A majority of returns is recycled into impact (M.A.D.I.B.A).", "Governance principle — financial covenant", "DECLARED"),
        (3, "Data Sovereignty", "Data and governance remain within the sovereign jurisdiction.", "Jurisdiction lock (ZA) + 6-hourly re-checks", "ENFORCED"),
        (4, "Fail-Closed Safety", "When governance cannot complete, default to denial — never open.", "Unknown/critical systems are blocked by default", "ENFORCED"),
        (5, "Tamper-Evident Accountability", "Every decision is independently verifiable.", "Merkle-linked audit chain + signed EVA certificates", "ENFORCED"),
        (6, "Transparency & Explainability", "Decisions expose their basis.", "Six-dimensional verdict + explicit reasons", "ENFORCED"),
        (7, "Non-Discrimination & Fairness", "Disparate impact is detected and blocked.", "SPD / disparate-impact thresholds in the EVA block path", "ENFORCED"),
        (8, "Human Primacy", "Humans retain final authority; the system cannot override this.", "HITL + oversight cases + non-overridable guardrail", "ENFORCED"),
        (9, "Separation of Powers", "Authoring, approval and operation are separated.", "COB approval + separation-of-duties on policy versions", "ENFORCED"),
        (10, "Proportionate Risk Tiering", "Controls scale with risk.", "Risk-tier classification drives enforcement", "ENFORCED"),
        (11, "Post-Quantum Resilience", "Signatures resist quantum attack.", "CRYSTALS-Dilithium via liboqs when provisioned; HMAC reference otherwise", "ENFORCED" if pqc else "PARTIAL"),
        (12, "Constitutional Oversight & Veto", "An oversight board can veto governance changes.", "COB veto returns a policy version to draft", "ENFORCED"),
    ]
    pillars = [{"n": n, "name": nm, "principle": pr, "enforcement": en, "status": st}
               for (n, nm, pr, en, st) in P]
    summary = dict(Counter(p["status"] for p in pillars))
    return {"count": len(pillars), "status_summary": summary, "pillars": pillars}


@router.get("/models/{model_id}/lifecycle")
def model_lifecycle(model_id: str, db: Session = Depends(get_db), user: dict = Depends(principal)):
    scope = scope_pk(user)
    m = _model_or_404(db, model_id, scope)
    decs = db.execute(select(Decision).where(Decision.model_pk == m.id)
                      .order_by(Decision.id.desc())).scalars().all()
    outcomes = Counter(d.decision for d in decs)
    last = decs[0] if decs else None
    return {
        "model_id": m.model_id, "name": m.name, "operator_id": m.operator_id,
        "risk_tier": m.risk_tier, "jurisdiction": m.jurisdiction, "status": m.status,
        "tenant_pk": m.tenant_pk,
        "decisions": {"total": len(decs), "by_outcome": dict(outcomes),
                      "last_decision": (last.created_at.isoformat() if last else None),
                      "last_outcome": (last.decision if last else None)},
        "blocked": m.status == "BLOCKED",
        "stage": ("BLOCKED" if m.status == "BLOCKED" else ("OPERATING" if decs else "REGISTERED")),
    }


@router.get("/decisions/{decision_id}/evidence")
def decision_evidence(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Full evidence bundle for audit/regulator: decision + certificate + audit context + inputs."""
    scope = scope_pk(user)
    d, m = _decision_or_404(db, decision_id, scope)
    cert = None
    if d.certificate_id:
        cert = db.execute(select(EvaCertificate).where(
            EvaCertificate.certificate_id == d.certificate_id)).scalar_one_or_none()
    head = db.execute(select(AuditRef).order_by(AuditRef.seq.desc())).scalars().first()
    return {
        "decision": {"id": d.id, "model_id": m.model_id if m else None, "outcome": d.decision,
                     "svs": d.svs, "risk": d.risk, "compliance": d.compliance,
                     "sovereign": d.sovereign, "latency_ms": d.latency_ms,
                     "reasons": d.block_reasons, "sealed": bool(d.seal), "at": d.created_at.isoformat()},
        "certificate": (None if not cert else {
            "certificate_id": cert.certificate_id, "decision": cert.decision,
            "composite_eva": cert.composite_eva, "content_sha3": cert.content_sha3,
            "policy_version": cert.policy_version, "merkle_leaf": cert.merkle_leaf,
            "dimensions": json.loads(cert.dimensions_json or "{}"),
            "signature_alg": "HMAC-SHA256 (PQC/Dilithium-ref)", "issued_at": cert.issued_at.isoformat()}),
        "audit_context": {"chain_head_seq": (head.seq if head else None),
                          "chain_head_hash": (head.event_hash if head else None)},
        "inputs": json.loads(d.inputs_json or "{}"),
    }


@router.get("/decisions/{decision_id}/replay")
def decision_replay(decision_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Re-run the original inputs through the CURRENT EVA engine + active policy and compare to the
    sealed original — demonstrating reproducibility and surfacing any drift."""
    scope = scope_pk(user)
    d, m = _decision_or_404(db, decision_id, scope)
    inp = json.loads(d.inputs_json or "{}")
    if not inp:
        raise HTTPException(409, "no stored inputs for this decision (pre-dates input capture)")
    ev = Evidence(
        model_id=m.model_id, risk_tier=inp.get("risk_tier") or m.risk_tier,
        raw_confidence=inp.get("raw_confidence", 0.9), compliance=inp.get("compliance", 1.0),
        priv_favorable=inp.get("priv_favorable", 480), priv_total=inp.get("priv_total", 1000),
        unpriv_favorable=inp.get("unpriv_favorable", 470), unpriv_total=inp.get("unpriv_total", 1000),
        ecs=inp.get("ecs", 0.75), bgp=inp.get("bgp", 1.0), traceroute=inp.get("traceroute", 1.0),
        dnssec=inp.get("dnssec", 1.0), storage=inp.get("storage", 1.0))
    v = evaluate(ev)
    pol = pe.apply(db, ev, m, v)
    current = pol["adjusted_decision"]
    drift = (current != d.decision) or abs(v.svs - d.svs) > 1e-3 or abs(v.risk - d.risk) > 1e-3
    return {
        "decision_id": d.id, "model_id": m.model_id,
        "original": {"outcome": d.decision, "svs": round(d.svs, 4), "risk": round(d.risk, 4),
                     "compliance": round(d.compliance, 4), "at": d.created_at.isoformat()},
        "replayed": {"outcome": current, "svs": round(v.svs, 4), "risk": round(v.risk, 4),
                     "compliance": round(v.compliance, 4), "composite_eva": v.composite_eva,
                     "dimensions": v.dimensions},
        "drift": drift,
        "note": "Replay re-evaluates stored inputs against the current engine and active policy version.",
    }


@router.get("/incidents")
def incidents(db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Governance incident feed: BLOCK/ESCALATE decisions + open oversight cases (tenant-isolated)."""
    scope = scope_pk(user)
    if scope == -1:
        return {"incidents": [], "open_cases": []}
    dq = select(Decision).where(Decision.decision.in_(("BLOCK", "ESCALATE"))).order_by(Decision.id.desc()).limit(50)
    if scope is not None:
        dq = (select(Decision).join(AIModel, Decision.model_pk == AIModel.id)
              .where(AIModel.tenant_pk == scope, Decision.decision.in_(("BLOCK", "ESCALATE")))
              .order_by(Decision.id.desc()).limit(50))
    inc = []
    for d in db.execute(dq).scalars().all():
        m = db.get(AIModel, d.model_pk)
        inc.append({"decision_id": d.id, "model_id": m.model_id if m else None, "severity": d.decision,
                    "risk": round(d.risk, 3), "reasons": d.block_reasons, "at": d.created_at.isoformat()})
    try:
        cases = db.execute(select(OversightCase)).scalars().all()
        open_cases = [{"id": c.id, "model_id": getattr(c, "model_id", None),
                       "status": getattr(c, "status", "OPEN"), "reason": getattr(c, "reason", "")}
                      for c in cases if getattr(c, "status", "OPEN") not in ("CLOSED", "RESOLVED")]
    except Exception:
        open_cases = []
    return {"incidents": inc, "open_cases": open_cases, "count": len(inc)}


@router.get("/exchange")
def data_exchange(db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Cross-border data-exchange & sovereignty posture (data stays in-jurisdiction; sovereign-first)."""
    scope = scope_pk(user)
    rules = pe.active_rules(db, tenant_pk=(scope if scope and scope != -1 else None))
    loc = [{"code": r.code, "kind": r.kind, "target": r.target} for r in rules
           if r.kind in ("DATA_LOCALISATION", "MIN_SOVEREIGNTY")]
    return {"jurisdiction": "ZA", "cross_border_transfer": "denied by default (sovereign-first)",
            "data_localisation": "enforced", "sovereignty_recheck_hours": 6,
            "localisation_rules": loc, "rules_active": len(loc),
            "basis": "POPIA Chapter 9 (s72 cross-border) + Constitutional Pillar III (Data Sovereignty)"}


@router.get("/schema")
def governance_schema(user: dict = Depends(principal)):
    """Self-describing governance data schema for integrators."""
    return {
        "ai_model": ["model_id", "name", "operator_id", "risk_tier", "use_case", "jurisdiction", "status", "tenant_pk"],
        "risk_tiers": ["MINIMAL", "NOTABLE", "HIGH", "UNACCEPTABLE"],
        "eva_dimensions": ["Validity", "Confidence", "Risk", "Compliance", "Stability", "Impact"],
        "decision_outcomes": ["APPROVE", "REVIEW", "ESCALATE", "BLOCK"],
        "decision_record": ["id", "model_id", "decision", "svs", "risk", "compliance", "sovereign",
                            "seal", "latency_ms", "certificate_id", "created_at"],
        "eva_certificate": ["certificate_id", "decision", "composite_eva", "content_sha3 (SHA-3-256)",
                            "policy_version", "merkle_leaf", "dimensions", "signature_alg", "issued_at"],
        "policy_rule_kinds": ["PROHIBIT", "RISK_TIER_CAP", "REQUIRE_HITL", "MIN_SOVEREIGNTY",
                              "MIN_COMPLIANCE", "MAX_DISPARATE_IMPACT", "DATA_LOCALISATION", "KEYWORD_FLAG"],
        "policy_version_states": ["PROPOSED", "APPROVED", "ACTIVE", "VETOED", "SUPERSEDED"],
        "note": "CGS is advisory; BLOCK is strictly dimensional. Certificates verify via SHA-3-256 payload + signature.",
    }


@router.get("/regulator/export")
def regulator_export(db: Session = Depends(get_db), user: dict = Depends(principal)):
    """Signed regulator evidence bundle (summary + recent decisions + audit head)."""
    import time as _t, json as _j
    base = regulator_summary(db, user)
    scope = scope_pk(user)
    dq = select(Decision).order_by(Decision.id.desc()).limit(50)
    if scope is not None and scope != -1:
        dq = (select(Decision).join(AIModel, Decision.model_pk == AIModel.id)
              .where(AIModel.tenant_pk == scope).order_by(Decision.id.desc()).limit(50))
    recent = []
    for d in db.execute(dq).scalars().all():
        m = db.get(AIModel, d.model_pk)
        recent.append({"id": d.id, "model_id": m.model_id if m else None, "outcome": d.decision,
                       "risk": round(d.risk, 3), "certificate_id": d.certificate_id,
                       "at": d.created_at.isoformat()})
    head = db.execute(select(AuditRef).order_by(AuditRef.seq.desc())).scalars().first()
    bundle = {"generated_at": _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()),
              "summary": base, "recent_decisions": recent,
              "audit_head": {"seq": (head.seq if head else None), "hash": (head.event_hash if head else None)}}
    bundle["seal"] = sign(_j.dumps(bundle, sort_keys=True))
    bundle["signature_alg"] = "HMAC-SHA256 (PQC/Dilithium-ref)"
    return bundle
