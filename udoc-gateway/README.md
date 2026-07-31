# UDOC Gateway

**Live host:** `gods-udoc-gateway` (static `index.html`)  
**Role:** Package sign-on — routes JWT users to Internal vs Client hosts.

## Capstone package routing

| Role | Destination | Package |
|------|-------------|---------|
| `admin` · `exec` | gods-udoc-admin | **Internal** |
| `auditor` | gods-udoc-admin | **Internal** |
| `operator` · `viewer` | gods-udoc-operator | **Internal** |
| `gov` | gods-udoc-sector | **Internal · Sector** |
| `client` | gods-udoc-client | **Client SaaS** |

Public (no login): Client `/citizen.html`.

All consoles call `gods-platform-core`. Matrix: `udoc-mvp/UDOC_MVP_PACKAGE_MATRIX.md`.

## Hardware gateway note

`gateway.py` is the **appliance** lineage/relay sketch (mTLS / air-gap). Not the Render static sign-on UI.
