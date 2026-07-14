# CHANGELOG_BRAND.md — Pre-Registration & Brand Rollout
**Date:** June 2026 · **By:** Sashin J. Singh · **Scope:** whole GODS_ECOSYSTEM repository, one pass.

This rollout aligns the entire repository with the project's first pillar (S.E.T.H.S — honesty) and applies the canonical G.O.D.S brand. The constants are recorded in `BRAND_AND_ENTITY_CONSTANTS.md` and are to **remain constant for all future builds, alignments, and deployments**.

## Honesty corrections
- **Demo / dev emails:** `@gods.za` → `@gods.local` — **52 replacements across 32 files** (frontend login auto-fill, backend `seed.py`, smoke tests, docs). Both seed and login sides changed together, so the demo still works; `gods.local` is a reserved local suffix that cannot be mistaken for a registered public domain.
- **Company suffix:** `(Pty) Ltd` → `(Pty) Ltd (proposed)` — 10 files. Reflects that no company is registered.
- **Verified absent (no change needed):** no `gods.systems`, no constituted IP Trust claim, no registered-trademark (®) claims existed in the repo.
- **Intentionally unchanged:** "registered" strings that refer to **AI-model registration** (a product feature, e.g. "model not registered") — these are not legal claims.
- **Asset text:** corrected "IP TRUST PROTECTED" and "G.O.D.S IP TRUST" baked into the diagonal/seal watermark SVGs to "PRE-REGISTRATION FORECAST" / "G.O.D.S — PROPOSED".

## Brand application
- **PWA icons:** all `icon-192.png` and `icon-512.png` across **11 apps** replaced with the new G.O.D.S master-mark favicon (navy shield + gold compass).
- **Entry pages:** a pre-registration ribbon and an `x-gods-status` meta tag added to all **15** `index.html` files.
- **PWA manifests:** all **6** webmanifests now carry a "(proposed)" name and an honest description.

## New canonical files
- `BRAND_AND_ENTITY_CONSTANTS.md` — the single constant reference (entity status, identifier rules, brand tokens, asset locations, 2026 SA trademark position).
- `PRE_REGISTRATION_NOTICE.md` and `IP_NOTICE.md` — honest status and IP attribution.
- `branding/` — `gods.brand.css` (canonical tokens), `entity.json` (machine-readable status), `footer-disclaimer.html` (canonical footer), and `assets/` (logos, divisions incl. the redrawn M.A.D.I.B.A, favicon, watermarks).

## Verification
- `@gods.za`: **0** remaining · unqualified `(Pty) Ltd`: **0** · `gods.systems` / `IP TRUST PROTECTED`: **0** (outside honest negations in the notice files) · new icons match the master mark on all 11 apps · ribbon renders on entry pages.

*If status changes (e.g. company registered, marks filed), update `BRAND_AND_ENTITY_CONSTANTS.md` §1–§2 first, then propagate.*
