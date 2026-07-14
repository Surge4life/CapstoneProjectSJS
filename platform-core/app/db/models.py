"""Domain models across all G.O.D.S divisions + UDOC governance/audit core."""
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ─── Identity / auth ───
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(40), default="viewer")  # admin|operator|auditor|client|gov|viewer
    division: Mapped[str] = mapped_column(String(40), default="GODS")  # GODS|SETHS|MADIBA|TS|UDOC
    profile: Mapped[str] = mapped_column(String(48), default="")  # Sovereign-Operator profile key (persona)
    tenant_id: Mapped[str] = mapped_column(String(60), default="", index=True)  # "" = platform staff
    tenant_pk: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── UDOC: AI model registry + decisions ───
class AIModel(Base):
    __tablename__ = "ai_models"
    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    operator_id: Mapped[str] = mapped_column(String(80))
    risk_tier: Mapped[str] = mapped_column(String(20), default="NOTABLE")  # MINIMAL..UNACCEPTABLE
    use_case: Mapped[str] = mapped_column(String(200), default="")
    jurisdiction: Mapped[str] = mapped_column(String(20), default="ZA")
    tenant_pk: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")  # ACTIVE|BLOCKED|SUSPENDED
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    decisions: Mapped[list["Decision"]] = relationship(back_populates="model")


