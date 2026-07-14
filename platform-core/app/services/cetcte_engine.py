"""
CET/CTE Engine — the real 9-stage participant journey, in-process.

Mirrors governance-engines/gis/src/services/cetcte.service.ts. Extends (does
not replace) SETHS's existing 3-state ENROLLED/COMPLETED/PLACED status —
that status still drives the closed-loop economic simulation exactly as
before (seths.py, gods-platform.ts, the smoke test). This engine adds the
institution-specific depth on top: the actual 9-stage CET/CTE journey,
cohort/stream assignment, the Self-Affirmation Contract, and certification
tier issuance — Document 00 Part III §7, §9, §11.

Known duality, documented rather than silently unified: this operates on
`Learner` (the operator-facing entity that drives the SETHS/TS/MADIBA closed
loop). The separate `Student` table (app/db/models.py) is the self-service
portal account used by portal_student.py / portal_employer.py. Both
represent a S.E.T.H.S. participant from a different angle; unifying them is
a larger refactor than this task's scope and is not attempted here — see
GIS_ECOSYSTEM_BUILD_NOTES.md.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.db.models import Learner, Certification, SkillsPassport
from app.services.audit_writer import append_audit

# Document 00 Part III §9 — the 9-stage CET/CTE Operating System.
STAGES = [
    "STABILISATION",      # Stage 0 — intake, assessment, Self-Affirmation Contract
    "CET_COMMUNICATE",     # Stage 01 — weeks 3-6
    "CET_EDUCATE",         # Stage 02 — weeks 7-18
    "CET_TRANSFER",        # Stage 03 — weeks 19-24
    "ASSESSMENT",          # Stage 04 — 30/60/90-day outcome verification
    "DEPLOYMENT",          # Stage 05 — months 6-12
    "EMPLOYMENT",          # Stage 06 — continuous
    "MENTORSHIP",          # Stage 07 — month 6 onward
    "PHASE_6",             # Stage 08 — the door never closes, perpetual
]

COHORTS = ("COHORT_1", "COHORT_2", "COHORT_3", "COHORT_4")
STREAMS = ("CONSTRUCTION", "DIGITAL_OPERATIONS", "AGRICULTURE", "COMMUNITY_HEALTH")

# Certification tiers unlock at these stage indices — Document 00 §11.1.
TIER_AT_STAGE = {
    1: ("BRONZE", "GBS Foundation Certificate"),
    3: ("SILVER", "GBS Employment-Ready Certificate"),
    4: ("GOLD", "GBS Verified Employment Certificate"),
    7: ("PLATINUM", "GBS Alumni Mentor Certification"),
}


def assign_cohort_stream(db: Session, learner_ref: str, cohort: str, stream: str) -> dict:
    if cohort not in COHORTS:
        raise ValueError(f"Unknown cohort: {cohort}. Must be one of {COHORTS}")
    if stream not in STREAMS:
        raise ValueError(f"Unknown stream: {stream}. Must be one of {STREAMS}")
    learner = db.query(Learner).filter(Learner.ref == learner_ref).one_or_none()
    if learner is None:
        raise LookupError(f"learner not found: {learner_ref}")
    learner.cohort = cohort
    learner.stream = stream
    db.commit()
    return {"ref": learner_ref, "cohort": cohort, "stream": stream}


def record_self_affirmation(db: Session, learner_ref: str, answers: dict) -> dict:
    """Document 00 §9 / Document 01 Annex D — the three-question intake
    commitment. Recorded, never used as leverage, revisited at milestones."""
    learner = db.query(Learner).filter(Learner.ref == learner_ref).one_or_none()
    if learner is None:
        raise LookupError(f"learner not found: {learner_ref}")
    import json
    payload = {
        "what_do_you_want_to_change": answers.get("what_do_you_want_to_change", ""),
        "why_now": answers.get("why_now", ""),
        "who_are_you_becoming": answers.get("who_are_you_becoming", ""),
        "witnessed_at": datetime.now(timezone.utc).isoformat(),
    }
    learner.self_affirmation_json = json.dumps(payload)
    db.commit()
    append_audit(db, event_type="SELF_AFFIRMATION_CONTRACT",
                 payload={"learner_ref": learner_ref}, classification="RESTRICTED",
                 actor_class="cetcte_engine")
    return {"ref": learner_ref, "recorded": True}


def advance_stage(db: Session, learner_ref: str) -> dict:
    """Moves the learner one CET/CTE stage forward. PHASE_6 (Stage 08) is
    terminal in the sense that it never closes — advancing from it is a
    no-op, consistent with Document 00 §9's 'the door never closes' design,
    not an error."""
    learner = db.query(Learner).filter(Learner.ref == learner_ref).one_or_none()
    if learner is None:
        raise LookupError(f"learner not found: {learner_ref}")

    current_idx = STAGES.index(learner.cetcte_stage) if learner.cetcte_stage in STAGES else 0
    new_idx = min(current_idx + 1, len(STAGES) - 1)
    learner.cetcte_stage = STAGES[new_idx]

    tier_issued = None
    if new_idx in TIER_AT_STAGE and new_idx != current_idx:
        tier, name = TIER_AT_STAGE[new_idx]
        already = db.query(Certification).filter(
            Certification.learner_pk == learner.id, Certification.tier == tier
        ).one_or_none()
        if already is None:
            cert = Certification(
                cert_ref=f"CERT-{uuid.uuid4().hex[:8].upper()}", learner_pk=learner.id,
                tier=tier, name=name, stream=learner.stream[:1] if learner.stream else "",
                verified=True,
            )
            db.add(cert)
            tier_issued = tier

    db.commit()
    append_audit(db, event_type="CETCTE_STAGE_ADVANCE",
                 payload={"learner_ref": learner_ref, "stage": learner.cetcte_stage, "tier_issued": tier_issued},
                 classification="INSTITUTIONAL", actor_class="cetcte_engine")

    return {"ref": learner_ref, "stage": learner.cetcte_stage,
            "stage_index": new_idx, "tier_issued": tier_issued,
            "phase_6_reached": new_idx == len(STAGES) - 1}


def update_ai_readiness(db: Session, learner_ref: str, stage: int) -> dict:
    """Document 00 §10 — the five-stage AI Workforce Adaptation Framework.
    Recorded on the Skills Passport, appended to history, never overwritten
    (Document 04 §6 — no credential is ever deleted)."""
    if not 1 <= stage <= 5:
        raise ValueError("AI readiness stage must be 1-5")
    learner = db.query(Learner).filter(Learner.ref == learner_ref).one_or_none()
    if learner is None:
        raise LookupError(f"learner not found: {learner_ref}")

    import json
    passport = db.query(SkillsPassport).filter(SkillsPassport.learner_pk == learner.id).one_or_none()
    stage_labels = {1: "AI Awareness", 2: "AI Augmentation", 3: "AI Collaboration",
                    4: "Career Evolution", 5: "Continuous Reinvention"}
    now_iso = datetime.now(timezone.utc).isoformat()
    if passport is None:
        passport = SkillsPassport(
            learner_pk=learner.id, ai_readiness_stage=stage,
            ai_readiness_json=json.dumps({"history": [{"stage": stage, "at": now_iso}]}),
            skills_json="[]", version=1,
        )
        db.add(passport)
    else:
        history = json.loads(passport.ai_readiness_json or '{"history": []}').get("history", [])
        history.append({"stage": stage, "at": now_iso})
        passport.ai_readiness_stage = stage
        passport.ai_readiness_json = json.dumps({"history": history})
        passport.version += 1
        passport.updated_at = datetime.now(timezone.utc)
    db.commit()
    return {"ref": learner_ref, "ai_readiness_stage": stage, "label": stage_labels[stage]}


def journey(db: Session, learner_ref: str) -> dict:
    """The read-only view a case manager or the participant's own portal
    would call — full journey state in one response."""
    learner = db.query(Learner).filter(Learner.ref == learner_ref).one_or_none()
    if learner is None:
        raise LookupError(f"learner not found: {learner_ref}")
    certs = db.query(Certification).filter(Certification.learner_pk == learner.id).all()
    passport = db.query(SkillsPassport).filter(SkillsPassport.learner_pk == learner.id).one_or_none()
    return {
        "ref": learner.ref, "status": learner.status, "cohort": learner.cohort,
        "stream": learner.stream, "cetcte_stage": learner.cetcte_stage,
        "stage_index": STAGES.index(learner.cetcte_stage) if learner.cetcte_stage in STAGES else 0,
        "total_stages": len(STAGES),
        "certifications": [{"tier": c.tier, "name": c.name, "verified": c.verified} for c in certs],
        "ai_readiness_stage": passport.ai_readiness_stage if passport else None,
        "has_self_affirmation": learner.self_affirmation_json not in ("{}", "", None),
    }
