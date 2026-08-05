"""
GBS Engine — the constitutional pillar registry and franchise node governance,
as real, queryable, DB-backed logic rather than only prose in the docx/pdf
package. Operationalises Document 00 Part I §2, Part II §5-6, Document 03
(Franchise Licensing Handbook), and GBS-UDOC Constitutional Proposition v1.0.
"""
from __future__ import annotations
import uuid
from sqlalchemy.orm import Session

from app.db.models import FranchiseNode
from app.services.audit_writer import append_audit

# Document 00 Part I §2 / Document 01 Part Three — live data, byte-identical to Document 01.
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

OUTCOME_UNDERPERFORMANCE_THRESHOLD = 0.20
MIN_CURRICULUM_FIDELITY = 0.90


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


def record_compliance_audit(db: Session, node_ref: str, compliance_score: float,
                            curriculum_fidelity_pct: float) -> dict:
    node = db.query(FranchiseNode).filter(FranchiseNode.node_ref == node_ref).one_or_none()
    if node is None:
        raise LookupError(f"node not found: {node_ref}")
    node.compliance_score = float(compliance_score)
    node.curriculum_fidelity_pct = float(curriculum_fidelity_pct)
    if curriculum_fidelity_pct < MIN_CURRICULUM_FIDELITY * 100 and node.licence_status == "ACTIVE":
        node.licence_status = "PROBATION"
    db.commit()
    append_audit(db, event_type="FRANCHISE_COMPLIANCE_AUDIT",
                 payload={"node_ref": node_ref, "compliance_score": compliance_score,
                          "curriculum_fidelity_pct": curriculum_fidelity_pct,
                          "licence_status": node.licence_status},
                 classification="INSTITUTIONAL", actor_class="gbs_engine")
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


# Four-divisional GBS — GBS-UDOC Constitutional Proposition v1.0 (July 2026)
FOUR_DIVISIONAL_ARCHITECTURE = {
    "doctrine": "GBS-Global (Layer 1) — constitutional standard licensed to every division",
    "source": "GBS-UDOC Constitutional Proposition v1.0 · July 2026 · completes set with GBS-SETHS, GBS-T.S., GBS-M.A.D.I.B.A./EIF",
    "symmetry": {
        "develops": ["SETHS", "TS"],
        "recognises": ["MADIBA_EIF", "UDOC"],
        "note": "SETHS develops human capability; TS develops trusted systems; MADIBA/EIF recognises exceptional individuals; UDOC recognises exceptional systems platforms",
    },
    "divisions": [
        {"division": "SETHS", "proposition": "GBS-SETHS", "assures": "Human capability", "mode": "develops"},
        {"division": "MADIBA", "proposition": "GBS-M.A.D.I.B.A. / EIF", "assures": "Exceptional individual contribution", "mode": "recognises"},
        {"division": "TS", "proposition": "GBS-T.S.", "assures": "Trusted systems", "mode": "develops"},
        {"division": "UDOC", "proposition": "GBS-UDOC", "assures": "Exceptional systems platforms", "mode": "recognises"},
    ],
}

SOVEREIGN_VERIFIED_TIER = {
    "name": "Sovereign-Verified",
    "status": "designed_not_built",
    "parallel_to": "EIF Diamond (individuals)",
    "baseline_exceeded": "GBS-T.S. standard compliance",
    "verification_authority": "UDOC via EVA six dimensions + sealed audit trail (StayChain)",
    "confers": [
        "Formal certification logged to sealed audit trail",
        "Priority standing across UDOC six commercial licensing tiers",
        "Eligibility as reference implementation for GBS-T.S. builds",
        "Credibility input into MADIBA capital position for T.S.-built systems",
    ],
    "proposed_process": [
        "Maintain GBS-T.S. compliance ≥ proposed 6 months continuous EVA (founder-confirm pending)",
        "UDOC certification function reviews sustained EVA history across 6 dimensions",
        "Independent evidence — not builder self-report",
        "Log certification + evidence to sealed audit trail",
        "Annual COB review (same cadence as EIF Diamond)",
    ],
    "safeguards": [
        {"safeguard": "Certification separated from commercial/sales within UDOC", "pillar": "V · Governance First"},
        {"safeguard": "Every Sovereign-Verified decision + EVA history on sealed audit trail", "pillar": "VI · Transparency"},
        {"safeguard": "No officer certifies system where they hold undisclosed interest", "pillar": "XI · Anti-Corruption"},
        {"safeguard": "Sustained performance data required — not single snapshot", "pillar": "XII · Evidence-Driven"},
        {"safeguard": "COB annual review once constituted", "pillar": "Document 01 Part Five"},
    ],
    "honesty": {
        "proven_live": "EVA 6-D evaluation + UDOC sealed audit trail (partially live Capstone path)",
        "designed_not_built": "Sovereign-Verified tier name, 6-month baseline, certification staffing — proposed in GBS-UDOC v1.0",
        "aspirational": "Externally recognised standard comparable to ISO — requires commercial UDOC scale",
    },
}

