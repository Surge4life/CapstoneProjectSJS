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
        licence_status="PROVISIONAL",
    )
    db.add(node); db.commit(); db.refresh(node)
    append_audit(db, event_type="GBS_NODE_REGISTER", actor_email="system", entity_ref=node.node_ref,
                 detail=f"layer={layer} territory={territory}")
    return _node_dict(node)


def set_licence_status(db: Session, node_ref: str, status: str, reason: str = "") -> dict:
    node = db.query(FranchiseNode).filter(FranchiseNode.node_ref == node_ref).one_or_none()
    if not node:
        raise LookupError(f"node not found: {node_ref}")
    node.licence_status = status
    db.commit(); db.refresh(node)
    append_audit(db, event_type="GBS_NODE_STATUS", actor_email="system", entity_ref=node_ref,
                 detail=f"status={status} reason={reason[:120]}")
    return _node_dict(node)


def record_compliance_audit(db: Session, node_ref: str, compliance_score: float,
                            curriculum_fidelity_pct: float) -> dict:
    node = db.query(FranchiseNode).filter(FranchiseNode.node_ref == node_ref).one_or_none()
    if not node:
        raise LookupError(f"node not found: {node_ref}")
    node.compliance_score = compliance_score
    node.curriculum_fidelity_pct = curriculum_fidelity_pct
    db.commit(); db.refresh(node)
    append_audit(db, event_type="GBS_NODE_AUDIT", actor_email="system", entity_ref=node_ref,
                 detail=f"compliance={compliance_score} fidelity={curriculum_fidelity_pct}")
    return _node_dict(node)


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


# Division ↔ pillar binding for Capstone honesty (UDOC GBS doc will refine).
DIVISION_BINDINGS = [
    {
        "division": "SETHS",
        "role": "Workforce reintegration + CET/CTE journey",
        "constitutional": ["I", "II", "IX", "XII"],
        "universal": [1, 2, 3, 4],
        "live_apis": ["/seths/enrol", "/seths/{ref}/advance", "/seths/metrics", "/gis/participants/{ref}/journey"],
        "honesty": "Learners + placement loop live; franchise curriculum fidelity not yet node-audited at scale",
    },
    {
        "division": "MADIBA",
        "role": "Capital cycle + EIF Diamond assurance (UDOC-backed)",
        "constitutional": ["IV", "V", "VI", "XI"],
        "universal": [4, 6, 7],
        "live_apis": ["/madiba/allocate", "/madiba/engage", "/madiba/series-a-status", "/eif/nominate"],
        "honesty": "Demo ledger only — not institutional AUM; EIF nominates to sealed audit, capital not_deployed",
    },
    {
        "division": "TS",
        "role": "Industrial SPVs + employment absorption",
        "constitutional": ["II", "IV", "IX"],
        "universal": [3, 4, 5],
        "live_apis": ["/ts/projects", "/ts/projects/{spv}/assign-worker", "/ts/submit/project"],
        "honesty": "SPV + assign-worker live; large project pipeline empty until funded deployments",
    },
    {
        "division": "UDOC",
        "role": "Constitutional governance plane for AI systems (EVA + policy-to-code)",
        "constitutional": ["V", "VI", "VIII", "XII"],
        "universal": [5, 7],
        "live_apis": ["/decisions", "/decisions/batch", "/policy/runtime-matrix", "/Sentinel", "/udoc/demo/ready"],
        "honesty": "Capstone production path on Render/Neon; hardware enforcement documented, not claimed on free tier",
    },
    {
        "division": "EIF",
        "role": "Exceptional Individual Fund under MADIBA + UDOC assurance",
        "constitutional": ["I", "II", "VI", "XI"],
        "universal": [1, 4, 7],
        "live_apis": ["/eif/framework", "/eif/nominate", "/eif/tiers", "/eif/domains"],
        "honesty": "Framework + nominate audit-only; no real capital on free-tier Neon",
    },
]


def overview(db: Session) -> dict:
    """Honest GBS snapshot for Capstone / pre-UDOC-GBS freeze."""
    nodes = list_nodes(db)
    by_layer = {str(k): 0 for k in LAYERS}
    by_status = {}
    for n in nodes:
        by_layer[str(n["layer"])] = by_layer.get(str(n["layer"]), 0) + 1
        st = n.get("licence_status") or "UNKNOWN"
        by_status[st] = by_status.get(st, 0) + 1
    return {
        "surface": "gis/gbs",
        "honesty": {
            "nodes_empty_ok": len(nodes) == 0,
            "note": "Zero franchise nodes is honest Capstone state — pillars + APIs live; geographic franchise scale post-seed",
            "awaiting": "UDOC GBS document (founder pack) for freeze alignment",
        },
        "constitutional_pillars": CONSTITUTIONAL_PILLARS,
        "gbs_universal_pillars": GBS_UNIVERSAL_PILLARS,
        "layers": [{"layer": k, "name": v} for k, v in LAYERS.items()],
        "thresholds": {
            "outcome_underperformance": OUTCOME_UNDERPERFORMANCE_THRESHOLD,
            "min_curriculum_fidelity": MIN_CURRICULUM_FIDELITY,
        },
        "nodes": {
            "total": len(nodes),
            "by_layer": by_layer,
            "by_licence_status": by_status,
            "sample": nodes[:8],
        },
        "division_bindings": DIVISION_BINDINGS,
    }
