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
    qualification: Mapped[str] = mapped_column(String(120), default="Software Developer 118707")
    nqf_level: Mapped[int] = mapped_column(Integer, default=5)
    status: Mapped[str] = mapped_column(String(20), default="ENROLLED")  # ENROLLED|COMPLETED|PLACED
    monthly_value: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── TS Industries: production SPVs ───
class TSProject(Base):
    __tablename__ = "ts_projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    spv_id: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    sector: Mapped[str] = mapped_column(String(30))  # ENERGY|HOUSING|AGRITECH|WATER|LOGISTICS
    name: Mapped[str] = mapped_column(String(160))
    workers_deployed: Mapped[int] = mapped_column(Integer, default=0)
    monthly_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    operating_margin: Mapped[float] = mapped_column(Float, default=0.0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


# ─── MADIBA: capital allocations (the loop-closer) ───
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
    qualification: Mapped[str] = mapped_column(String(120), default="Software Developer 118707")
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
