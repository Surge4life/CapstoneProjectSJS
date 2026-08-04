# Admin path naming (hyphen vs underscore)

## Three different “Admin” surfaces

| What | URL | Source file |
|------|-----|-------------|
| **Internal package (dense)** | `https://gods-udoc-admin.onrender.com/` | `udoc-internal/` static host |
| **UDOC controller on Core** | `https://gods-platform-core.onrender.com/udoc-admin` | `static/udoc_admin_v93.html` |
| **GODS constitutional** | `https://gods-platform-core.onrender.com/admin` | `static/admin.html` |

## Hyphen vs underscore

| Path | Status |
|------|--------|
| `/udoc-admin` | **Canonical** (hyphen) |
| `/udoc_admin` | **Alias** (same SPA) — added 2026-08-04 |
| Filename `udoc_admin_v93.html` | Underscore on disk only |

Do not use underscore on the **Render service name** (`gods-udoc-admin` is correct with hyphens).

## Surface 4 smoke

Prefer Core when the Render Admin host blank-caches:

1. https://gods-platform-core.onrender.com/udoc-admin  
2. Or https://gods-platform-core.onrender.com/admin  
3. Login `admin@gods.local` / `admin123`  
4. EVA / decisions path same Core API  