class Decision(Base):
    __tablename__ = "decisions"
    id: Mapped[int] = mapped_column(primary_key=True)
    model_pk: Mapped[int] = mapped_column(ForeignKey("ai_models.id"))
    decision: Mapped[str] = mapped_column(String(20))  # APPROVE|REVIEW|RESTRICT|ESCALATE|BLOCK
    svs: Mapped[float] = mapped_column(Float, default=0.0)
    risk: Mapped[float] = mapped_column(Float, default=0.0)
    compliance: Mapped[float] = mapped_column(Float, default=0.0)
    sovereign: Mapped[bool] = mapped_column(Boolean, default=True)
    seal: Mapped[str] = mapped_column(String(128), default="")   # HMAC / Dilithium-ref
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    block_reasons: Mapped[str] = mapped_column(Text, default="")
    inputs_json: Mapped[str] = mapped_column(Text, default="{}")
    certificate_id: Mapped[str] = mapped_column(String(40), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    model: Mapped["AIModel"] = relationship(back_populates="decisions")


# ─── UDOC: immutable audit reference (hash-chain head stored here; full WORM in Cassandra) ───
class AuditRef(Base):
    __tablename__ = "audit_refs"
    id: Mapped[int] = mapped_column(primary_key=True)
    seq: Mapped[int] = mapped_column(Integer, index=True)
    event_type: Mapped[str] = mapped_column(String(40))
    event_hash: Mapped[str] = mapped_column(String(64))
    prev_hash: Mapped[str] = mapped_column(String(64))
    dilithium_ref: Mapped[str] = mapped_column(String(80), default="")
    classification: Mapped[str] = mapped_column(String(30), default="INTERNAL")
    actor_class: Mapped[str] = mapped_column(String(30), default="SYSTEM")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── SETHS: workforce reintegration ───
class Learner(Base):
    __tablename__ = "seths_learners"
    id: Mapped[int] = mapped_column(primary_key=True)
    ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    qualification: Mapped[str] = mapped_column(String(120), default="Digital Operations & AI Literacy")
    nqf_level: Mapped[int] = mapped_column(Integer, default=5)
    status: Mapped[str] = mapped_column(String(20), default="ENROLLED")  # ENROLLED|COMPLETED|PLACED
    monthly_value: Mapped[float] = mapped_column(Float, default=0.0)
    # --- CET/CTE + cohort fields added for GBS-SETHS alignment (Document 00 Part III §7.1, §9) ---
    # Additive only — existing `status` above is untouched and still drives the SETHS/TS/MADIBA
    # closed-loop simulation exactly as before. These fields add the institution-specific depth
    # (cohort, stream, CET/CTE stage) that "status" alone does not capture.
    cohort: Mapped[str] = mapped_column(String(4), default="COHORT_1")
    # COHORT_1 Reintegration | COHORT_2 AI Displacement | COHORT_3 Workforce Evolution | COHORT_4 Future Workforce
    stream: Mapped[str] = mapped_column(String(24), default="DIGITAL_OPERATIONS")
    # CONSTRUCTION | DIGITAL_OPERATIONS | AGRICULTURE | COMMUNITY_HEALTH — Document 00 vocational streams
    cetcte_stage: Mapped[str] = mapped_column(String(24), default="STABILISATION")
    self_affirmation_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── TS Industries: production SPVs ───
class TSProject(Base):
    __tablename__ = "ts_projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    spv_id: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    sector: Mapped[str] = mapped_column(String(30))  # legacy free-text field, kept for backward compatibility
    # --- corrected + extended for GBS-SETHS alignment (Document 00 Part I §1.2 note; T.S. Industries =
    # "The Technological Sector", 7 subsidiaries). The old sector comment listed 5 items including
    # "HOUSING", which is not one of the seven documented subsidiaries — corrected below, `sector` is
    # left untouched for any existing caller/data, `subsidiary` is the new, GBS-aligned, authoritative field.
    subsidiary: Mapped[str] = mapped_column(String(24), default="ENERGY")
    # ENERGY|CONSTRUCTION|AGRITECH|WATER|DIGITAL_INFRASTRUCTURE|MANUFACTURING|LOGISTICS
    equity_pct: Mapped[float] = mapped_column(Float, default=0.30)  # SPV co-ownership, 0.20-0.60 per M.A.D.I.B.A model
    name: Mapped[str] = mapped_column(String(160))
    workers_deployed: Mapped[int] = mapped_column(Integer, default=0)
    monthly_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    operating_margin: Mapped[float] = mapped_column(Float, default=0.0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class TSWorkerAssignment(Base):
    """Real FK link closing the SETHS→TS loop: a specific PLACED Learner
    assigned to a specific TSProject, rather than two independent counters.
    workers_deployed on TSProject remains as a fast aggregate; this table is
    the source of truth it is derived from."""
    __tablename__ = "ts_worker_assignments"
    id: Mapped[int] = mapped_column(primary_key=True)
    ts_project_pk: Mapped[int] = mapped_column(ForeignKey("ts_projects.id"), index=True)
    learner_pk: Mapped[int] = mapped_column(ForeignKey("seths_learners.id"), index=True)
    role: Mapped[str] = mapped_column(String(80), default="")
    monthly_wage: Mapped[float] = mapped_column(Float, default=0.0)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    ts_project: Mapped["TSProject"] = relationship()
    learner: Mapped["Learner"] = relationship()


# ─── MADIBA: capital allocations (the loop-closer) ───
class InstitutionalMilestone(Base):
    """Manually-recorded institutional milestones that have no natural
    transactional trace in this schema — e.g. a signed government Letter of
    Intent. Used by the M.A.D.I.B.A Series A trigger check (Document 00 §13;
    live-site-confirmed 4 conditions) alongside real DB-derived signals."""
    __tablename__ = "institutional_milestones"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    achieved: Mapped[bool] = mapped_column(Boolean, default=False)
    evidence_note: Mapped[str] = mapped_column(Text, default="")
    achieved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class CapitalCycle(Base):
    __tablename__ = "madiba_cycles"
    id: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(Integer, index=True)
    total_inflow: Mapped[float] = mapped_column(Float, default=0.0)
    dfi_servicing: Mapped[float] = mapped_column(Float, default=0.0)
    reserve: Mapped[float] = mapped_column(Float, default=0.0)
    holdings_opex: Mapped[float] = mapped_column(Float, default=0.0)
    recycled_to_seths: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── UDOC oversight: human-in-the-loop cases ───
class OversightCase(Base):
    __tablename__ = "oversight_cases"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    model_id: Mapped[str] = mapped_column(String(80))
    reason: Mapped[str] = mapped_column(String(200))
    state: Mapped[str] = mapped_column(String(20), default="OPEN")  # OPEN|REVIEWING|RESOLVED|OVERRIDDEN
    assigned_to: Mapped[str] = mapped_column(String(120), default="")
    resolution: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class OperatorAction(Base):
    """Structured, inspectable record of a Sovereign-Operator action: which profile did what, the
    operation type it resolved to, the artifact it produced/affected, and the outcome. Complements the
    immutable audit chain with a queryable operator-activity history."""
    __tablename__ = "operator_actions"
    id: Mapped[int] = mapped_column(primary_key=True)
    ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    actor_email: Mapped[str] = mapped_column(String(120), index=True)
    profile_key: Mapped[str] = mapped_column(String(60), index=True)
    capability: Mapped[str] = mapped_column(String(80))
    op_type: Mapped[str] = mapped_column(String(20))                 # CASE|REGISTRY|DIRECTIVE|EVALUATE|REPORT|RECORD
    target: Mapped[str] = mapped_column(String(120), default="")     # affected artifact id (case ref, model id, …)
    result_ref: Mapped[str] = mapped_column(String(60), default="")  # produced artifact id
    result_summary: Mapped[str] = mapped_column(Text, default="")
    detail_json: Mapped[str] = mapped_column(Text, default="{}")     # structured result (metrics, note, etc.)
    status: Mapped[str] = mapped_column(String(24), default="DONE")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── UDOC data-record-and-analytics: every division event is recorded here ───
class DivisionRecord(Base):
    """Immutable-ish event record UDOC keeps for each division — the analytics source."""
    __tablename__ = "division_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    division: Mapped[str] = mapped_column(String(20), index=True)   # SETHS|MADIBA|TS
    event_type: Mapped[str] = mapped_column(String(40), index=True)
    entity_ref: Mapped[str] = mapped_column(String(60), default="")
    metric_name: Mapped[str] = mapped_column(String(40), default="")
    metric_value: Mapped[float] = mapped_column(Float, default=0.0)
    period: Mapped[str] = mapped_column(String(16), default="", index=True)  # YYYY-MM bucket
    meta: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── PORTAL LAYER: students, employers, employees, applications, placements ───
class Student(Base):
    """SETHS student/learner portal account."""
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    student_ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    email: Mapped[str] = mapped_column(String(255), index=True)
    qualification: Mapped[str] = mapped_column(String(120), default="Digital Operations & AI Literacy")
    nqf_level: Mapped[int] = mapped_column(Integer, default=5)
    progress_pct: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(20), default="ENROLLED")  # ENROLLED|IN_PROGRESS|COMPLETED|PLACED
    portfolio_url: Mapped[str] = mapped_column(String(300), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Employer(Base):
    """Employer portal account — posts opportunities, reviews candidates."""
    __tablename__ = "employers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    org_name: Mapped[str] = mapped_column(String(200))
    sector: Mapped[str] = mapped_column(String(40), default="")
    contact_email: Mapped[str] = mapped_column(String(255), index=True)
    bbbee_level: Mapped[int] = mapped_column(Integer, default=4)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Opportunity(Base):
    """A job/placement opportunity posted by an employer."""
    __tablename__ = "opportunities"
    id: Mapped[int] = mapped_column(primary_key=True)
    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id"))
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text, default="")
    sector: Mapped[str] = mapped_column(String(40), default="")
    positions: Mapped[int] = mapped_column(Integer, default=1)
    monthly_stipend: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(20), default="OPEN")  # OPEN|FILLED|CLOSED
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Application(Base):
    """A student's application to an opportunity (the matching record)."""
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"))
    state: Mapped[str] = mapped_column(String(20), default="SUBMITTED")  # SUBMITTED|SHORTLISTED|OFFERED|PLACED|DECLINED
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Employee(Base):
    """Employee portal account — a placed worker inside a TS Industries SPV."""
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    employee_ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    email: Mapped[str] = mapped_column(String(255), index=True)
    division: Mapped[str] = mapped_column(String(20), default="TS")
    spv_id: Mapped[str] = mapped_column(String(60), default="")
    role: Mapped[str] = mapped_column(String(80), default="")
    monthly_salary: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")  # ACTIVE|ON_LEAVE|EXITED
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class TimesheetEntry(Base):
    """Employee timesheet/attendance — feeds payroll + TS productivity analytics."""
    __tablename__ = "timesheets"
    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    period: Mapped[str] = mapped_column(String(16), index=True)   # YYYY-MM
    hours: Mapped[float] = mapped_column(Float, default=0.0)
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── DOCUMENT STORE: uploads recorded through UDOC, fetchable from the records DB ───
class Document(Base):
    """A stored document (CV, qualification, project doc, report). Metadata here; bytes on disk/S3."""
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    doc_ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    division: Mapped[str] = mapped_column(String(20), index=True)   # SETHS|MADIBA|TS|UDOC
    owner_ref: Mapped[str] = mapped_column(String(60), index=True)  # student/employer/employee/client ref
    category: Mapped[str] = mapped_column(String(40), default="GENERAL")  # CV|QUALIFICATION|PROJECT|REPORT
    filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(100), default="application/octet-stream")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    sha256: Mapped[str] = mapped_column(String(64), default="")
    storage_path: Mapped[str] = mapped_column(String(400), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── UDOC SaaS CLIENTS: organisations governing their own AIs through UDOC ───
class SaaSClient(Base):
    """A SaaS client org that deploys AIs under UDOC governance (UDOC .apk users)."""
    __tablename__ = "saas_clients"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    org_name: Mapped[str] = mapped_column(String(200))
    contact_email: Mapped[str] = mapped_column(String(255), index=True)
    tier: Mapped[str] = mapped_column(String(20), default="STANDARD")  # STANDARD|SOVEREIGN|GOV
    api_key: Mapped[str] = mapped_column(String(80), default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── MADIBA: investor engagements + project updates (MADIBA .apk) ───
class InvestmentEngagement(Base):
    """A sovereign/institutional investor engagement tracked in MADIBA."""
    __tablename__ = "madiba_engagements"
    id: Mapped[int] = mapped_column(primary_key=True)
    engagement_ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    investor_name: Mapped[str] = mapped_column(String(200))
    investor_type: Mapped[str] = mapped_column(String(40), default="INSTITUTIONAL")  # SOVEREIGN|DFI|INSTITUTIONAL|PRIVATE
    instrument: Mapped[str] = mapped_column(String(60), default="")  # blended|debt|equity|guarantee
    indicated_amount: Mapped[float] = mapped_column(Float, default=0.0)
    stage: Mapped[str] = mapped_column(String(20), default="INTRODUCED")  # INTRODUCED|DD|TERM_SHEET|COMMITTED|FUNDED
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── TS: external project submissions + partner-build applications (TS .apk) ───
class ProjectSubmission(Base):
    """SPV/government/private project submitted to TS Industries for assessment/tracking."""
    __tablename__ = "ts_submissions"
    id: Mapped[int] = mapped_column(primary_key=True)
    submission_ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    submitter_name: Mapped[str] = mapped_column(String(200))
    submitter_type: Mapped[str] = mapped_column(String(30), default="PRIVATE")  # GOV|PRIVATE|SPV
    sector: Mapped[str] = mapped_column(String(40), default="")
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    capex_estimate: Mapped[float] = mapped_column(Float, default=0.0)
    stage: Mapped[str] = mapped_column(String(20), default="SUBMITTED")  # SUBMITTED|SCREENING|APPROVED|IN_BUILD|DECLINED
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class PartnerApplication(Base):
    """Application to become a partnered build assistant for TS projects."""
    __tablename__ = "ts_partner_apps"
    id: Mapped[int] = mapped_column(primary_key=True)
    app_ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    org_name: Mapped[str] = mapped_column(String(200))
    capability: Mapped[str] = mapped_column(String(200), default="")
    sector: Mapped[str] = mapped_column(String(40), default="")
    bbbee_level: Mapped[int] = mapped_column(Integer, default=4)
    state: Mapped[str] = mapped_column(String(20), default="APPLIED")  # APPLIED|VETTING|APPROVED|REJECTED
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── Policy-to-Code · UDOC governance protocol layer ───
class PolicyPack(Base):
    """A piece of passed/applicable legislation a client uploads, compiled into enforceable rules."""
    __tablename__ = "policy_packs"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    source_filename: Mapped[str] = mapped_column(String(255), default="")
    jurisdiction: Mapped[str] = mapped_column(String(40), default="ZA")
    sector: Mapped[str] = mapped_column(String(20), default="GENERAL")  # PUBLIC|PRIVATE|GENERAL
    tenant_pk: Mapped[int] = mapped_column(Integer, nullable=True, index=True)  # NULL = platform-wide
    status: Mapped[str] = mapped_column(String(20), default="DRAFT")    # DRAFT|ACTIVE|ARCHIVED
    uploaded_by: Mapped[str] = mapped_column(String(120), default="")
    sha256: Mapped[str] = mapped_column(String(64), default="")
    summary: Mapped[str] = mapped_column(Text, default="")
    rule_count: Mapped[int] = mapped_column(Integer, default=0)
    current_version: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    activated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class PolicyRule(Base):
    """A single machine-enforceable rule compiled from a PolicyPack (human-reviewable/editable)."""
    __tablename__ = "policy_rules"
    id: Mapped[int] = mapped_column(primary_key=True)
    pack_id: Mapped[int] = mapped_column(ForeignKey("policy_packs.id"), index=True)
    code: Mapped[str] = mapped_column(String(20), default="")  # PR-001
    kind: Mapped[str] = mapped_column(String(40))  # PROHIBIT|RISK_TIER_CAP|REQUIRE_HITL|MIN_SOVEREIGNTY|MIN_COMPLIANCE|MAX_DISPARATE_IMPACT|DATA_LOCALISATION|KEYWORD_FLAG
    target: Mapped[str] = mapped_column(Text, default="")
    operator: Mapped[str] = mapped_column(String(8), default="")  # <, >=, contains
    threshold: Mapped[float] = mapped_column(Float, nullable=True)
    severity: Mapped[str] = mapped_column(String(10), default="REVIEW")  # BLOCK|REVIEW|FLAG
    description: Mapped[str] = mapped_column(Text, default="")
    source_excerpt: Mapped[str] = mapped_column(Text, default="")
    confidence: Mapped[float] = mapped_column(Float, default=0.6)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── G.O.D.S Intelligence · internal self-contained knowledge + governance brain ───
class KnowledgeDoc(Base):
    """A document in the G.O.D.S Intelligence archive (the internal data room). Add/remove updates the corpus the system reasons over. INTERNAL ONLY — never client-exposed."""
    __tablename__ = "gi_knowledge_docs"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(240))
    source: Mapped[str] = mapped_column(String(255), default="")      # filename / drive path
    category: Mapped[str] = mapped_column(String(60), default="GENERAL")  # PATENT|SPEC|BRAND|MANDATE|FINANCIAL|LEGAL|MEMOIR|GENERAL
    division: Mapped[str] = mapped_column(String(40), default="GODS")
    sha256: Mapped[str] = mapped_column(String(64), default="")
    content_text: Mapped[str] = mapped_column(Text, default="")
    char_len: Mapped[int] = mapped_column(Integer, default=0)
    tags: Mapped[str] = mapped_column(String(300), default="")
    added_by: Mapped[str] = mapped_column(String(120), default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class IntelState(Base):
    """Singleton-ish state for the G.O.D.S Intelligence maturity + training position."""
    __tablename__ = "gi_state"
    id: Mapped[int] = mapped_column(primary_key=True)
    stage: Mapped[int] = mapped_column(Integer, default=1)  # 1 Automated/Assistive .. 5 Singularity-Governance
    corpus_docs: Mapped[int] = mapped_column(Integer, default=0)
    corpus_chars: Mapped[int] = mapped_column(Integer, default=0)
    last_trained_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    notes: Mapped[str] = mapped_column(Text, default="")


class EvaCertificate(Base):
    """Signed governance-evidence object issued on an EVA APPROVE outcome (white paper §4.3). WORM-style; verifiable via the UDOC seal."""
    __tablename__ = "eva_certificates"
    id: Mapped[int] = mapped_column(primary_key=True)
    certificate_id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    model_id: Mapped[str] = mapped_column(String(80), index=True)
    tenant_pk: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    decision: Mapped[str] = mapped_column(String(20))
    composite_eva: Mapped[float] = mapped_column(Float, default=0.0)
    dimensions_json: Mapped[str] = mapped_column(Text, default="{}")
    policy_pack: Mapped[str] = mapped_column(String(200), default="")
    seal: Mapped[str] = mapped_column(String(128), default="")
    content_sha3: Mapped[str] = mapped_column(String(64), default="")
    policy_version: Mapped[str] = mapped_column(String(120), default="")
    merkle_leaf: Mapped[str] = mapped_column(String(64), default="")
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    sector: Mapped[str] = mapped_column(String(20), default="GENERAL")          # PUBLIC|PRIVATE|GENERAL in force
    frameworks_cited: Mapped[str] = mapped_column(Text, default="[]")           # JSON list of sector framework names


# ─── SaaS multi-tenancy + commercial layer ───
class Tenant(Base):
    """A SaaS client organisation. Data of one tenant is isolated from every other tenant."""
    __tablename__ = "tenants"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(60), unique=True, index=True)  # slug
    name: Mapped[str] = mapped_column(String(200))
    sector: Mapped[str] = mapped_column(String(20), default="GENERAL")   # PUBLIC|PRIVATE|GENERAL
    tier: Mapped[str] = mapped_column(String(20), default="SANDBOX")     # SANDBOX..SOVEREIGN
    status: Mapped[str] = mapped_column(String(20), default="TRIAL")     # TRIAL|ACTIVE|SUSPENDED
    decision_quota: Mapped[int] = mapped_column(Integer, default=200)    # per period; -1 = unlimited
    usage_decisions: Mapped[int] = mapped_column(Integer, default=0)
    period_start: Mapped[datetime] = mapped_column(DateTime, default=_now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class ApiKey(Base):
    """Programmatic SaaS access for a tenant. The raw key is shown once; only its hash is stored."""
    __tablename__ = "api_keys"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_pk: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(120), default="default")
    prefix: Mapped[str] = mapped_column(String(12), index=True)
    key_hash: Mapped[str] = mapped_column(String(64), index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class PolicyVersion(Base):
    """An immutable, signed snapshot of a PolicyPack's enabled rules. COB-approved before it goes ACTIVE.
    Every rule change/activation produces a new version — a tamper-evident commit record."""
    __tablename__ = "policy_versions"
    id: Mapped[int] = mapped_column(primary_key=True)
    pack_id: Mapped[int] = mapped_column(ForeignKey("policy_packs.id"), index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    content_hash: Mapped[str] = mapped_column(String(64), default="")     # SHA-3-256 of the frozen rule set
    rules_json: Mapped[str] = mapped_column(Text, default="[]")
    rule_count: Mapped[int] = mapped_column(Integer, default=0)
    state: Mapped[str] = mapped_column(String(20), default="PROPOSED")    # PROPOSED|APPROVED|ACTIVE|VETOED|SUPERSEDED
    proposed_by: Mapped[str] = mapped_column(String(120), default="")
    reviewed_by: Mapped[str] = mapped_column(String(120), default="")     # COB officer
    review_note: Mapped[str] = mapped_column(Text, default="")
    signature: Mapped[str] = mapped_column(String(128), default="")       # sovereign HMAC seal (PQC/Dilithium-ref)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    decided_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class ClientKBDoc(Base):
    """A document in a SaaS CLIENT's PRIVATE knowledge base. Strictly isolated per tenant
    (tenant_pk) and never mixed with the internal G.O.D.S Intelligence corpus (gi_knowledge_docs).
    Clients upload/curate their own operational documents; their team queries them as an automated
    grounded reference, scoped only to their own tenant."""
    __tablename__ = "client_kb_docs"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_pk: Mapped[int] = mapped_column(Integer, index=True)          # isolation key -> tenants.id
    title: Mapped[str] = mapped_column(String(240))
    source: Mapped[str] = mapped_column(String(255), default="")
    category: Mapped[str] = mapped_column(String(60), default="GENERAL")
    sha256: Mapped[str] = mapped_column(String(64), default="")
    content_text: Mapped[str] = mapped_column(Text, default="")
    char_len: Mapped[int] = mapped_column(Integer, default=0)
    tags: Mapped[str] = mapped_column(String(300), default="")
    added_by: Mapped[str] = mapped_column(String(120), default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── UDOC: 24/7 continuous conformance scanner — scan runs + per-system findings ───

class ConformanceScan(Base):
    __tablename__ = "conformance_scans"
    id: Mapped[int] = mapped_column(primary_key=True)
    scan_ref: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    trigger: Mapped[str] = mapped_column(String(20), default="SCHEDULED")
    total: Mapped[int] = mapped_column(Integer, default=0)
    conformant: Mapped[int] = mapped_column(Integer, default=0)
    review: Mapped[int] = mapped_column(Integer, default=0)
    non_conformant: Mapped[int] = mapped_column(Integer, default=0)
    unverified: Mapped[int] = mapped_column(Integer, default=0)
    coverage_pct: Mapped[float] = mapped_column(Float, default=0.0)
    duration_ms: Mapped[float] = mapped_column(Float, default=0.0)
    audit_seq: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, index=True)


class ConformanceFinding(Base):
    __tablename__ = "conformance_findings"
    id: Mapped[int] = mapped_column(primary_key=True)
    scan_ref: Mapped[str] = mapped_column(String(40), index=True)
    model_id: Mapped[str] = mapped_column(String(80), index=True)
    name: Mapped[str] = mapped_column(String(160), default="")
    verdict: Mapped[str] = mapped_column(String(20))
    state: Mapped[str] = mapped_column(String(20))
    reason: Mapped[str] = mapped_column(String(240), default="")
    last_svs: Mapped[float] = mapped_column(Float, default=0.0)
    sovereign: Mapped[bool] = mapped_column(Boolean, default=True)
    block_rate: Mapped[float] = mapped_column(Float, default=0.0)
    recent_count: Mapped[int] = mapped_column(Integer, default=0)
    remediation: Mapped[str] = mapped_column(String(120), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, index=True)


# ═══════════════════════════════════════════════════════════════════════════
# G.O.D.S. Intelligence System (GIS) — added to align the live backend with
# GBS-SETHS v2.0 / the GBS-SETHS Institutional Readiness Package (Document 00
# §3, Document 04, Document 06). GIS supersedes EVA as the institutional AI
# backbone; its decisions are issued through this same audit-writer/AuditRef
# chain that EVA/UDOC already use (see app/services/gis_engine.py).
#
# Naming bridge (documented, not silently resolved): the GBS-SETHS documents
# and the standalone gods-intelligence-system reference package use
# "Participant". This backend's existing S.E.T.H.S. table is `Learner`
# (seths_learners). Rather than introduce a second, competing participant
# concept, GIS decisions and Skills Passports here reference `Learner.id`
# directly — "Participant" (institutional docs) == "Learner" (this schema).
# ═══════════════════════════════════════════════════════════════════════════

class GISDecision(Base):
    """A GIS decision: constitutional-pillar-gated, fail-closed by default.
    Mirrors governance-engines/gis/src/services/gis.service.ts's GISDecision
    record exactly (decision_type enum, pillar_checks, fail_closed) so the TS
    reference implementation and this live Python engine stay traceable to
    each other."""
    __tablename__ = "gis_decisions"
    id: Mapped[int] = mapped_column(primary_key=True)
    decision_ref: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    decision_type: Mapped[str] = mapped_column(String(40))
    # CAREER_NAVIGATION|CERTIFICATION_VERIFICATION|EMPLOYMENT_VERIFICATION|COMPLIANCE_CHECK|
    # GOVERNANCE_DECISION|OUTCOME_AUDIT|FRANCHISE_INTELLIGENCE|AI_ADAPTATION|RESEARCH_INSIGHT|MENTOR_MATCHING
    domain: Mapped[str] = mapped_column(String(40), default="SETHS")
    learner_pk: Mapped[int] = mapped_column(ForeignKey("seths_learners.id"), nullable=True, index=True)
    input_json: Mapped[str] = mapped_column(Text, default="{}")
    output_json: Mapped[str] = mapped_column(Text, default="{}")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    reasoning: Mapped[str] = mapped_column(Text, default="")
    pillar_checks_json: Mapped[str] = mapped_column(Text, default="[]")
    all_pillars_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    governance_gate: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    fail_closed: Mapped[bool] = mapped_column(Boolean, default=True)
    cob_reviewed: Mapped[bool] = mapped_column(Boolean, default=False)
    cob_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    audit_seq: Mapped[int] = mapped_column(Integer, default=0)  # links to AuditRef.seq
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, index=True)
    learner: Mapped["Learner"] = relationship()


class Certification(Base):
    """Bronze/Silver/Gold/Platinum/Specialist tiers per Document 00 §11.1."""
    __tablename__ = "gis_certifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    cert_ref: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    learner_pk: Mapped[int] = mapped_column(ForeignKey("seths_learners.id"), index=True)
    tier: Mapped[str] = mapped_column(String(20))  # BRONZE|SILVER|GOLD|PLATINUM|SPECIALIST
    name: Mapped[str] = mapped_column(String(160))
    stream: Mapped[str] = mapped_column(String(4), default="")  # A|B|C|D — Document 00 vocational streams
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    gis_decision_ref: Mapped[str] = mapped_column(String(60), default="")
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    learner: Mapped["Learner"] = relationship()


class SkillsPassport(Base):
    """One per Learner/Participant — Document 04, Skills Passport Technical Standard."""
    __tablename__ = "gis_skills_passports"
    id: Mapped[int] = mapped_column(primary_key=True)
    learner_pk: Mapped[int] = mapped_column(ForeignKey("seths_learners.id"), unique=True, index=True)
    ai_readiness_stage: Mapped[int] = mapped_column(Integer, default=1)  # 1-5, Document 00 §10
    ai_readiness_json: Mapped[str] = mapped_column(Text, default="{}")
    skills_json: Mapped[str] = mapped_column(Text, default="[]")
    version: Mapped[int] = mapped_column(Integer, default=1)
    verified_hash: Mapped[str] = mapped_column(String(64), default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    learner: Mapped["Learner"] = relationship()


class WorldPledge(Base):
    """The pledge register — d-24 World Pledge Document; pledge-before-capital strategy."""
    __tablename__ = "gis_world_pledges"
    id: Mapped[int] = mapped_column(primary_key=True)
    pledge_ref: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(80))
    last_name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(255), index=True)
    country: Mapped[str] = mapped_column(String(80), default="South Africa")
    role_interest: Mapped[str] = mapped_column(String(160), default="")
    message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, index=True)


