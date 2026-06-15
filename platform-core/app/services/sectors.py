"""
Sector experiences — genuine Public vs Private differentiation for UDOC tenants.

A tenant's `sector` (PUBLIC | PRIVATE | GENERAL) drives a materially different governance experience:
the regulatory frameworks that apply, the oversight model, the dashboard emphasis, and the terminology.
Grounded in real South African instruments (current as of mid-2026):
  - National AI Policy Framework (Aug 2024) — high-level principles, constitutional alignment.
    (The April 2026 Draft National AI Policy was withdrawn; the 2024 Framework remains the standing instrument.)
  - Constitution of the RSA — s9 equality, s14 privacy, s33 just administrative action.
  - PAJA (Promotion of Administrative Justice Act 3 of 2000) — lawful, reasonable, procedurally fair admin action + reasons.
  - POPIA (Protection of Personal Information Act 4 of 2013) — s71 automated decision-making safeguards; responsible-party duties.
  - PAIA (access to information); National Data and Cloud Policy (2024) — data residency / sovereignty.
  - Consumer Protection Act 68 of 2008 (CPA); sector regulators (FSCA/FAIS, NCA) for private deployments.
This is the applicable governance scope per sector — not a cosmetic toggle.
"""

SECTORS = {
    "PUBLIC": {
        "key": "PUBLIC",
        "label": "Public Sector",
        "audience": "citizens",
        "accent": "#00C2D4",
        "tagline": "Constitutional, accountable AI for public administration",
        "summary": "AI decisions by an organ of state that affect citizens must be lawful, reasonable and procedurally fair, with reasons on request and meaningful human oversight. Data stays sovereign.",
        "oversight_model": "Mandatory human-in-the-loop for citizen-affecting decisions; public accountability; right to reasons and review.",
        "terminology": {"subject": "citizen", "subjects": "citizens", "org": "department / public entity",
                        "compliance": "constitutional & administrative compliance", "risk": "rights & accountability risk"},
        "frameworks": [
            {"id": "ai-framework-2024", "name": "National AI Policy Framework (2024)", "basis": "DCDT Framework, Aug 2024",
             "focus": "Responsible, ethical AI; constitutional alignment; transformation. Six core pillars.", "applies_to": "all state AI"},
            {"id": "constitution-s33", "name": "Just Administrative Action (s33)", "basis": "Constitution of the RSA",
             "focus": "Lawful, reasonable and procedurally fair administrative action.", "applies_to": "citizen-affecting decisions"},
            {"id": "constitution-s9", "name": "Equality (s9)", "basis": "Constitution of the RSA",
             "focus": "No unfair discrimination — fairness across protected groups.", "applies_to": "all decisions"},
            {"id": "paja", "name": "PAJA — Administrative Justice", "basis": "Act 3 of 2000",
             "focus": "Procedural fairness; written reasons on request; right of review.", "applies_to": "administrative decisions"},
            {"id": "popia-s71-pub", "name": "POPIA s71 — Automated Decisions", "basis": "Act 4 of 2013",
             "focus": "No decision based solely on automated processing with legal/significant effect, without safeguards.", "applies_to": "automated decisions"},
            {"id": "data-cloud-2024", "name": "Data & Cloud Policy — Sovereignty", "basis": "National Data and Cloud Policy, 2024",
             "focus": "Data residency and sovereign control of state data and AI infrastructure.", "applies_to": "data & hosting"},
            {"id": "paia", "name": "PAIA — Access to Information", "basis": "Act 2 of 2000",
             "focus": "Transparency and access to records of decisions.", "applies_to": "transparency"},
        ],
        "kpi_focus": ["citizen_decisions", "oversight_open", "rights_block_rate", "review_rate", "sovereignty"],
    },
    "PRIVATE": {
        "key": "PRIVATE",
        "label": "Private Sector",
        "audience": "customers",
        "accent": "#C9A84C",
        "tagline": "Responsible, defensible AI for commercial deployment",
        "summary": "AI decisions affecting customers, applicants or employees must meet POPIA's responsible-party duties, treat people fairly, and manage regulatory and commercial exposure — with evidence you can defend.",
        "oversight_model": "Risk-based human review; fairness/bias controls; defensible audit trail for regulators and customers.",
        "terminology": {"subject": "customer", "subjects": "customers", "org": "organisation",
                        "compliance": "commercial & data-protection compliance", "risk": "regulatory & commercial risk"},
        "frameworks": [
            {"id": "popia-rp", "name": "POPIA — Responsible Party", "basis": "Act 4 of 2013",
             "focus": "Lawful processing, purpose specification, minimality, security safeguards, data-subject rights.", "applies_to": "all personal data"},
            {"id": "popia-s71-priv", "name": "POPIA s71 — Automated Decisions", "basis": "Act 4 of 2013",
             "focus": "Safeguards where a decision with legal/significant effect is based solely on automated processing.", "applies_to": "automated decisions"},
            {"id": "ai-framework-2024-priv", "name": "National AI Policy Framework (2024)", "basis": "DCDT Framework, Aug 2024",
             "focus": "Responsible innovation, transparency and accountability principles for industry.", "applies_to": "commercial AI"},
            {"id": "cpa", "name": "Consumer Protection Act", "basis": "Act 68 of 2008",
             "focus": "Fair, just and reasonable treatment of consumers; no unfair discrimination in supply.", "applies_to": "consumer-facing decisions"},
            {"id": "fairness-bias", "name": "Algorithmic Fairness & Bias", "basis": "POPIA s9 + EE Act principles",
             "focus": "Disparate-impact testing across protected groups; documented mitigation.", "applies_to": "scoring & ranking"},
            {"id": "sector-reg", "name": "Sector Regulators (where applicable)", "basis": "FSCA/FAIS, NCA, etc.",
             "focus": "Financial-services suitability, responsible lending and conduct standards.", "applies_to": "regulated industries"},
        ],
        "kpi_focus": ["customer_decisions", "bias_flags", "regulatory_exposure", "block_rate", "commercial_risk"],
    },
    "GENERAL": {
        "key": "GENERAL",
        "label": "General",
        "audience": "stakeholders",
        "accent": "#8A9BB0",
        "tagline": "Baseline AI governance",
        "summary": "Baseline governance scope. Assign a Public or Private sector to tailor frameworks, oversight and dashboards.",
        "oversight_model": "Standard human-in-the-loop on blocked decisions.",
        "terminology": {"subject": "subject", "subjects": "subjects", "org": "organisation",
                        "compliance": "compliance", "risk": "risk"},
        "frameworks": [
            {"id": "ai-framework-2024-gen", "name": "National AI Policy Framework (2024)", "basis": "DCDT Framework, Aug 2024",
             "focus": "Responsible, ethical AI principles.", "applies_to": "all AI"},
            {"id": "popia-gen", "name": "POPIA", "basis": "Act 4 of 2013",
             "focus": "Personal-information protection and automated-decision safeguards.", "applies_to": "personal data"},
        ],
        "kpi_focus": ["decisions", "blocked", "oversight_open", "block_rate"],
    },
}


def get(sector_key: str) -> dict:
    return SECTORS.get((sector_key or "GENERAL").upper(), SECTORS["GENERAL"])
