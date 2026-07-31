# UDOC Client Package · App / Mobile / Desktop Client

**Audience:** Tenant SaaS (`role=client` and equivalent)  
**Not:** GODS staff admin, hardware kill-switch plane, access-control user grants  
**API:** `gods-platform-core` only  
**Matrix:** `UDOC_MVP_PACKAGE_MATRIX.md`

## Channels

| Channel | Source |
|---------|--------|
| Web Client | `udoc-public` |
| Desktop Client | `udoc-desktop-client` → Client host |
| App (PWA) | `udoc-app` → `gods-udoc-web` |
| Mobile APK | `udoc-mobile` wraps client `udoc-app` build |

## Client-visible software tabs (role CAPS)

Dashboard · AI Registry · EVA · Policy-to-Code · Intelligence (tenant corpus) · Tenancy  
**Hidden for pure client:** Access Control · staff Hardware plane · global kill-switch chrome

## Client functions (MVP)

1. **Models** — list/register tenant systems; suspend/resume only if CAPS allow (not marketed as hardware kill-switch)
2. **Reports** — decisions table + certificates
3. **Policy** — view active packs; upload/activate only if role allows
4. **EVA** — fair/biased/healthy scenarios · live `POST /decisions`
5. **Tenancy** — plan · API keys

## Staff path

Internal Desktop / Admin Web / Sentinel / Core Portals — **separate packages**.

## Build note

After `udoc-app` source changes: rebuild PWA (`npm run build` in udoc-app) and refresh `udoc-mobile/www` from dist for APK parity.
