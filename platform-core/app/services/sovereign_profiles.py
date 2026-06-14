"""
Sovereign-Operator Profiles — the 24 canonical operator personas of the G.O.D.S / UDOC ecosystem,
grouped GOVERNANCE · OPERATIONS · PEOPLE · BUSINESS. Sourced from the UDOC 24-portal master.

Each profile is grounded to a base enforcement role + division so the server-authoritative access
layer (access_control.systems_for / may_open) still governs what a holder may actually open — the
profile is the institutional persona; the base_role/division is what the backend enforces. Each
profile carries its capability set (the operational actions it is authorised to perform).
"""
from typing import Dict, List, Tuple
from app.services.access_control import systems_for

# key: (title, group, base_role, division, [capabilities])
_P = [
    # ── GOVERNANCE (5) ──
    ("SUPER_ADMIN", "Super Administrator", "GOVERNANCE", "admin", "GODS",
     ["System Override", "Deploy Global Policy", "Audit All Portals", "Emergency Lockdown"]),
    ("REGULATOR", "Regulator", "GOVERNANCE", "gov", "UDOC",
     ["Issue Directive", "Start Audit", "Review Submission", "Impose Penalty"]),
    ("INFO_REGULATOR", "Information Regulator", "GOVERNANCE", "gov", "UDOC",
     ["Open Investigation", "Issue PAIA Notice", "Assess Breach", "Close Case"]),
    ("DCDT_POLICY", "DCDT Policy", "GOVERNANCE", "gov", "UDOC",
     ["Publish Policy", "Schedule Review", "Impact Assessment", "Stakeholder Consult"]),
    ("CONSTITUTIONAL_OVERSIGHT", "Constitutional Oversight (COB)", "GOVERNANCE", "gov", "UDOC",
     ["Constitutional Review", "Issue Opinion", "Refer to Court", "Close Matter"]),
    # ── OPERATIONS (8) ──
    ("BORDER", "Border Control", "OPERATIONS", "operator", "GODS",
     ["Flag Traveler", "Release Hold", "Update Watchlist", "Generate Report"]),
    ("DHA", "Home Affairs (DHA)", "OPERATIONS", "operator", "GODS",
     ["Verify Identity", "Issue Document", "Biometric Capture", "Expedite"]),
    ("SARS", "Revenue Service (SARS)", "OPERATIONS", "operator", "GODS",
     ["Initiate Audit", "Verify Return", "Issue Assessment", "Close Case"]),
    ("SERVICE_DELIVERY", "Service Delivery", "OPERATIONS", "operator", "GODS",
     ["Assign Ticket", "Escalate", "Resolve", "Close Feedback"]),
    ("MUNICIPAL", "Municipal", "OPERATIONS", "operator", "GODS",
     ["Approve Budget", "Log Outage", "Update Project", "Dispatch Team"]),
    ("JUSTICE", "Justice", "OPERATIONS", "operator", "GODS",
     ["Schedule Hearing", "File Judgment", "Issue Warrant", "Archive Case"]),
    ("NPA", "National Prosecuting Authority", "OPERATIONS", "operator", "GODS",
     ["Authorize Prosecution", "Request Evidence", "File Charges", "Withdraw Case"]),
    ("HEALTH", "Health", "OPERATIONS", "operator", "GODS",
     ["Triage Patient", "Issue Alert", "Update Records", "Dispatch Ambulance"]),
    # ── PEOPLE (7) ──
    ("SETHS", "S.E.T.H.S Skills", "PEOPLE", "operator", "SETHS",
     ["Enroll Learner", "Approve Funding", "Verify Placement", "Certify"]),
    ("CASE_MANAGER", "Case Manager", "PEOPLE", "operator", "SETHS",
     ["Open Case", "Assign Worker", "Update Status", "Close Case"]),
    ("EMPLOYER", "Employer", "PEOPLE", "client", "UDOC",
     ["File UIF", "Verify Employee", "Submit PAYE", "Resolve Dispute"]),
    ("SAHRC", "Human Rights Commission", "PEOPLE", "gov", "UDOC",
     ["Log Complaint", "Start Investigation", "Schedule Hearing", "Publish Finding"]),
    ("HITL_REVIEW", "HITL Review", "PEOPLE", "operator", "UDOC",
     ["Approve AI Decision", "Override", "Flag for Training", "Release"]),
    ("CITIZEN", "Citizen", "PEOPLE", "viewer", "GODS",
     ["Apply for Service", "Check Status", "Upload Document", "Book Appointment"]),
    ("WELFARE", "Welfare", "PEOPLE", "operator", "MADIBA",
     ["Approve Grant", "Verify Beneficiary", "Investigate Fraud", "Disburse"]),
    # ── BUSINESS (4) ──
    ("AI_OWNER", "AI System Owner", "BUSINESS", "client", "UDOC",
     ["Deploy Model", "Retrain", "Monitor Drift", "Rollback"]),
    ("PRIVATE_COMPLIANCE", "Private Compliance", "BUSINESS", "client", "UDOC",
     ["Run Compliance Check", "Issue Certificate", "Flag Non-Compliant", "Update Registry"]),
    ("INSURANCE", "Insurance", "BUSINESS", "client", "UDOC",
     ["Process Claim", "Verify Policy", "Flag Fraud", "Approve Payout"]),
    ("MADIBA", "M.A.D.I.B.A Capital", "BUSINESS", "operator", "MADIBA",
     ["Launch Project", "Allocate Funds", "Field Report", "Impact Assessment"]),
]

GROUPS = ["GOVERNANCE", "OPERATIONS", "PEOPLE", "BUSINESS"]
PROFILES: Dict[str, dict] = {
    key: {"key": key, "title": title, "group": group, "base_role": role,
          "division": div, "capabilities": caps}
    for (key, title, group, role, div, caps) in _P
}


def catalog() -> List[dict]:
    """All 24 profiles, each annotated with the systems its base_role/division may actually open."""
    out = []
    for p in PROFILES.values():
        syss = [s["key"] for s in systems_for(p["base_role"], p["division"])]
        out.append({**p, "systems": syss})
    return out


def resolve(profile_key: str) -> Tuple[str, str]:
    """Map a profile -> (base_role, division) for enforcement. Returns ('', '') if unknown."""
    p = PROFILES.get((profile_key or "").upper())
    return (p["base_role"], p["division"]) if p else ("", "")


def by_group() -> Dict[str, List[dict]]:
    g = {grp: [] for grp in GROUPS}
    for p in catalog():
        g.setdefault(p["group"], []).append(p)
    return g


def matrix() -> dict:
    """Profile × capability matrix data + the role→systems grid for the base roles in play."""
    roles = sorted({p["base_role"] for p in PROFILES.values()})
    role_systems = {r: [s["key"] for s in systems_for(r, "GODS")] for r in roles}
    return {"groups": GROUPS, "count": len(PROFILES), "profiles": catalog(),
            "role_systems": role_systems,
            "note": "A profile is the institutional persona; its base_role + division is what the server enforces."}
