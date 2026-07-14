"""
GIS Engine — the G.O.D.S. Intelligence System's decision core, in-process.

Mirrors governance-engines/gis/src/services/gis.service.ts exactly (same 12
constitutional pillar checks, same fail-closed default, same decision types)
so the TS package remains the canonical reference and this stays the live,
in-process implementation platform-core actually runs — the same pattern
already established by governance_bridge.py for EVA/UDOC.

Per Document 00 §3 (GBS-SETHS Consolidated Super Framework) and Document 06
(GIS Architecture Specification): GIS issues decisions via UDOC's audit
infrastructure; it does not run a parallel, undocumented decision path.
Every GIS decision here is written through the same audit_writer used by
UDOC/EVA, and recorded in gis_decisions for direct query.

Human primacy (Pillar VIII): nothing in this module can complete an action
on a participant's behalf. It returns a decision and reasoning; a human case
manager (or, for programmatic flows, an explicit caller) acts on it. GIS
never overrides FAIL_CLOSED — an unresolvable case always surfaces to a
human, it never silently proceeds.
"""
from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional
from sqlalchemy.orm import Session

from app.db.models import GISDecision, Learner
from app.services.audit_writer import append_audit

DECISION_TYPES = (
    "CAREER_NAVIGATION", "CERTIFICATION_VERIFICATION", "EMPLOYMENT_VERIFICATION",
    "COMPLIANCE_CHECK", "GOVERNANCE_DECISION", "OUTCOME_AUDIT",
    "FRANCHISE_INTELLIGENCE", "AI_ADAPTATION", "RESEARCH_INSIGHT", "MENTOR_MATCHING",
)

# The Twelve G.O.D.S. Constitutional Pillars — Document 00 Part I §2 / Document 01 Part Three.
# Each pillar maps to one boolean flag GIS expects on the decision input. This is a direct,
# faithful port of PILLAR_CHECKS in governance-engines/gis/src/config/constants.ts.
PILLAR_CHECKS = [
    ("I", "Human Dignity", "respects_human_dignity"),
    ("II", "Contribution First", "affirms_contribution_potential"),
    ("III", "Sovereign Respect", "politically_neutral"),
    ("IV", "Ethical Profitability", "ethically_sound"),
    ("V", "Governance First", "has_governance_review"),
    ("VI", "Transparency", "has_transparent_record"),
    ("VII", "Founder Constraint", "respects_founder_limits"),
    ("VIII", "Human Primacy in AI", "has_human_oversight"),
    ("IX", "Reintegration", "supports_reintegration_cohort"),
    ("X", "Long-Horizon Discipline", "considers_long_term_impact"),
    ("XI", "Anti-Corruption", "no_corruption_risk"),
    ("XII", "Evidence-Driven", "is_evidence_based"),
]


@dataclass
class GISInput:
    decision_type: str
    learner_ref: Optional[str] = None
    domain: str = "SETHS"
    context: dict = field(default_factory=dict)
    pillar_flags: dict = field(default_factory=dict)
    requested_by: str = "system"


def _check_pillars(pillar_flags: dict) -> tuple[list[dict], bool]:
    """Fail-closed by construction: a flag that is missing is treated as False,
    never assumed True. This is the same rule stated in Document 00 §3 and
    Document 06 §3 — absence of proof is not proof of compliance."""
    results = []
    all_passed = True
    for numeral, name, flag_key in PILLAR_CHECKS:
        passed = bool(pillar_flags.get(flag_key, False))
        if not passed:
            all_passed = False
        results.append({"pillar": numeral, "name": name, "flag": flag_key, "passed": passed})
    return results, all_passed


def make_decision(db: Session, gis_input: GISInput) -> dict:
    """The single entry point every GIS-facing router calls. Fail-closed: if
    pillar checks cannot be verified, the decision BLOCKs and escalates for
    human review rather than defaulting to allow."""
    t0 = time.time()
    if gis_input.decision_type not in DECISION_TYPES:
        raise ValueError(f"Unknown GIS decision_type: {gis_input.decision_type}")

    pillar_results, all_passed = _check_pillars(gis_input.pillar_flags)

    learner = None
    if gis_input.learner_ref:
        learner = db.query(Learner).filter(Learner.ref == gis_input.learner_ref).one_or_none()

    fail_closed = True  # constitutional default; never set False by this function itself
    blocked = not all_passed
    governance_gate = all_passed and not blocked

    decision_ref = f"GIS-{uuid.uuid4().hex[:10].upper()}"
    reasoning = (
        "All twelve constitutional pillar checks passed; decision proceeds."
        if all_passed else
        "One or more constitutional pillar checks failed or were unverified — "
        "GIS defaults to BLOCK per Pillar VIII (Human Primacy in AI) and the "
        "fail-closed architecture. Escalate to a human case manager or the COB."
    )

    row = GISDecision(
        decision_ref=decision_ref,
        decision_type=gis_input.decision_type,
        domain=gis_input.domain,
        learner_pk=learner.id if learner else None,
        input_json=_safe_json(gis_input.context),
        output_json=_safe_json({"pillar_results": pillar_results}),
        confidence=1.0 if all_passed else 0.0,
        reasoning=reasoning,
        pillar_checks_json=_safe_json(pillar_results),
        all_pillars_passed=all_passed,
        governance_gate=governance_gate,
        blocked=blocked,
        fail_closed=fail_closed,
        cob_reviewed=False,
        cob_approved=False,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    audit_ref = append_audit(
        db, event_type="GIS_DECISION",
        payload={
            "decision_ref": decision_ref, "decision_type": gis_input.decision_type,
            "domain": gis_input.domain, "learner_ref": gis_input.learner_ref,
            "all_pillars_passed": all_passed, "blocked": blocked,
            "requested_by": gis_input.requested_by,
        },
        classification="INSTITUTIONAL", actor_class="gis_engine",
    )
    row.audit_seq = audit_ref.seq if audit_ref is not None else 0
    db.commit()

    latency_ms = round((time.time() - t0) * 1000, 2)
    return {
        "decision_ref": decision_ref,
        "decision_type": gis_input.decision_type,
        "blocked": blocked,
        "governance_gate": governance_gate,
        "fail_closed": fail_closed,
        "all_pillars_passed": all_passed,
        "pillar_results": pillar_results,
        "reasoning": reasoning,
        "audit_seq": row.audit_seq,
        "latency_ms": latency_ms,
    }


def _safe_json(obj) -> str:
    import json
    try:
        return json.dumps(obj, default=str)
    except Exception:
        return "{}"
