# Chapter 03 — Learner Portal (SETHS)

## Overview

The learner portal is the primary interface for individuals seeking employment and skills development through the SETHS division. It is accessible via the SETHS web PWA (`seths-app`), the Capacitor mobile app, and through the shared portals web application.

**Primary users:** Job seekers, re-entry individuals, CETCTE participants, students.
**Key jobs-to-be-done:** Find work, track applications, upload documents, view progress.

---

## Information Architecture

```
Learner Portal
├── Dashboard (summary, active applications, notifications)
├── My Profile
│   ├── Personal Details
│   ├── Skills & Experience
│   ├── Education & Qualifications (NQF records)
│   └── Documents (CV, certificates)
├── Opportunities
│   ├── Browse (with filters: sector, location, NQF level, work arrangement)
│   ├── Saved
│   └── Recommended (intelligence-powered matching)
├── My Applications
│   ├── Active
│   ├── History
│   └── Application Detail
├── Documents
│   ├── Upload
│   └── My Documents (with integrity status)
└── Support
    ├── CETCTE Programme (if enrolled)
    └── Rights & Governance
        ├── My Governance Rights
        └── Challenge a Decision
```

---

## Dashboard

The learner dashboard is designed for a single-screen overview:

### Application Pipeline Widget
Visual pipeline showing active applications by stage:
```
Submitted (3) → Under Review (2) → Shortlisted (1) → Offered (0)
```

Clicking any stage shows the applications at that stage.

### Recommended Opportunities Widget
3 opportunities recommended by the G.O.D.S Intelligence matching engine, based on the learner's profile. Each card shows:
- Job title and employer
- Match score (%)
- NQF level requirement
- Location and work arrangement
- "Apply" CTA

### Document Status Widget
Quick view of uploaded documents with integrity status:
- ✅ CV (verified, sealed)
- ✅ NQF 6 Certificate — Unisa (verified, sealed)
- ⚠️ Reference Letter (pending verification)

### Notifications
Recent notifications:
- Application status changes
- New opportunities matching profile
- Document integrity alerts (if any)
- Governance rights notifications (if an oversight case has been opened)

---

## My Applications — Detail View

When a learner views an application in detail:

**Application Timeline:**
```
25 Jan 2025 — Application submitted
27 Jan 2025 — Under review
29 Jan 2025 — Shortlisted ✅
```

**Governance Transparency Panel (collapsed by default):**
A learner can expand this panel to see:
- The governance check that was applied to their shortlisting (or rejection)
- The outcome (APPROVE/BLOCK)
- A plain-language explanation ("Your application was assessed as meeting the listed requirements without any fairness concerns.")
- If a rejection was blocked by governance: "This rejection was flagged by our governance system. A review has been opened."

This is the learner-facing implementation of the Human Primacy doctrine (Volume I, Chapter 04).

---

## Challenge a Decision

If a learner's application was rejected and they believe the rejection was unfair, they can initiate a governance challenge:

**Step 1:** Learner selects "Challenge this decision" from the application detail
**Step 2:** Learner provides their reason for the challenge (free text, required)
**Step 3:** System creates an `OversightCase` linked to the original governance decision
**Step 4:** Learner receives a reference number and expected review timeline
**Step 5:** A compliance officer reviews the case within the SLA
**Step 6:** Learner notified of the outcome

The learner-facing interface is deliberately simple. The governance complexity is internal. From the learner's perspective, they submitted a concern and received a response. The audit trail records everything.

---

## Document Upload Flow

1. Learner taps "Upload Document" 
2. Selects document type (CV, qualification, etc.)
3. If qualification: fills in institution, NQF level, year obtained
4. Selects file (drag-and-drop on desktop, file picker on mobile)
5. Preview shown (PDF preview or filename confirmation)
6. Learner taps "Upload & Seal"
7. Upload progress indicator
8. Success: "Document uploaded and sealed to the UDOC governance chain. Reference: [hash]"

The SHA-256 hash is shown to the learner. They can keep this as their own evidence of the original document state.

---

## Mobile UX Considerations

The SETHS mobile app (`seths-mobile`) wraps the web PWA in Capacitor. Key mobile-specific adaptations:

- **Connect Screen:** On first launch, the app prompts for the backend URL (allows connection to LAN deployments or ngrok tunnels)
- **Offline capability:** The learner's profile and application list are cached in the service worker. Read access works offline. Writes queue and sync when online.
- **Document upload:** Uses the device's native file picker and camera integration (for photographing physical documents)
- **Push notifications:** Kapacitor-native push for application status updates
