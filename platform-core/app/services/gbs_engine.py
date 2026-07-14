"""
GBS Engine — the constitutional pillar registry and franchise node governance,
as real, queryable, DB-backed logic rather than only prose in the docx/pdf
package. Operationalises Document 00 Part I §2, Part II §5-6, and Document 03
(Franchise Licensing Handbook) directly.
"""
from __future__ import annotations
import uuid
from sqlalchemy.orm import Session

from app.db.models import FranchiseNode
from app.services.audit_writer import append_audit

# Document 00 Part I §2 / Document 01 Part Three — reproduced here as live data,
# not re-typed from the docx. Keep this list byte-identical to Document 01 if either changes.
CONSTITUTIONAL_PILLARS = [
    {"numeral": "I", "name": "Human Dignity"},
    {"numeral": "II", "name": "Contribution First"},
    {"numeral": "III", "name": "Sovereign Respect"},
    {"numeral": "IV", "name": "Ethical Profitability"},
    {"numeral": "V", "name": "Governance First"},
    {"numeral": "VI", "name": "Transparency"},
    {"numeral": "VII", "name": "Founder Constraint"},
    {"numeral": "VIII", "name": "Human Primacy in AI"},
    {"numeral": "IX", "name": "Reintegration"},
    {"numeral": "X", "name": "Long-Horizon Discipline"},
    {"numeral": "XI", "name": "Anti-Corruption"},
    {"numeral": "XII", "name": "Evidence-Driven"},
]

# Document 00 Part II §5 — the Seven GBS Universal Pillars.
GBS_UNIVERSAL_PILLARS = [
    {"number": 1, "name": "Human Value"},
    {"number": 2, "name": "Continuous Education"},
    {"number": 3, "name": "Capability Transfer"},
    {"number": 4, "name": "Economic Participation"},
    {"number": 5, "name": "Technological Adaptation"},
    {"number": 6, "name": "Sustainability"},
    {"number": 7, "name": "Generational Continuity"},
]

LAYERS = {2: "National GBS", 3: "Regional GBS", 4: "Delivery Operator", 5: "Employer Ecosystem"}

# Document 03 §5 — Franchise Governance sanctions ladder.
OUTCOME_UNDERPERFORMANCE_THRESHOLD = 0.20      # >20% below benchmark, two consecutive cohorts
MIN_CURRICULUM_FIDELITY = 0.90                  # Document 00 §11.2


def register_node(db: Session, layer: int, name: str, territory: str, parent_node_ref: str = "") -> dict:
    if layer not in LAYERS:
        raise ValueError(f"layer must be one of {list(LAYERS)} (Layer 1 is GBS Global itself, not a node)")
    node = FranchiseNode(
        node_ref=f"GBS-{LAYERS[layer].split()[0].upper()}-{uuid.uuid4().hex[:6].upper()}",
        layer=layer, name=name, territory=territory, parent_node_ref=parent_node_ref,
        licence_status="PENDING",
    )
    db.add(node)
    db.commit()
    db.refresh(node)
    append_audit(db, event_type="FRANCHISE_NODE_REGISTERED",
                 payload={"node_ref": node.node_ref, "layer": layer, "name": name},
                 classification="INSTITUTIONAL", actor_class="gbs_engine")
    return _node_dict(node)


def set_licence_status(db: Session, node_ref: str, status: str, reason: str = "") -> dict:
    valid = {"PENDING", "ACTIVE", "PROBATION", "SUSPENDED", "REVOKED"}
    if status not in valid:
        raise ValueError(f"status must be one of {valid}")
    node = db.query(FranchiseNode).filter(FranchiseNode.node_ref == node_ref).one_or_none()
    if node is None:
        raise LookupError(f"node not found: {node_ref}")
    node.licence_status = status
    db.commit()
    append_audit(db, event_type="FRANCHISE_LICENCE_STATUS_CHANGE",
                 payload={"node_ref": node_ref, "status": status, "reason": reason},
                 classification="INSTITUTIONAL", actor_class="gbs_engine")
    return _node_dict(node)


def record_compliance_audit(db: Session, node_ref: str, compliance_score: float, curriculum_fidelity_pct: float) -> dict:
    """Document 00 §6.1 — Annual Compliance Audit. Applies the sanctions
    ladder mechanically where the thresholds are crossed; a human/COB
    decision is still required for revocation (this flags, it does not
    revoke on its own — Pillar VIII, human primacy)."""
    node = db.query(FranchiseNode).filter(FranchiseNode.node_ref == node_ref).one_or_none()
    if node is None:
        raise LookupError(f"node not found: {node_ref}")
    node.compliance_score = compliance_score
    node.curriculum_fidelity_pct = curriculum_fidelity_pct

    flag = None
    if curriculum_fidelity_pct < MIN_CURRICULUM_FIDELITY:
        flag = "CURRICULUM_FIDELITY_BELOW_MINIMUM"
    if compliance_score < (1 - OUTCOME_UNDERPERFORMANCE_THRESHOLD):
        flag = "OUTCOME_UNDERPERFORMANCE"
        if node.licence_status == "ACTIVE":
            node.licence_status = "PROBATION"

    db.commit()
    append_audit(db, event_type="FRANCHISE_COMPLIANCE_AUDIT",
                 payload={"node_ref": node_ref, "compliance_score": compliance_score,
                          "curriculum_fidelity_pct": curriculum_fidelity_pct, "flag": flag},
                 classification="INSTITUTIONAL", actor_class="gbs_engine")
    return {**_node_dict(node), "flag": flag}


def list_nodes(db: Session, layer: int | None = None) -> list[dict]:
    q = db.query(FranchiseNode)
    if layer is not None:
        q = q.filter(FranchiseNode.layer == layer)
    return [_node_dict(n) for n in q.order_by(FranchiseNode.layer, FranchiseNode.id).all()]


def _node_dict(n: FranchiseNode) -> dict:
    return {
        "node_ref": n.node_ref, "layer": n.layer, "layer_name": LAYERS.get(n.layer, "?"),
        "name": n.name, "territory": n.territory, "parent_node_ref": n.parent_node_ref,
        "licence_status": n.licence_status, "compliance_score": n.compliance_score,
        "curriculum_fidelity_pct": n.curriculum_fidelity_pct,
    }
