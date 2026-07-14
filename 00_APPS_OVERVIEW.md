> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# G.O.D.S ECOSYSTEM — APPLICATIONS OVERVIEW

Per the distribution model: four installable apps + one browser-only admin.

| App | Who | What it does | .apk? | Build dir |
|---|---|---|---|---|
| **UDOC Control** | SaaS clients | Register, govern OWN AIs, live kill-switch suspend/resume, dashboard | yes | udoc-app + udoc-mobile |
| **SETHS** | students/employers/employees | Enrol, progress, browse/apply, **upload & download documents** via UDOC records | yes | seths-app + seths-mobile |
| **MADIBA** | investors | Sovereign/institutional engagement pipeline + project updates | yes | madiba-app + madiba-mobile |
| **TS Industries** | SPV/gov/private | Project submission + tracking + apply to become a partnered build assistant | yes | ts-app + ts-mobile |
| **G.O.D.S Admin** | internal | Full control plane | **NO apk — browser-only, password-protected HTTPS** | platform-web |

## Each app
- Installable **PWA today** (no toolchain): open in browser → Install / Add to Home Screen.
- **Real .apk**: the matching `*-mobile/` Capacitor project compiles to a signed .apk on a
  machine with Android Studio + JDK (SDK can't be installed in the build sandbox; firewall-blocked).
- **Connect screen**: each app asks for your deployed backend URL (LAN IP or ngrok/cloudflared
  tunnel) so it connects live to your G.O.D.S deployment — including from capstoneprojectsjs.netlify.app.

## Document feature (SETHS, as requested)
Upload (CV/qualifications) → stored server-side, SHA-256 sealed, recorded to the UDOC audit
chain + analytics → listed and **downloadable** from the records DB. Production swaps local
storage for S3/object storage (same interface).

## Verified
All four app PWAs build clean (service workers generated). All four data paths verified live
over HTTP (incl. multipart document upload). End-to-end smoke test: 31/31.
