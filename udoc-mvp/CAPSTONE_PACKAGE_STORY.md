# Capstone MVP · Package Story (March 2027)

**Updated:** 2026-07-31  
**Purpose:** One-page map of the **seven Netlify demos** into **Internal vs Client** packages so assessors see product channels, not one mega-HTML.

Source demos: https://capstoneprojectsjs.netlify.app  
Live API: `gods-platform-core` · Neon ≤500MB · Render free · no new user registration required for smoke.

---

## Two packages (hard rule)

| Package | Who | Must include | Must **not** include |
|---------|-----|--------------|----------------------|
| **INTERNAL** | GODS staff · UDOC admins · operators | Kill-switch · global jobs · 24 portals dual-path · Core `/admin` · Sentinel · HITL · Access Control | Tenant sales onboarding UI as the primary product |
| **CLIENT** | External / pilot tenants | Models · Reports · Policy packs · EVA Govern · Tenancy · Bias/Sovereignty view · Citizen public link | Hardware plane · kill-switch UI · cross-tenant admin · staff Access Control |

Backend JWT role remains authoritative. UI gating is defence-in-depth only.

---

## Demo → package → live channel

| # | Demo slug | Primary package | Live channels |
|---|-----------|-----------------|---------------|
| 1 | `udoc-mvp-1` | **Client** | Client Web (`udoc-public`) · App/Mobile · Desktop Client |
| 2 | `udoc-mvp-2` | **Client** (+ Sector) | Client Compliance · Sector console |
| 3 | `udoc-v7-platform` | **Split** | Internal Admin + Client + Citizen + Core `/portals` |
| 4 | `udoc-v7-eva` | **Internal ops** (+ Client Govern) | Core `/Sentinel` · Client Govern EVA |
| 5 | `udoc-v5-sa` | **Internal** (+ Client sov strip) | Sentinel Pillars · Client Sovereignty |
| 6 | `udoc-platform-ui` v9.3 | **Internal** primary | Admin enhance · Policy · Registry; Client subset |
| 7 | `udoc-sovereign-console` v9.3 | **Internal** primary | Admin kill-switch · Sentinel EVA detail; Client no HW |

Patent control detail: `UDOC_V93_DEMO67_PATENT_CONTROLS.md`.

---

## Channel checklist (what to open)

### Internal package
1. **Desktop Internal** — `udoc-desktop` → Admin host; menu: Sentinel · 24 Portals · Core `/admin`
2. **Web Internal** — https://gods-udoc-admin.onrender.com  
3. **Sentinel** — https://gods-platform-core.onrender.com/Sentinel  
4. **24 Portals** — https://gods-platform-core.onrender.com/portals  
5. **Constitutional** — https://gods-platform-core.onrender.com/admin  
6. **Operator** — https://gods-udoc-operator.onrender.com  
7. **Staff mobile (Capstone)** — PWA install of Admin (no separate staff APK)

### Client package
1. **Desktop Client** — `udoc-desktop-client` → Client host; menu: SaaS Portals · Sector · Citizen  
2. **Web Client** — https://gods-udoc-client.onrender.com  
3. **SaaS Portals** — https://gods-udoc-portals.onrender.com  
4. **App / PWA** — https://gods-udoc-web.onrender.com (`udoc-app`, `UDOC_PACKAGE=client`)  
5. **Mobile APK** — `udoc-mobile` wraps client `udoc-app` build  
6. **Citizen (public)** — Client `/citizen.html` — no login

### Gateway
https://gods-udoc-gateway.onrender.com — role → Internal Admin | Operator | Sector | Client SaaS | Citizen surface links.

---

## CAPS (App / Mobile)

`udoc-app/src/App.tsx` role CAPS:

- `client` → software tabs only; **`hw: []`**
- CSS `html[data-udoc-package="client"]` hides `.plane.hw` and plane switch
- `main.tsx` auto-enters Software plane after login

Staff hardware (HQ-OS · Edge · Kill-Switch) lives on **Internal** Desktop/Web only for Capstone packaging.

---

## Capstone bar (assessor)

1. Open **Internal** path and see staff controls (Admin / Sentinel / Portals).  
2. Open **Client** path and see tenant governance only (no kill-switch plane).  
3. Open **Citizen** without login.  
4. Gateway routes by role.  
5. Live smoke: health + `/udoc/demo/ready` + **biased = BLOCK** on Client Govern and Sentinel.

Task 2 closes when step 5 is green on live hosts (operator).  
GIS / GBS / GODS Intelligence expansion remain **after** that bar.
