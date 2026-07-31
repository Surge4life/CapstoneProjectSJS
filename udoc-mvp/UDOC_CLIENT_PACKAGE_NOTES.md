# UDOC Client Package · App / Mobile / Desktop Client

**Audience:** Tenant SaaS (`role=client` and this app build)  
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

## Client-visible software tabs (role CAPS in App.tsx)

Dashboard · AI Registry · EVA · Policy-to-Code · Intelligence (tenant corpus) · Tenancy  
**Hidden:** Access Control · Hardware plane (HQ-OS / kill-switch UI)

## Package gating (2026-07-31)

| Mechanism | Behaviour |
|-----------|-----------|
| `packageMode.ts` | `UDOC_PACKAGE = "client"` |
| `main.tsx` | sets `html[data-udoc-package=client]` · auto-clicks **Software** plane |
| `styles.css` | hides `.plane.hw` · hides Switch plane · titles **Client** |
| App.tsx CAPS `client` | `hw: []` — no hardware tabs if plane reached |

## Client functions (MVP)

1. **Models** — list/register tenant systems  
2. **Reports** — decisions table + certificates  
3. **Policy** — packs / active enforcement  
4. **EVA** — scenarios · live `POST /decisions`  
5. **Tenancy** — plan · API keys  

## Staff path

Internal Desktop / Admin Web / Sentinel / Core Portals — **separate packages**.

## Rebuild note

After source changes: `cd udoc-app && npm run build` then refresh `udoc-mobile/www` from `dist` for APK parity. Render `gods-udoc-web` auto-deploys from `udoc-app` build on main.