class FranchiseNode(Base):
    """The five-layer GBS franchise architecture (Document 00 Part II §6;
    Document 03, Franchise Licensing Handbook) as real, queryable data —
    not just documentation. Layer 1 (GBS Global / G.O.D.S Holdings itself)
    is not a row here; it is the implicit root every node licenses from."""
    __tablename__ = "gbs_franchise_nodes"
    id: Mapped[int] = mapped_column(primary_key=True)
    node_ref: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    layer: Mapped[int] = mapped_column(Integer)  # 2 National | 3 Regional | 4 Delivery Operator | 5 Employer Ecosystem
    name: Mapped[str] = mapped_column(String(160))
    territory: Mapped[str] = mapped_column(String(120), default="South Africa")
    parent_node_ref: Mapped[str] = mapped_column(String(60), default="")  # "" == licensed directly from Layer 1
    licence_status: Mapped[str] = mapped_column(String(20), default="PENDING")
    # PENDING|ACTIVE|PROBATION|SUSPENDED|REVOKED — Document 03 §5
    compliance_score: Mapped[float] = mapped_column(Float, default=1.0)  # 0.0-1.0, Document 06 §4.3 risk scoring
    curriculum_fidelity_pct: Mapped[float] = mapped_column(Float, default=1.0)  # Document 00 §11.2, min 0.90
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, index=True)


