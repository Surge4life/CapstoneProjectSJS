# GIS Alignment + Ecosystem Build — Notes for SJS
13 July 2026 | Read this before merging to main | Full build log: see the tracker file in this delivery

## What was asked, in order
1. Align `gods-intelligence-system.zip` (a standalone GIS package) with GBS, integrate it into the live
   `CapstoneProjectSJS` repo, produce a zip mergeable to main and deployable on Render.
2. Clarification: this repo is the actual G.O.D.S. ecosystem build and the UDOC patent-application
   software evidence — not a lightweight submission project.
3. Extension: build SETHS, M.A.D.I.B.A, T.S. Industries, GBS, and GIS from "scaffolding" into "working
   running" systems.

## What the three uploaded zips actually were (verified by inspection, not assumed)
- `CapstoneProjectSJS-main__2_.zip` — the live repo. 543 files. Deploys as `gods-platform-core` on Render
  (confirmed via `render.yaml`: one Python FastAPI service holds the database connection; every other
  service listed is a static frontend build that talks to it over HTTP).
- `gods-intelligence-system.zip` — a standalone, unintegrated Node/Express/Prisma package. Well-designed
  and already closely aligned to GBS-SETHS v2.0 terminology (12 Pillars, CET/CTE, Skills Passport,
  fail-closed language) — but it would not have started as uploaded (see Bug 2 below), and had never been
  wired into the live repo.
- `GODS_ECOSYSTEM_MERGED.zip` — confirmed via `diff -rq` to be byte-identical to the other two zips just
  placed side by side as sibling folders. Not an integration. This is why the task needed real engineering
  work rather than repackaging.

## Baseline established before any change was made
`smoke_test.py`, run live in-sandbox: **34 passed, 0 failed.** This was the regression bar for everything
below — re-run after every single change, not just once at the end.

## Three real bugs found and fixed (not hypothetical — each was caught by actually running the code)
1. **SAQA 118707 conflation, in code this time.** `seths.py`, `portal_student.py`, `models.py` (×2), and
   `manifest.py` all hardcoded participant/programme records to `"Software Developer 118707"` — your
   personal learnership qualification, not a S.E.T.H.S. programme accreditation. Same error already
   tracked in project memory for prose documents; found here in the live backend and fixed to a generic
   default (`"Digital Operations & AI Literacy"`) and corrected programme-description text.
2. **The GIS package would not have started.** `index.ts` imported `franchise.routes.ts` and
   `certification.routes.ts` — neither file existed in the upload. Written to match the existing
   `participant.controller.ts`/`.routes.ts` pattern, backed by the `Certification` and
   `ComplianceViolation` Prisma models already in `schema.prisma`.
