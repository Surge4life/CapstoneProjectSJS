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

# ── what each portal IS and DOES (served via /access/profiles + /portal/{key}) ──
DESC = {
 "SUPER_ADMIN": "Root governance authority over the entire G.O.D.S / UDOC estate: deploy global policy, audit every portal, and trigger emergency lockdown across all sovereign systems.",
 "REGULATOR": "The UDOC sector regulator. Issues binding directives to AI-system operators, opens audits, reviews submissions, and imposes penalties for non-compliance.",
 "INFO_REGULATOR": "South Africa's Information Regulator function under POPIA/PAIA: opens investigations, issues PAIA notices, assesses data breaches, and closes cases.",
 "DCDT_POLICY": "Department of Communications & Digital Technologies policy desk: publishes national AI/digital policy, schedules reviews, runs impact assessments, and consults stakeholders.",
 "CONSTITUTIONAL_OVERSIGHT": "The Constitutional Oversight Board (COB). Tests AI decisions and policy against the Bill of Rights, issues opinions, refers matters to court, and closes constitutional reviews.",
 "BORDER": "Border-control operations. Flags travellers against watchlists, releases holds, updates the watchlist, and generates port-of-entry reports.",
 "DHA": "Home Affairs identity operations. Verifies identity, issues documents, captures biometrics, and expedites priority cases.",
 "SARS": "Revenue-service operations. Initiates audits, verifies returns, issues assessments, and closes revenue cases.",
 "SERVICE_DELIVERY": "Citizen service-delivery desk. Assigns tickets, escalates, resolves issues, and closes feedback loops.",
 "MUNICIPAL": "Municipal operations. Approves budgets, logs service outages, updates capital projects, and dispatches field teams.",
 "JUSTICE": "Court administration. Schedules hearings, files judgments, issues warrants, and archives cases.",
 "NPA": "National Prosecuting Authority. Authorises prosecutions, requests evidence, files charges, and withdraws cases.",
 "HEALTH": "Health operations. Triages patients, issues public-health alerts, updates records, and dispatches ambulances.",
 "SETHS": "S.E.T.H.S skills & workforce reintegration. Enrols learners, approves funding, verifies placements, and certifies completions.",
 "CASE_MANAGER": "Social case management. Opens cases, assigns caseworkers, updates status, and closes resolved cases.",
 "EMPLOYER": "Employer compliance desk. Files UIF, verifies employees, submits PAYE, and resolves labour disputes.",
 "SAHRC": "South African Human Rights Commission. Logs complaints, opens investigations, schedules hearings, and publishes findings.",
 "HITL_REVIEW": "Human-in-the-loop review. Approves or overrides AI decisions, flags cases for retraining, and releases holds.",
 "CITIZEN": "Citizen self-service. Applies for services, checks status, uploads documents, and books appointments.",
 "WELFARE": "Welfare administration. Approves grants, verifies beneficiaries, investigates fraud, and disburses payments.",
 "AI_OWNER": "AI-system owner console. Deploys models, retrains, monitors drift, and rolls back to a safe version.",
 "PRIVATE_COMPLIANCE": "Private-sector compliance. Runs compliance checks, issues certificates, flags non-compliance, and updates the registry.",
 "INSURANCE": "Insurance operations. Processes claims, verifies policies, flags fraud, and approves payouts.",
 "MADIBA": "M.A.D.I.B.A Capital impact desk. Launches projects, allocates funds, files field reports, and runs impact assessments.",
}

