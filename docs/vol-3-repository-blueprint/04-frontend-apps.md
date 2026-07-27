# Chapter 04 — Frontend Applications (Web PWAs)

## Overview

The G.O.D.S ecosystem has five web frontend applications. Each is a React + Vite Progressive Web App (PWA). They share a design language (see Volume IX) but have completely distinct information architectures and user journeys.

---

## Common Structure

Every frontend app follows this structure:

```
{division}-app/
├── public/
│   ├── manifest.json        PWA manifest (icons, name, start_url, theme_color)
│   ├── icons/               App icons at all required sizes (72, 96, 128, 144, 152, 192, 384, 512)
│   └── robots.txt
├── src/
│   ├── main.tsx             React entry point + service worker registration
│   ├── App.tsx              Root component + router
│   ├── api.ts               All API calls (the ONLY place fetch/axios is used)
│   ├── types.ts             TypeScript interfaces for all domain models
│   ├── components/          Shared UI components for this app
│   ├── pages/               Page-level components (one per route)
│   ├── hooks/               Custom React hooks
│   ├── utils/               Utility functions
│   └── assets/              Images, fonts, static assets
├── index.html               Vite entry HTML
├── vite.config.ts           Vite + PWA plugin configuration
├── tsconfig.json
├── package.json
└── .env.example             Required environment variables
```

---

## `udoc-app/` — UDOC Control

**Who uses it:** AI operators, governance clients, UDOC SaaS users  
**Primary purpose:** Register and monitor governed AI models, view governance decisions, manage oversight cases, access governance dashboards  

**Key pages:**
- `Login` — credential entry with connect-screen (backend URL configuration)
- `Dashboard` — live governance decision feed, model status overview
- `ModelRegistry` — list, register, certify, suspend models
- `DecisionInspector` — drill into any governance decision (EVA scores, reasoning, seal)
- `OversightCases` — manage open cases
- `EdgeNodes` — status of udoc-agent/edge/gateway attachments
- `Settings` — account, API keys, notification preferences

**Connect Screen:**  
On first launch (or when no backend URL is configured), the app shows a connect screen prompting for the backend URL. This allows the app to connect to any G.O.D.S deployment — cloud, LAN, or ngrok tunnel.

---

## `seths-app/` — SETHS

**Who uses it:** Learners, employers, employment practitioners  
**Primary purpose:** Job seeking, opportunity posting, application management, document upload  

**Key pages:**
- `Connect` — backend URL configuration
- `Login` / `Register` — role-based registration (learner or employer)
- `Dashboard` — role-appropriate overview
- `Opportunities` — search and filter (learner) or manage postings (employer)
- `Applications` — track applications (learner) or manage pipeline (employer)
- `Documents` — upload and manage sealed documents (learner)
- `Profile` — skills, qualifications, NQF record

---

## `madiba-app/` — MADIBA

**Who uses it:** Investors, sovereign fund managers, institutional capital managers  
**Primary purpose:** Capital allocation pipeline, milestone tracking, project updates, investor engagement  

**Key pages:**
- `Connect` + `Login`
- `Dashboard` — capital pipeline overview, milestone status
- `Projects` — list of projects seeking or receiving capital
- `Milestones` — milestone tracking and reporting
- `InstitutionalProfile` — investor registration and profile management
- `Reports` — capital deployment and impact reports

---

## `ts-app/` — TS Industries

**Who uses it:** SPVs, government project offices, private contractors  
**Primary purpose:** Project submission, tracking, and partner applications  

**Key pages:**
- `Connect` + `Login`
- `Dashboard` — project pipeline overview
- `Projects` — submit, view, and track industrial projects
- `Partners` — apply to become a build assistant partner
- `Sectors` — sector-specific information and requirements
- `Reports` — project status and governance reports

---

## `platform-web/` — G.O.D.S Admin Console

**Who uses it:** G.O.D.S administrators, compliance officers, sovereignty officers  
**Primary purpose:** Full platform control — all four divisions + infrastructure  
**Access:** Browser-only, password-protected, not available as a mobile app  

This is the most complex frontend. It has integrated consoles for all four divisions plus platform-level administration. See Volume IX, Chapter 06 for the detailed information architecture.

---

## PWA Requirements

Every frontend app is a fully compliant PWA:

| Requirement | Implementation |
|------------|---------------|
| Service worker | `vite-plugin-pwa` generates SW with Workbox |
| App manifest | `public/manifest.json` with all required fields |
| Icons | All sizes: 72, 96, 128, 144, 152, 192, 384, 512px |
| Offline capability | Core views cached; writes queue for sync |
| Install prompt | Handled via `beforeinstallprompt` event |
| HTTPS required | Enforced in production; localhost exempted for dev |

---

## The Connect Screen Pattern

Every division app (not `platform-web`) shows a connect screen on first launch. This is intentional:

```
[App loads]
    ↓
[Check localStorage for saved backend URL]
    ↓ Not found
[Show connect screen]
  "Enter your G.O.D.S deployment URL"
  [https://gods-platform-core.onrender.com]  [Connect]
    ↓ URL saved
[Proceed to login]
```

This pattern allows a single mobile app to connect to any G.O.D.S deployment in the world — a pilot client's private server, a national deployment, or the public cloud instance — without releasing a new app binary.
