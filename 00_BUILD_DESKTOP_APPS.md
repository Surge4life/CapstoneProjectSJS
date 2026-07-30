> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# Building the G.O.D.S Desktop (.exe) Applications

Electron shells load **live hosts** (always current). UDOC is split into two products.

| App | Build dir | Window opens |
|---|---|---|
| **UDOC Internal** (staff) | `udoc-desktop` | Admin · menu → Sentinel / Portals / Core admin |
| **UDOC Client** (tenant) | `udoc-desktop-client` | Client · menu → SaaS Portals / Sector / Citizen |
| SETHS | `seths-desktop` | portals site |
| MADIBA | `madiba-desktop` | portals site |
| TS Industries | `ts-desktop` | portals site |
| GODS Portals | `portals-desktop` | portals site |

Matrix: `udoc-mvp/UDOC_MVP_PACKAGE_MATRIX.md`.

## Prerequisites
- Node.js 18+ — https://nodejs.org

## Build
```bash
cd udoc-desktop              # or udoc-desktop-client
npm install
npm run dist
```
Output in `release/`: installer + portable `.exe`.

## Test without packaging
```bash
cd udoc-desktop && npm install && npm start
cd udoc-desktop-client && npm install && npm start
```

## PWA alternative
Install Admin or Client from the browser (Edge/Chrome → Install) — zero Electron build.
