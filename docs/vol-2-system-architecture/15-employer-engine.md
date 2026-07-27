# Chapter 15 — Employer Engine

## Purpose

The Employer Engine manages employer registration, verification, opportunity management, and employment equity compliance within the SETHS division. It is the counterpart to the Learner Engine — while the Learner Engine serves individuals seeking work, the Employer Engine serves organisations offering it.

---

## Location

- **Router:** `platform-core/app/routers/seths.py` (employer routes)
- **Router:** `platform-core/app/routers/portals_employer.py`
- **Service:** Part of the SETHS service layer
- **Frontend:** `seths-app` (employer views), `portals-web` (employer portal)

---

## Employer Registration and Verification

An employer must complete a two-step process before posting opportunities:

**Step 1: Self-registration**
- Company name, registration number (CIPC)
- Industry sector
- Province and contact details
- BEE level declaration
- Employment Equity plan status

**Step 2: Verification**
- Compliance officer verifies the CIPC registration number against the CIPC public register
- If the company is listed and active: `verification_status → verified`
- If unverifiable or discrepancies found: `verification_status → requires_clarification`
- Unverified employers can register but cannot post opportunities until verified

The verification creates a `GIS_CERTIFICATION` of type `EMPLOYER_VERIFIED`.

---

## Opportunity Lifecycle

```
DRAFT → ACTIVE → CLOSED
                  ↑
              (date reached or employer action)
         ACTIVE → FILLED (when offer accepted)
         ACTIVE → WITHDRAWN (employer withdraws)
```

An opportunity can only be posted by a verified employer. Each opportunity goes through a GBS compliance check before it becomes `ACTIVE`:

- Does the NQF requirement match the role description?
- Does the salary range meet minimum wage requirements?
- Are any stated requirements potential proxies for protected characteristics?
- Is the geographic restriction legally justified?

If any check fails, the opportunity is flagged for compliance review before being published.

---

## Application Management

From the employer perspective, the application pipeline is:

```
New Applications → Under Review → Shortlisted → Interview (employer-managed) → Offer → Accepted
                                              → Rejected (GBS governed)
```

Every rejection that goes through the system is submitted to the governance path. The employer provides a rejection reason, which is checked by the EVA fairness dimension for:
- Explicit protected characteristic references
- Proxy language (e.g., "cultural fit" without substantiation, "location preference" that correlates with race)
- Pattern consistency with the employer's historical rejection behaviour

---

## Employment Equity Monitoring

The Employer Engine feeds data to the bias detection service on a rolling basis:

**Tracked metrics per employer:**
- Applicant pool composition (by province, NQF level, and self-declared demographics where provided)
- Shortlisting rate by NQF level
- Offer acceptance rate
- Historical GBS block rate on rejections

**The `bias_score` field** on the `seths.employers` table is recomputed weekly by the analytics engine. It summarises the employer's bias pattern over the trailing 90 days:

| Bias Score | Meaning | System Response |
|-----------|---------|----------------|
| 0.0–0.30 | Low detected bias | Normal processing |
| 0.31–0.60 | Moderate detected patterns | EVA fairness dimension threshold elevated |
| 0.61–0.80 | Significant patterns | Rejection decisions require compliance review |
| 0.81–1.0 | Severe patterns | Employer account flagged; compliance officer alerted |

The bias score is a governance signal, not a sanction. It adjusts the governance scrutiny applied to this employer's future actions. A compliance officer reviews severe cases and determines whether escalation or remediation is required.

---

## Employer Portal

The employer portal (`portals-web` employer view) provides:
- Application pipeline management (kanban view of active applications)
- Candidate search (within governance boundaries)
- Opportunity creation and management
- Employment equity dashboard (own metrics, not other employers')
- GBS compliance notifications
- Billing (if SaaS deployment)