3. **The GIS package would not have compiled at all.** `constants.ts` had an unescaped apostrophe inside a
   single-quoted string (`'...GBS-SETHS's obligation...'`), breaking the string literal. Found by actually
   running `npx tsc --noEmit` against the package's own strict `tsconfig.json`, not by reading the file.
   Fixed, along with every other `noUnusedLocals`/`noImplicitAny` strictness violation already present —
   one of them (`cetcte.service.ts`'s unused `gisService` field) was a real missing integration, now wired
   in as a genuine governance-gate check on stage advancement rather than silenced.

One bug was self-inflicted during this build (a str_replace edit accidentally merged two model classes) —
caught immediately by the functional test suite (a 500 error) rather than shipped. Full detail in the
tracker file. Flagging it because you should know the verification loop actually catches things, including
my own mistakes, not just the original code's.

## What "aligned with GBS" concretely means, division by division
Every division already had **real, tested, but generic** code — a state-machine + arithmetic skeleton that
proves the SETHS→TS→UDOC→M.A.D.I.B.A closed loop shape, without the institution-specific depth documented
in the GBS-SETHS package. Nothing below replaces or breaks that existing skeleton — it extends it.

**GIS** — new, live (`app/services/gis_engine.py`): the twelve-constitutional-pillar fail-closed decision
engine, mirroring the TS reference package exactly. A decision with no verified pillar flags BLOCKs; only
when all twelve pass does it APPROVE. Every decision writes through the same audit chain EVA/UDOC already
use. Endpoint: `POST /gis/decisions`.

**CET/CTE** — new, live (`app/services/cetcte_engine.py`): the real 9-stage journey (Stabilisation →
Phase 6), cohort/stream assignment, the Self-Affirmation Contract, and automatic certification-tier
issuance (Bronze at Stage 1, Silver at Stage 3, Gold at Stage 4, Platinum at Stage 7) — layered on top of,
not replacing, the existing `ENROLLED/COMPLETED/PLACED` status that still drives the closed-loop
simulation. Endpoints under `/gis/participants/{ref}/...`.

**GBS layer** — new, live (`app/services/gbs_engine.py`): the Twelve Constitutional Pillars and Seven GBS
Universal Pillars as real queryable data (`GET /gis/gbs/pillars`), and a franchise node registry (Layers
2-5) with real licence-status transitions and the Document 03 sanctions ladder mechanically applied
(compliance audit below threshold → auto-PROBATION). Endpoints under `/gis/gbs/nodes`.

**T.S. Industries** — corrected + extended (`app/routers/ts.py`): the old `sector` field's comment listed
five values including "HOUSING", which isn't one of the seven documented subsidiaries. Added the correct
seven-subsidiary taxonomy, SPV equity-percentage tracking (20-60% band), and — the significant change — a
**real foreign-key worker assignment** (`TSWorkerAssignment`) linking a specific `PLACED` learner to a
specific project. `workers_deployed` is now a derived count, not an independently-settable number.
Verified: assignment is rejected for any learner not in `PLACED` status.

**M.A.D.I.B.A** — extended (`app/routers/madiba.py`): Series A trigger tracking against the four
conditions from your own live site — 100+ verified placements, 3+ UDOC clients, signed government LOI,
T.S. first project operational — checked against **real DB state** (actual `Learner`/`SaaSClient`/
`TSProject` counts), not hardcoded. The government-LOI trigger has no natural transactional trace, so it's
recorded manually via `POST /madiba/milestones/GOVT_LOI_SIGNED`. `GET /madiba/series-a-status` returns all
four with an honest note that "3+ UDOC clients" counts registered clients, not confirmed-paying ones, since
billing state isn't modelled in this schema yet.

## What this does NOT do — read before assuming more was built than was
- It does not touch the frontend portals (seths-app, madiba-app, ts-app, portals-*) — only `platform-core`
  and `governance-engines/gis`. The new endpoints have no UI yet.
- It does not unify `Learner` and `Student` — two existing tables representing the same real-world
  participant from two angles (operator-facing closed-loop entity vs. self-service portal account). Noted
  clearly rather than silently merged; a real unification is a bigger refactor than this task's scope and
  risks breaking `portal_student.py`/`portal_employer.py` without much deeper testing than was possible here.
- It does not build the M.A.D.I.B.A "3 capital vehicles" concept referenced loosely in project memory — I
  could not find a specific, sourced definition of what the three vehicles are named/structured as, and
  chose not to invent one. If you can point me to where that's specified, I can build it properly next.
- `npx prisma generate` could not be run to completion in this sandbox (no network access to
  binaries.prisma.sh) — run it yourself before `npm run dev`/`npm run build` in the `governance-engines/gis`
  package, or let Render's build step handle it. This does not affect `platform-core`, which needs no
  Prisma client (SQLAlchemy only).
- Nothing here has been run against your actual live Render Postgres instance — only against local SQLite,
  which is what `platform-core` itself uses for dev/test (see `app/db/session.py`). The self-healing schema
  (`_heal_schema()`, already in your codebase) should create the new tables automatically on next deploy,
  the same way it already handles additive schema changes — but confirm this on a staging deploy before
  assuming it either.

## S.E.T.H.S. acronym note carried over from the document-package work
Still unresolved, now also relevant to code comments: three expansions are in circulation across your
materials. I used "Systematically Engineered Transfer of Human Systems" in all new code comments/docstrings
to match the GBS-SETHS v2.0 framework text. Your call on which is canonical still stands.

## How to merge and deploy
1. Review the diff (patch file included) or the full corrected tree (also included).
2. `git apply` the patch to your local clone, or copy the corrected files over manually.
3. Push to main. Render will rebuild `gods-platform-core` automatically per your existing `render.yaml` —
   no new services, no new secrets, no new database required. The self-healing schema handles the new
   tables on boot.
4. For `governance-engines/gis` specifically (the TS reference package): `npm install && npx prisma
   generate` in your own environment before relying on it for local development. It is not part of the
   Render deploy — nothing in `render.yaml` references it, consistent with how `eva`/`udoc`/`gods` already
   work as reference-only code.
5. Run `python smoke_test.py` and `python run_gis_test.py` from the repo root against your local clone to
   reproduce the 34/34 + 30/30 result before you trust the merge.
