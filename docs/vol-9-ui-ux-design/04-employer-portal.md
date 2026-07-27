# Chapter 04 — Employer Portal

## Overview

The employer portal is the interface for verified employers managing their recruitment pipeline within the G.O.D.S SETHS division. It is accessible from `seths-app` (via role detection post-login) and `portals-web` (employer view).

---

## Information Architecture

```
Employer Portal
├── Dashboard
│   ├── Active opportunities overview
│   ├── Application pipeline summary (new / under review / shortlisted)
│   ├── Compliance status (bias score, pending governance reviews)
│   └── Recent activity feed
│
├── Opportunities
│   ├── Active opportunities list
│   ├── Create opportunity (form + GBS pre-check)
│   ├── Opportunity detail
│   │   ├── Applicant pipeline (kanban)
│   │   ├── Opportunity analytics (views, application rate)
│   │   └── Edit / close
│   └── Archived opportunities
│
├── Applications
│   ├── All applications (across all opportunities)
│   ├── Application detail
│   │   ├── Applicant profile (skills, NQF, documents)
│   │   ├── CETCTE notice (if applicable — anonymous until consent)
│   │   ├── Governance record for this application
│   │   └── Actions: shortlist / request info / reject / offer
│   └── Pipeline kanban (drag-and-drop status changes)
│
├── Compliance
│   ├── Employment equity metrics (own data)
│   ├── Bias score trend (90-day)
│   ├── Pending governance reviews
│   └── Rejection justification log
│
├── Documents
│   └── Employer verification documents (upload, view)
│
└── Settings
    ├── Company profile
    ├── Notification preferences
    └── Team members (sub-accounts)
```

---

## The Application Pipeline (Kanban)

The kanban view is the primary employer workflow tool:

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   New (23)  │ Reviewing(8)│Shortlisted(5)│ Interview(3)│  Offer (1)  │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ [Applicant] │ [Applicant] │ [Applicant] │ [Applicant] │ [Applicant] │
│ NQF 6       │ NQF 7       │ NQF 6       │ NQF 6       │ NQF 7       │
│ 3 years exp │ 5 years exp │ 4 years exp │ 4 years exp │ 6 years exp │
│ [View] [→]  │ [View] [→]  │ [View] [→]  │ [View] [→]  │ [View] [→]  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

Cards show: pseudonymous identifier (for CETCTE applicants), NQF level, experience summary, skills match percentage.

Drag a card to the next column to change status. Rejecting (moving to a terminal state) opens a rejection reason dialog — the reason is required and submitted to the GBS governance path.

---

## The Rejection Dialog

Rejection is a governance event. The employer must provide:

1. A rejection reason code (dropdown)
2. A brief note (text, min 20 chars)
3. Acknowledgement that the rejection will be reviewed by the G.O.D.S governance system

After submission:
- GBS evaluates the rejection (FA dimension, historical bias check)
- If APPROVE: rejection confirmed, applicant notified with governance reference
- If REVIEW: rejection held pending human review
- If BLOCK: rejection blocked — employer receives governance notice; compliance officer reviews

The employer cannot see the internal GBS evaluation details, but receives the governance reference number they can use for dispute resolution.

---

## Employment Equity Dashboard

Shows the employer's own equity metrics (not other employers'):

```
┌──────────────────────────────────────────────────────────┐
│ Employment Equity Dashboard — Last 90 Days               │
├─────────────────────┬────────────────────────────────────┤
│ Applicant Pool      │ █████████░ 9.2% shortlisting rate  │
│ Province: Gauteng 47%│ ████░░░░░░ 5.1% hire rate         │
│ Province: WCape 23% │                                    │
├─────────────────────┴────────────────────────────────────┤
│ Bias Score: 0.12 (LOW — normal governance scrutiny)      │
│ Trend: ↓ improving (-0.04 from last quarter)             │
└──────────────────────────────────────────────────────────┘
```

The bias score is presented with plain language explanation of what it means and what actions can be taken to improve it.

---

## CETCTE Applicant Handling

When a CETCTE participant applies for an opportunity, the employer sees:

```
┌──────────────────────────────────────────────────┐
│ Candidate Profile — ANONYMOUS                    │
│ (This candidate has requested anonymous review)  │
├──────────────────────────────────────────────────┤
│ NQF Level: 6                                     │
│ Experience: 4 years in software development      │
│ Skills: Python ✓ (Certified) | React ✓ (Evidenced)│
│ Location: Available to relocate                  │
├──────────────────────────────────────────────────┤
│ [Request Introduction] [Reject]                  │
│                                                  │
│ Requesting introduction will reveal the          │
│ candidate's identity with their consent.         │
└──────────────────────────────────────────────────┘
```

The employer evaluates on skills and experience alone. Identity is only revealed if both employer and candidate consent to the introduction. This is the constitutional anonymity protection in practice.