DIVISION_BINDINGS = [
    {
        "division": "SETHS",
        "proposition": "GBS-SETHS",
        "mode": "develops",
        "role": "Workforce reintegration + CET/CTE — develops human capability",
        "assures": "Human capability",
        "constitutional": ["I", "II", "IX", "XII"],
        "universal": [1, 2, 3, 4],
        "live_apis": ["/seths/enrol", "/seths/{ref}/advance", "/seths/metrics", "/gis/participants/{ref}/journey"],
        "honesty": "Learners + placement loop live; Skills Passport claims verified via UDOC infrastructure (not GBS-UDOC exceptional tier)",
    },
    {
        "division": "MADIBA",
        "proposition": "GBS-M.A.D.I.B.A. / EIF",
        "mode": "recognises",
        "role": "Capital cycle + EIF Diamond — recognises exceptional individual contribution",
        "assures": "Exceptional individual contribution (Six Domains)",
        "constitutional": ["IV", "V", "VI", "XI"],
        "universal": [4, 6, 7],
        "live_apis": ["/madiba/allocate", "/madiba/engage", "/madiba/series-a-status", "/eif/nominate", "/eif/framework"],
        "honesty": "Demo ledger only — not institutional AUM; EIF nominate → sealed audit; capital not_deployed on free tier",
    },
    {
        "division": "TS",
        "proposition": "GBS-T.S.",
        "mode": "develops",
        "role": "Industrial SPVs + employment absorption — develops trusted systems",
        "assures": "Trusted systems (baseline compliance plane)",
        "constitutional": ["II", "IV", "IX"],
        "universal": [3, 4, 5],
        "live_apis": ["/ts/projects", "/ts/projects/{spv}/assign-worker", "/ts/submit/project"],
        "honesty": "SPV + assign-worker live; GBS-T.S. compliance is the baseline that GBS-UDOC exceptional certification exceeds",
    },
    {
        "division": "UDOC",
        "proposition": "GBS-UDOC",
        "mode": "recognises",
        "role": "Constitutional governance plane + Sovereign-Verified recognition of exceptional systems platforms",
        "assures": "Exceptional systems platforms (beyond GBS-T.S. baseline)",
        "constitutional": ["V", "VI", "VIII", "XII"],
        "universal": [5, 7],
        "live_apis": ["/decisions", "/decisions/batch", "/policy/runtime-matrix", "/Sentinel", "/udoc/demo/ready", "/gis/gbs/overview"],
        "honesty": "EVA + policy-to-code live on Capstone path; Sovereign-Verified tier is designed_not_built per GBS-UDOC v1.0",
        "sovereign_tier": "Sovereign-Verified",
    },
    {
        "division": "EIF",
        "proposition": "GBS-M.A.D.I.B.A. / EIF (recognition instrument)",
        "mode": "recognises",
        "role": "Exceptional Individual Fund under MADIBA — individual-side parallel to GBS-UDOC Sovereign-Verified",
        "assures": "Exceptional individual contribution",
        "constitutional": ["I", "II", "VI", "XI"],
        "universal": [1, 4, 7],
        "live_apis": ["/eif/framework", "/eif/nominate", "/eif/tiers", "/eif/domains"],
        "honesty": "Framework + nominate audit-only; Diamond parallel to systems Sovereign-Verified (UDOC)",
        "systems_parallel": "GBS-UDOC Sovereign-Verified",
    },
]


def overview(db: Session) -> dict:
    """Honest GBS snapshot aligned to four-divisional architecture + GBS-UDOC v1.0."""
    nodes = list_nodes(db)
    by_layer = {str(k): 0 for k in LAYERS}
    by_status = {}
    for n in nodes:
        by_layer[str(n["layer"])] = by_layer.get(str(n["layer"]), 0) + 1
        st = n.get("licence_status") or "UNKNOWN"
        by_status[st] = by_status.get(st, 0) + 1
    return {
        "surface": "gis/gbs",
        "gbs_udoc_version": "1.0",
        "honesty": {
            "nodes_empty_ok": len(nodes) == 0,
            "note": "Zero franchise nodes is honest Capstone state — pillars + APIs live; geographic franchise scale post-seed",
            "sovereign_verified": SOVEREIGN_VERIFIED_TIER["status"],
            "four_division_set": "complete — GBS-SETHS, GBS-T.S., GBS-M.A.D.I.B.A./EIF, GBS-UDOC",
        },
        "architecture": FOUR_DIVISIONAL_ARCHITECTURE,
        "sovereign_verified_tier": SOVEREIGN_VERIFIED_TIER,
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


def architecture() -> dict:
    return FOUR_DIVISIONAL_ARCHITECTURE


def sovereign_tier() -> dict:
    return SOVEREIGN_VERIFIED_TIER
