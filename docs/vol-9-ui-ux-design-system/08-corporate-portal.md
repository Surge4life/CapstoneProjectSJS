# Chapter 08 — Corporate / MADIBA Portal

## Overview

The MADIBA portal serves institutional investors, corporate capital managers, and sovereign wealth funds participating in the MADIBA capital investment pipeline. It is accessible from `madiba-app` (role-detected) and `portals-web` (investor view).

---

## Design Philosophy for Institutional Investors

Institutional investors are sophisticated users. They:
- Manage large capital positions and need precision in numbers
- Are accountable to boards and beneficiaries
- Require audit trails for every investment decision
- Prefer formal, professional interfaces over consumer-style designs
- Need export capabilities for board reporting

Design approach:
- **Data density over simplicity** — show more data, not less
- **Formal language** — no conversational copy
- **Report-ready output** — every view should look acceptable in a board pack
- **Number precision** — all currency figures shown with 2 decimal places and ZAR notation
- **Governance visibility** — every capital allocation shows its governance outcome

---

## Information Architecture

```
MADIBA Investor Portal
├── Portfolio Dashboard
│   ├── Total capital committed / deployed / returned
│   ├── Active projects count by sector
│   ├── Milestone completion rate (across portfolio)
│   ├── Governance health (average EVA across portfolio events)
│   └── Recent activity log
│
├── Projects
│   ├── All projects (filterable: sector, province, status, capital range)
│   ├── Project detail
│   │   ├── Project summary + impact metrics
│   │   ├── Milestone tracker
│   │   ├── Capital allocation record
│   │   ├── Governance record (GBS decisions on this project)
│   │   └── Project documents
│   └── Watchlist (projects under consideration)
│
├── Allocations
│   ├── My capital allocations
│   ├── Allocation detail
│   │   ├── Disbursement schedule
│   │   ├── Disbursements to date
│   │   └── Governance record
│   └── New allocation (form → governance check → confirmation)
│
├── Reports
│   ├── Portfolio performance report (quarterly)
│   ├── Capital deployment report
│   ├── Impact report (jobs, SDG alignment)
│   └── Governance compliance report
│
└── Profile
    ├── Investor entity details
    ├── Investment mandate
    ├── KYC/AML status
    └── Notification preferences
```

---

## The Capital Allocation Flow

```
1. Investor selects project from pipeline
2. Investor specifies:
   ├── Allocation type (equity / debt / grant / blended)
   ├── Amount (ZAR)
   └── Disbursement schedule
3. System shows: Allocation summary + projected impact metrics
4. Investor submits → GBS governance path runs
5. Governance outcome:
   ├── APPROVE → Allocation confirmed, project notified
   ├── REVIEW  → Human reviewer confirms within 48h
   └── BLOCK   → Governance notice with reason
6. If approved: Disbursement schedule live, milestone notifications enabled
```

---

## Milestone Tracker

```
Project: Limpopo Solar Farm Phase 2

Milestone 1  [✓ Completed] Site acquisition          Mar 2025
             Capital released: ZAR 5,000,000.00

Milestone 2  [✓ Completed] Environmental approval    Jun 2025
             Capital released: ZAR 5,000,000.00

Milestone 3  [⏳ In Progress] Grid connection permit  Sep 2025
             Capital pending: ZAR 10,000,000.00
             On track: Yes

Milestone 4  [○ Pending]    Construction start       Dec 2025
             Capital pending: ZAR 20,000,000.00
```

Investors receive a notification when a milestone is completed or when a milestone is at risk of missing its target date.

---

## Board Report Export

The MADIBA portal can generate a board-ready portfolio summary:

- A4 PDF formatted for presentation
- Cover page with G.O.D.S entity notation
- Portfolio summary table
- Project detail pages
- Milestone status summary
- Governance compliance statement
- Signed with the audit reference for verification

This document is generated from live data and sealed with an HMAC signature, making it tamper-evident.