class ComplianceViolation(Base):
    """Node/employer-level violations — Document 08, Risk & Failure Framework;
    Document 05 §6.3, the Absorption Commitment Clause."""
    __tablename__ = "gis_compliance_violations"
    id: Mapped[int] = mapped_column(primary_key=True)
    violation_ref: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    employer_id: Mapped[str] = mapped_column(String(80), default="")
    franchise_node_id: Mapped[str] = mapped_column(String(80), default="")
    violation_type: Mapped[str] = mapped_column(String(40))
    # OUTCOME_DATA_MANIPULATION|LEARNERSHIP_CREDIT_ABUSE|CONSTITUTIONAL_VIOLATION|
    # ABSORPTION_COMMITMENT_BREACH|GOVERNANCE_VIOLATION|ANTI_CORRUPTION_VIOLATION|
    # TRANSPARENCY_VIOLATION|HUMAN_DIGNITY_VIOLATION|AI_PRIMACY_VIOLATION
    description: Mapped[str] = mapped_column(Text, default="")
    severity: Mapped[str] = mapped_column(String(20), default="MEDIUM")  # LOW|MEDIUM|HIGH|CRITICAL
    status: Mapped[str] = mapped_column(String(24), default="REPORTED")
    # REPORTED|UNDER_INVESTIGATION|CONFIRMED|REMEDIATED|RESOLVED|APPEALED
    gis_decision_ref: Mapped[str] = mapped_column(String(60), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, index=True)
