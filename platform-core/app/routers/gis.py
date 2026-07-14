"""
GIS + CET/CTE + GBS router — the live HTTP surface for the G.O.D.S.
Intelligence System and the GBS franchise/pillar layer.

Endpoint surface mirrors governance-engines/gis/ (the TS reference package)
so the two stay traceable to each other. See GIS_ECOSYSTEM_BUILD_NOTES.md at
the repo root for the full alignment rationale.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.core.dependencies import require_role
from app.services import gis_engine, cetcte_engine, gbs_engine

router = APIRouter(prefix="/gis", tags=["GIS · GBS-SETHS Intelligence & Franchise Layer"])


# ───────────────────────── GIS decisions ─────────────────────────

class PillarFlags(BaseModel):
    respects_human_dignity: bool = False
    affirms_contribution_potential: bool = False
    politically_neutral: bool = False
    ethically_sound: bool = False
    has_governance_review: bool = False
    has_transparent_record: bool = False
    respects_founder_limits: bool = False
    has_human_oversight: bool = False
    supports_reintegration_cohort: bool = False
    considers_long_term_impact: bool = False
    no_corruption_risk: bool = False
    is_evidence_based: bool = False


class DecisionReq(BaseModel):
    decision_type: str
    learner_ref: Optional[str] = None
    domain: str = "SETHS"
    context: dict = Field(default_factory=dict)
    pillar_flags: PillarFlags = Field(default_factory=PillarFlags)


@router.post("/decisions")
def make_decision(req: DecisionReq, db: Session = Depends(get_db),
                   _=Depends(require_role("operator", "admin"))):
    try:
        gi = gis_engine.GISInput(
            decision_type=req.decision_type, learner_ref=req.learner_ref, domain=req.domain,
            context=req.context, pillar_flags=req.pillar_flags.model_dump(), requested_by="api",
        )
        return gis_engine.make_decision(db, gi)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.get("/decisions/types")
def decision_types():
    return {"decision_types": list(gis_engine.DECISION_TYPES), "pillars": gis_engine.PILLAR_CHECKS}


# ───────────────────────── CET/CTE participant journey ─────────────────────────

class AssignReq(BaseModel):
    cohort: str
    stream: str


class AffirmationReq(BaseModel):
    what_do_you_want_to_change: str = ""
    why_now: str = ""
    who_are_you_becoming: str = ""


class AIReadinessReq(BaseModel):
    stage: int


@router.post("/participants/{ref}/assign")
def assign(ref: str, req: AssignReq, db: Session = Depends(get_db),
           _=Depends(require_role("operator", "admin"))):
    try:
        return cetcte_engine.assign_cohort_stream(db, ref, req.cohort, req.stream)
    except (ValueError, LookupError) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.post("/participants/{ref}/self-affirmation")
def self_affirmation(ref: str, req: AffirmationReq, db: Session = Depends(get_db),
                      _=Depends(require_role("operator", "admin"))):
    try:
        return cetcte_engine.record_self_affirmation(db, ref, req.model_dump())
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.post("/participants/{ref}/advance")
def advance(ref: str, db: Session = Depends(get_db),
            _=Depends(require_role("operator", "admin"))):
    try:
        return cetcte_engine.advance_stage(db, ref)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.post("/participants/{ref}/ai-readiness")
def ai_readiness(ref: str, req: AIReadinessReq, db: Session = Depends(get_db),
                  _=Depends(require_role("operator", "admin"))):
    try:
        return cetcte_engine.update_ai_readiness(db, ref, req.stage)
    except (ValueError, LookupError) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.get("/participants/{ref}/journey")
def journey(ref: str, db: Session = Depends(get_db)):
    try:
        return cetcte_engine.journey(db, ref)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


# ───────────────────────── GBS pillars & franchise registry ─────────────────────────

@router.get("/gbs/pillars")
def pillars():
    return {"constitutional_pillars": gbs_engine.CONSTITUTIONAL_PILLARS,
            "gbs_universal_pillars": gbs_engine.GBS_UNIVERSAL_PILLARS}


class NodeReq(BaseModel):
    layer: int
    name: str
    territory: str = "South Africa"
    parent_node_ref: str = ""


@router.post("/gbs/nodes")
def register_node(req: NodeReq, db: Session = Depends(get_db),
                   _=Depends(require_role("admin"))):
    try:
        return gbs_engine.register_node(db, req.layer, req.name, req.territory, req.parent_node_ref)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.get("/gbs/nodes")
def list_nodes(layer: Optional[int] = None, db: Session = Depends(get_db)):
    return gbs_engine.list_nodes(db, layer)


class StatusReq(BaseModel):
    status: str
    reason: str = ""


@router.post("/gbs/nodes/{node_ref}/status")
def set_status(node_ref: str, req: StatusReq, db: Session = Depends(get_db),
                _=Depends(require_role("admin"))):
    try:
        return gbs_engine.set_licence_status(db, node_ref, req.status, req.reason)
    except (ValueError, LookupError) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


class AuditReq(BaseModel):
    compliance_score: float
    curriculum_fidelity_pct: float


@router.post("/gbs/nodes/{node_ref}/audit")
def audit_node(node_ref: str, req: AuditReq, db: Session = Depends(get_db),
               _=Depends(require_role("admin"))):
    try:
        return gbs_engine.record_compliance_audit(db, node_ref, req.compliance_score, req.curriculum_fidelity_pct)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