# concise action description per control (what the control does when operated)
CONTROL_DESC = {
 "System Override":"Force a state change across systems, bypassing normal gates.","Deploy Global Policy":"Publish a policy pack to every connected portal.","Audit All Portals":"Run a cross-portal compliance sweep.","Emergency Lockdown":"Freeze all sovereign systems immediately.",
 "Issue Directive":"Serve a binding instruction on an operator.","Start Audit":"Open a formal audit of a system or operator.","Review Submission":"Assess a submitted compliance package.","Impose Penalty":"Record a sanction for non-compliance.",
 "Open Investigation":"Begin a formal investigation and assign a reference.","Issue PAIA Notice":"Serve an access-to-information notice.","Assess Breach":"Evaluate a reported data breach.","Close Case":"Close out and archive the case.",
 "Publish Policy":"Release a policy document to the registry.","Schedule Review":"Diarise a future policy/impact review.","Impact Assessment":"Run a structured impact assessment.","Stakeholder Consult":"Open a stakeholder consultation round.",
 "Constitutional Review":"Test a decision/policy against the Bill of Rights.","Issue Opinion":"Publish a constitutional opinion.","Refer to Court":"Escalate the matter to a court.","Close Matter":"Conclude and archive the matter.",
 "Flag Traveler":"Place a traveller on review against the watchlist.","Release Hold":"Lift a hold and allow passage/processing.","Update Watchlist":"Add or amend a watchlist entry.","Generate Report":"Produce an operational report.",
 "Verify Identity":"Confirm an identity against the register.","Issue Document":"Issue an official document.","Biometric Capture":"Record a biometric enrolment.","Expedite":"Fast-track a priority case.",
 "Initiate Audit":"Open a revenue audit.","Verify Return":"Validate a submitted return.","Issue Assessment":"Raise a tax assessment.",
 "Assign Ticket":"Route a service ticket to an owner.","Escalate":"Raise the case to a higher tier.","Resolve":"Mark the issue resolved.","Close Feedback":"Close the feedback loop with the citizen.",
 "Approve Budget":"Authorise a budget line.","Log Outage":"Record a service outage.","Update Project":"Update capital-project status.","Dispatch Team":"Send a field team to site.",
 "Schedule Hearing":"Set a hearing date.","File Judgment":"Record a judgment.","Issue Warrant":"Issue a warrant.","Archive Case":"Archive a closed case.",
 "Authorize Prosecution":"Authorise a prosecution to proceed.","Request Evidence":"Request evidence from a source.","File Charges":"Lodge formal charges.","Withdraw Case":"Withdraw a case from the roll.",
 "Triage Patient":"Assign a clinical priority.","Issue Alert":"Broadcast a public-health alert.","Update Records":"Update a patient/health record.","Dispatch Ambulance":"Dispatch emergency transport.",
 "Enroll Learner":"Enrol a learner on a programme.","Approve Funding":"Approve programme funding.","Verify Placement":"Confirm a workplace placement.","Certify":"Issue a completion certificate.",
 "Open Case":"Open a social-services case.","Assign Worker":"Assign a caseworker.","Update Status":"Update the case status.",
 "File UIF":"File a UIF declaration.","Verify Employee":"Verify an employee record.","Submit PAYE":"Submit a PAYE return.","Resolve Dispute":"Resolve a labour dispute.",
 "Log Complaint":"Record a rights complaint.","Start Investigation":"Open an investigation.","Publish Finding":"Publish an investigation finding.",
 "Approve AI Decision":"Confirm an AI decision after review.","Override":"Override the AI's decision.","Flag for Training":"Send the case to the training set.","Release":"Release the held subject/decision.",
 "Apply for Service":"Submit a service application.","Check Status":"Check application status.","Upload Document":"Upload a supporting document.","Book Appointment":"Book a service appointment.",
 "Approve Grant":"Approve a welfare grant.","Verify Beneficiary":"Verify a beneficiary.","Investigate Fraud":"Open a fraud investigation.","Disburse":"Release a payment.",
 "Deploy Model":"Deploy an AI model to production.","Retrain":"Trigger a retraining run.","Monitor Drift":"Check live drift metrics.","Rollback":"Roll back to a safe model version.",
 "Run Compliance Check":"Run a compliance evaluation.","Issue Certificate":"Issue a compliance certificate.","Flag Non-Compliant":"Mark a subject non-compliant.","Update Registry":"Update the compliance registry.",
 "Process Claim":"Process an insurance claim.","Verify Policy":"Verify policy coverage.","Flag Fraud":"Flag a suspicious claim.","Approve Payout":"Approve a claim payout.",
 "Launch Project":"Launch an impact project.","Allocate Funds":"Allocate capital to a project.","Field Report":"File a field report.",
}

# which op_type bucket a control records under (for the queryable activity log)
def op_type_for(control: str) -> str:
    c = (control or "").lower()
    if any(k in c for k in ("case","matter","complaint","investigat","prosecut","charge","hearing","warrant","judgment")): return "CASE"
    if any(k in c for k in ("model","registry","deploy","retrain","drift","rollback","watchlist","record","document")): return "REGISTRY"
    if any(k in c for k in ("directive","policy","opinion","alert","penalty","lockdown","override")): return "DIRECTIVE"
    if any(k in c for k in ("audit","review","verify","assess","check","triage","compliance")): return "EVALUATE"
    if any(k in c for k in ("report","certificate","finding","assessment","payslip","return")): return "REPORT"
    return "RECORD"


def catalog() -> List[dict]:
    """All 24 profiles, annotated with description, per-control detail, and the systems the base_role/division may open."""
    out = []
    for p in PROFILES.values():
        syss = [s["key"] for s in systems_for(p["base_role"], p["division"])]
        controls = [{"name": c, "desc": CONTROL_DESC.get(c, ""), "op_type": op_type_for(c)} for c in p["capabilities"]]
        out.append({**p, "desc": DESC.get(p["key"], ""), "controls": controls, "systems": syss})
    return out


def get(profile_key: str) -> dict | None:
    """One enriched profile by key, or None."""
    k = (profile_key or "").upper()
    for p in catalog():
        if p["key"] == k:
            return p
    return None


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
