"""
EIF — Exceptional Individual Fund (M.A.D.I.B.A. companion)
UDOC assurance surface for GBS-MADIBA EIF Framework v1.0.

Honesty: philosophy is founder-sourced; nomination/funding mechanics are designed
not yet operational at scale. Capstone path logs nominations to sealed audit only —
no real capital deployment on free-tier Neon.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import current_user
from app.services.audit_writer import append_audit

router = APIRouter(prefix="/eif", tags=["EIF · MADIBA Diamond / UDOC assurance"])

_DOMAINS = [
    {"id": "intellectual", "label": "Intellectual Contribution",
     "examples": "Ideas, research, knowledge, frameworks, patents, teaching, open-source"},
    {"id": "physical", "label": "Physical Contribution",
     "examples": "Construction, engineering, manufacturing, infrastructure, agriculture, healthcare"},
    {"id": "creative", "label": "Creative Contribution",
     "examples": "Art, music, writing, design, film, culture, entertainment"},
    {"id": "community", "label": "Community Contribution",
     "examples": "Mentoring, volunteering, family care, conflict resolution, community leadership"},
    {"id": "economic", "label": "Economic Contribution",
     "examples": "Employment creation, business formation, investment, innovation"},
    {"id": "environmental", "label": "Environmental Contribution",
     "examples": "Conservation, renewables, waste reduction, biodiversity, sustainable farming"},
]

_TIERS = [
    {"tier": "Bronze", "recognises": "Phases 1–2 core transferable and digital-literacy skills"},
    {"tier": "Silver", "recognises": "Employer-readiness assessment passed"},
    {"tier": "Gold", "recognises": "90-day verified employment outcome"},
    {"tier": "Platinum", "recognises": "Alumni peer-mentor pathway — S.E.T.H.S. ceiling"},
    {"tier": "Specialist", "recognises": "Stream-specific trade certification (parallel track)"},
    {"tier": "Diamond", "recognises": "EIF status — exceptional contribution, independently verified"},
]

_SAFEGUARDS = [
    {"safeguard": "Nomination separated from funding decisions", "pillar": "V · Governance First"},
    {"safeguard": "Diamond decisions logged to UDOC sealed audit", "pillar": "VI · Transparency"},
    {"safeguard": "No undisclosed relationship nominations", "pillar": "XI · Anti-Corruption"},
    {"safeguard": "COB annual review of Diamond decisions", "pillar": "V · Oversight"},
    {"safeguard": "Independent evidence, not self-report alone", "pillar": "XII · Evidence-Driven"},
]


@router.get("/framework")
def framework():
    """GBS-MADIBA EIF instrument summary for Capstone / operator surfaces."""
    return {
        "instrument": "EIF · Exceptional Individual Fund",
        "division": "M.A.D.I.B.A.",
        "version": "1.0 · July 2026",
        "udoc_role": "Assurance · audit trail · evidence-driven verification — not capital deployment",
        "philosophy": {
            "connects": "G.O.D.S. should connect us for what matters, not what divides us.",
            "funds": "Exceptional contribution (not merely exceptional people)",
            "poverty": "Incapacity of means to survive (clean water, healthy food, safe shelter)",
        },
        "domains": _DOMAINS,
        "passport_tiers": _TIERS,
        "safeguards": _SAFEGUARDS,
        "honesty": {
            "proven": "Contribution philosophy, Six Domains, poverty/access distinction (founder-sourced)",
            "designed": "Diamond tier, two-pathway nomination, review process — not founder-confirmed final mechanics",
            "aspirational": "Real EIF funding at scale depends on M.A.D.I.B.A. capital formation (not started)",
        },
        "pathways_proposed": [
            "S.E.T.H.S. Platinum alumnus → verified exceptional contribution",
            "Open nomination/application via M.A.D.I.B.A. regardless of S.E.T.H.S. pipeline",
        ],
    }


@router.get("/domains")
def domains():
    return {"domains": _DOMAINS, "count": len(_DOMAINS)}


@router.get("/tiers")
def tiers():
    return {"tiers": _TIERS, "diamond_ceiling": True}


class NominateReq(BaseModel):
    nominee_label: str = Field(..., min_length=2, max_length=120)
    domain: str = Field(..., description="One of six domain ids")
    contribution_summary: str = Field(..., min_length=10, max_length=2000)
    evidence_note: str = Field("", max_length=1000)
    pathway: str = Field("open", description="seths_platinum | open")


@router.post("/nominate")
def nominate(body: NominateReq, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    """Capstone nomination log — audit only. No funding, no Diamond grant on free tier."""
    domain_ids = {d["id"] for d in _DOMAINS}
    if body.domain not in domain_ids:
        raise HTTPException(400, f"domain must be one of {sorted(domain_ids)}")
    role = user.get("role") or ""
    if role not in ("admin", "operator", "gov"):
        raise HTTPException(403, "EIF nomination log is staff-facing on Capstone host")
    payload = {
        "nominee_label": body.nominee_label[:120],
        "domain": body.domain,
        "pathway": body.pathway,
        "contribution_summary": body.contribution_summary[:500],
        "evidence_note": (body.evidence_note or "")[:300],
        "status": "LOGGED_PENDING_REVIEW",
        "funding": False,
        "note": "Designed process only — not operational Diamond grant",
    }
    try:
        append_audit(db, "EIF_NOMINATION", payload, classification="GOVERNANCE",
                     actor_class=role or "SYSTEM")
    except Exception as e:
        raise HTTPException(500, f"audit write failed: {e}")
    return {
        "ok": True,
        "logged": True,
        "status": "LOGGED_PENDING_REVIEW",
        "domain": body.domain,
        "nominee_label": body.nominee_label,
        "udoc": "Sealed audit event EIF_NOMINATION — Pillar VI Transparency",
        "honesty": "No capital deployed; review function not staffed on free-tier Capstone host",
    }


@router.get("/health")
def eif_health():
    return {
        "surface": "eif",
        "status": "live",
        "assurance": "UDOC audit + framework read",
        "capital": "not_deployed",
    }
