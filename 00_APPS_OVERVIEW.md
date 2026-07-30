> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# G.O.D.S ECOSYSTEM — APPLICATIONS OVERVIEW

## UDOC packages (Capstone MVP split)

Full matrix: **`udoc-mvp/UDOC_MVP_PACKAGE_MATRIX.md`**.

| Package | Who | Channel | Dir / host |
|---------|-----|---------|------------|
| **UDOC Internal Desktop** | GODS staff · UDOC admins | Electron | `udoc-desktop` → Admin host |
| **UDOC Client Desktop** | Tenants | Electron | `udoc-desktop-client` → Client host |
| **UDOC Web Client** | Tenants | Browser/PWA | `udoc-public` |
| **UDOC Web Internal** | Staff | Browser | `udoc-internal` |
| **UDOC App + Mobile** | Tenants | PWA / APK | `udoc-app` + `udoc-mobile` (**client only**) |
| **Citizen** | Public | Browser | Client `/citizen.html` |
| **Gateway** | All | Browser | `udoc-gateway` |

Staff mobile for Capstone = install Admin/Internal as PWA (no separate staff APK required).

---

## Wider G.O.D.S installables

| App | Who | What it does | .apk? | Build dir |
|---|---|---|---|---|
| **UDOC Client** | SaaS clients | Register/govern **tenant** AIs, dashboard, portals | yes | udoc-app + udoc-mobile |
| **UDOC Internal** | Staff | Admin control plane (desktop/web) | no staff apk | udoc-desktop + udoc-internal |
| **SETHS** | students/employers/employees | Enrol, progress, documents via UDOC records | yes | seths-app + seths-mobile |
| **MADIBA** | investors | Engagement pipeline | yes | madiba-app + madiba-mobile |
| **TS Industries** | SPV/gov/private | Project tracking | yes | ts-app + ts-mobile |
| **G.O.D.S Admin** | internal | Full control plane (browser) | **NO apk** | platform-web / udoc-internal |

## Each client app
- Installable **PWA today**.
- **Real .apk**: matching `*-mobile/` Capacitor on a machine with Android Studio.
- Connect / API base: deployed Core (`https://gods-platform-core.onrender.com`).

## Honest note
Packages are **role shells** over live web hosts + Core API. Capstone MVP is package clarity + smoke, not commercial SaaS hardening.
