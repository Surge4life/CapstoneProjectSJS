# BRAND_AND_ENTITY_CONSTANTS.md
### The single, constant reference for the entire G.O.D.S ecosystem
**This file is canonical. Every build, alignment, and deployment — now and in future — conforms to it.**
© 2026 Sashin J. Singh · G.O.D.S Holdings (Pty) Ltd *(proposed)*

---

## 1 · ENTITY STATUS (must never be overstated)
- **G.O.D.S Holdings (Pty) Ltd is a PROPOSED entity name — not a registered company.**
- **No** company, IP trust, trademark, or domain has been registered.
- **All intellectual property presently vests in the founder, Sashin J. Singh, as author.**
- Upon incorporation, IP is *intended* to be vested in a **G.O.D.S IP Trust** to be constituted under the **Trust Property Control Act 57 of 1988**, with a perpetual exclusive licence to the operating company.
- Marks carry **™** as common-law notice of intent only. **®** is used **solely after confirmed CIPC registration.**
- Machine-readable version: [`branding/entity.json`](branding/entity.json).

## 2 · IDENTIFIERS — WHAT MAY AND MAY NOT BE CLAIMED
| Item | Rule |
|---|---|
| Public domain | **None registered.** Do **not** assert `gods.systems`, `gods.za`, or any public domain until it is actually owned. |
| Demo / dev email | Use **`@gods.local`** only (reserved local suffix; not a public domain). Never use a real-looking public address. |
| Deployment URLs | Only the actual hosts in use (e.g. `*.onrender.com`) may appear as live; everything else is "to be registered". |
| Company suffix | Write **"G.O.D.S Holdings (Pty) Ltd (proposed)"** wherever legal status is implied. |

## 3 · BRAND — CANONICAL TOKENS
Import [`branding/gods.brand.css`](branding/gods.brand.css); never hardcode.
- **Core:** gold `#C9A84C` · navy `#060E1C` (deepest `#040B16`). Gold light `#E8C97A`, dim `#8B6914`. Navy mid/lift/accent/border `#0C1A2E`/`#122238`/`#1A3050`/`#243A5A`.
- **Text:** `#F5F0E8` / `#D4CEBC` / `#7A7A8A`.
- **Division accents:** S.E.T.H.S `#E87B3A` · M.A.D.I.B.A `#D4A017` · UDOC `#7C5CBF` · T.S `#2D9B5A` · HQ-OS `#00E5FF`.
- **Type:** Display Playfair Display (Georgia) · Body Cormorant/EB Garamond (Times) · UI Barlow (system-ui) · Mono IBM Plex Mono.
- **Clear space** 1× mark height · **min** 48 px screen / 32 px favicon / 15 mm print.

## 4 · MARKS / ASSETS (single source)
All in [`branding/assets/`](branding/assets): `logos/` (master dark/light/gold, emblem, lockups), `divisions/` (S.E.T.H.S, T.S Industries, UDOC, **M.A.D.I.B.A — dignified Africa**, HQ-OS), `favicon/` (SVG + 32/48/192/512 PNG — used for all PWA `icon-192/512.png`), `watermarks/` (seal, diagonal, 4 classification ribbons). **Reproduce from these files; never redraw.**

## 5 · FOOTER / DISCLAIMER
Public/human-facing surfaces include the canonical footer in [`branding/footer-disclaimer.html`](branding/footer-disclaimer.html) (or the `.gods-prereg-ribbon` from the brand CSS at minimum).

## 6 · TRADEMARK POSITION (2026, SA — planned only)
Trade Marks Act 194 of 1993 · CIPC (IPOnline) · single-class (Form TM1/class) · **Nice 13th Edition (from 1 Jan 2026; AIaaS classified)** · ~R590 file / R260 renew per class · 10-yr term · **South Africa is NOT a Madrid member** → direct national/regional filing (CIPC → ARIPO/OAPI → EUIPO/UKIPO/USPTO). **Nothing is filed yet.**

## 7 · WHAT WAS APPLIED IN THIS ROLLOUT
- Demo emails `@gods.za` → `@gods.local` (52 fixes, 32 files) — seed, login, docs, tests kept consistent.
- `(Pty) Ltd` → `(Pty) Ltd (proposed)` (10 files).
- All PWA `icon-192/512.png` (11 apps) → new G.O.D.S master-mark favicon.
- Added `branding/` (CSS, entity.json, assets, footer) and root notices (`PRE_REGISTRATION_NOTICE.md`, `IP_NOTICE.md`).
- "registered" strings referring to **AI-model** registration were intentionally left unchanged (product feature, not a legal claim).

*Keep this file constant. If status changes (e.g. company registered), update §1–§2 here first, then propagate.*
