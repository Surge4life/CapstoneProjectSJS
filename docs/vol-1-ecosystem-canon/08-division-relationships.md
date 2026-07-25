# Chapter 08 — Division Relationships

## How the Four Divisions Relate to the G.O.D.S Core

The G.O.D.S ecosystem comprises four divisions, each serving a distinct domain. All four divisions share the same governance infrastructure. None of them is more or less governed than the others.

---

## The Hub and Spoke Model

```
                    G.O.D.S Core
                    (platform-core)
                    Governance | Auth | RBAC
                    Audit | Intelligence | Analytics
                         /    |    |    \
                        /     |    |     \
                    UDOC   SETHS  TS    MADIBA
                  Control        Ind.  / EIF
```

The G.O.D.S Core is the hub. The four divisions are the spokes. Data flows from each division into the core for governance processing. Governance decisions flow back to each division. The divisions do not communicate directly with each other — all cross-division data flows go through the core.

---

## Division 1: SETHS — Skills, Employment, Training, and Human Services

**What it does:** SETHS is the workforce governance division. It manages:
- Learner enrolment and progress tracking
- Employer registration and opportunity posting
- Application management and matching
- Document upload, SHA-256 sealing, and UDOC recording
- Reintegration support (CETCTE engine)
- Certification and qualification recording

**Who uses it:** Learners, employers, employment practitioners, training providers, government workforce agencies.

**Relationship to G.O.D.S Core:**
- Every employment decision (shortlisting, rejection, offer) passes through the GBS Runtime
- Every document upload is recorded in the UDOC audit chain
- Learner data is governed under POPIA privacy rules enforced by the sovereignty engine
- The `seths` and `workforce` routers in `platform-core` are the primary interface

**Key models:** `Learner`, `Student`, `Employer`, `Opportunity`, `Application`, `Employee`, `TimesheetEntry`, `Document`

**Division accent colour:** As defined in `branding/entity.json`

---

## Division 2: UDOC — Universal Declaration of Operations Compliance

**What it does:** UDOC is the AI governance division. It manages:
- AI model registration and certification
- Live kill-switch suspend/resume for registered models
- Governance decision monitoring and dashboard
- Edge node status and management
- Operator client management
- SaaS governance-as-a-service for external AI operators

**Who uses it:** AI operators (businesses deploying AI), regulators, compliance officers, governance clients.

**Relationship to G.O.D.S Core:**
- UDOC *is* the governance product — it is the externally-facing governance service
- The `registry`, `decisions`, `udoc_engine`, `compliance`, `conformance`, and `enclave` routers serve UDOC
- The `udoc-agent`, `udoc-gateway`, `udoc-edge`, and `udoc-sidecar` are the UDOC attachment components
- UDOC clients receive the full governance path for their AI systems

**Key models:** `AIModel`, `Decision`, `AuditRef`, `SaaSClient`, `OperatorAction`, `OversightCase`

---

## Division 3: TS Industries — Technical and Sovereign Industrial Projects

**What it does:** TS Industries manages industrial and sovereign project participation:
- Project submission from SPVs, government, and private entities
- Tracking and status reporting
- Partner application (to become a build assistant)
- Industrial compliance verification
- Sector-specific governance

**Who uses it:** SPVs (Special Purpose Vehicles), government project offices, private industrial contractors, sovereign fund managers.

**Relationship to G.O.D.S Core:**
- Project decisions (award, rejection, partnership approval) pass through GBS Runtime
- The `ts` and `sectors` routers serve this division
- Cross-jurisdiction project governance via the sovereignty engine
- Capital flow tracking via the MADIBA division interface (through the core)

**Key models:** `TSProject`, `DivisionRecord`

---

## Division 4: MADIBA / EIF — Sovereign Capital and Institutional Finance

**What it does:** MADIBA is the capital and investor engagement division:
- Sovereign and institutional investor engagement
- Capital allocation pipeline management
- Milestone-based funding tracking
- Project updates and reporting
- EIF (Economic Intelligence Foundation) functions

**Who uses it:** Investors, sovereign funds, institutional capital managers, project proponents seeking funding.

**Relationship to G.O.D.S Core:**
- Investment decisions and capital allocations pass through GBS Runtime
- The `madiba` router serves this division
- High-value transactions receive elevated governance scrutiny (EVA threshold adjustments via PolicyPack)
- Cross-border capital flows trigger sovereignty compliance checks

**Key models:** `InstitutionalMilestone`, `CapitalCycle`

---

## Cross-Division Intelligence

The `intelligence` router provides a cross-division view for authorised administrators. It can:
- Identify patterns across divisions (e.g., learners → employment → project participation → investment outcomes)
- Surface governance anomalies that span division boundaries
- Produce reports that trace an individual's journey across the SETHS → TS → MADIBA pathway

Cross-division intelligence access requires `gods_admin` or `intelligence_analyst` RBAC role. The data remains governed — every cross-division query is logged in the audit chain.
