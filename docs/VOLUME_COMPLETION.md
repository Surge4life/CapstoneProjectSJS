# Engineering Canon — Volume completion (2026-08-27)

Replit Agent (25 Jul 2026, `c21711aa`) started the 11-volume tree and hit usage limits. A later merge (PR #25, 27 Jul) filled most remaining chapters **into duplicate folder names**. Yesterday’s Replit session **did not push** to GitHub.

This commit:

1. Merges split folders into the Canon paths named in [`ENGINEERING_CANON.md`](ENGINEERING_CANON.md).
2. Leaves redirect READMEs at the old folder names so old links do not 404.
3. Fixes Volume VI and Volume XI README links to **actual filenames**.
4. Adds Capstone honesty notes on Volume V (designed vs live).

**No live application code was changed.** Render still deploys `platform-core` from `main`; this is documentation only.

## Canonical folders (Plane B)

| Vol | Path | Chapters on disk |
|-----|------|------------------|
| I | `vol-1-ecosystem-canon/` | 01–12 + README |
| II | `vol-2-system-architecture/` | 01–19 + README |
| III | `vol-3-repository-blueprint/` | 01–14 + README |
| IV | `vol-4-intelligence-whitepaper/` | 01–16 + README |
| V | `vol-5-gbs-constitutional-runtime/` | 01–10 + README |
| VI | `vol-6-developer-implementation-guide/` | 01–14 + README |
| VII | `vol-7-database-design/` | 01–11 + README |
| VIII | `vol-8-api-reference/` | 01–14 + README |
| IX | `vol-9-ui-ux-design-system/` | 01–12 + README |
| X | `vol-10-infrastructure/` | 01–13 + README |
| XI | `vol-11-roadmap/` | 01–07 + README |

## Redirect stubs (do not add new chapters here)

- `vol-5-gbs-runtime/README.md`
- `vol-6-developer-implementation/README.md`
- `vol-9-ui-ux-design/README.md`

## Honesty

Canon volumes describe **constitutional design**. Capstone live proof remains Plane A (`udoc-mvp/`) on Render free + Neon ≤500MB. Kafka / Cassandra / HSM / air-gap chapters are target architecture unless a chapter explicitly says it is live.
