> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# SKILLS.md — G.O.D.S Build: hard-won technical know-how (handoff for a new chat)

> Companion to MEMORY.md. These are the concrete techniques, gotchas, and exact procedures
> proven across this build. Read before touching code so nothing is re-debugged from scratch.

---

## ENVIRONMENT REALITIES (assistant sandbox)
- Shell is **`sh`, not bash**. `declare -A`, `${VAR:0:N}`, brace-expansion FAIL.
  → Wrap bash-isms in `bash << 'BASH' ... BASH`.
- **Network is locked** to a few registries (npm, pip, etc.). `github.com` push, `dl.google.com`
  (Android SDK / AGP Maven), and Electron's binary download are **BLOCKED (403/unreachable)**.
  → The assistant cannot push to GitHub or compile .apk/.exe. The USER does those on their machine.
- `pip install` needs `--break-system-packages`.
- Heredoc content in bash tool calls must NOT contain a literal `</parameter>` string (premature
  truncation). Restructure content to avoid it.
- For very large files, validate structurally with Python (`open().read().count(...)`) rather than
  relying on shell return codes.

## PYTHON / FASTAPI (platform-core)
- **Config & Render DB:** `app/core/config.py` reads `os.environ["DATABASE_URL"]` (unprefixed,
  Render injects it), else falls back to the `GODS_`-prefixed setting / sqlite default. Then it
  MUST rewrite the scheme to **`postgresql+psycopg://`** for BOTH `postgres://` and `postgresql://`
  (SQLAlchemy otherwise reaches for psycopg2, which is not installed; we ship `psycopg[binary]`).
- **requirements.txt pins that matter:** `bcrypt==4.0.1` (passlib breaks on bcrypt 4.x),
  `email-validator` (pydantic EmailStr), `psycopg[binary]==3.2.3`, `python-multipart` (file upload).
- **Governance seal:** HMAC over `round(eva_svs, 4)` so verify matches sign. HSM emulated key MUST
  be deterministic (sha256 of a fixed seed) so sign/verify work across processes.
- **Audit chain:** appends MUST be serialized — `audit_writer._append_lock` (threading.Lock).
  Without it the hash-chain head is a read-modify-write race under concurrency (the stress test
  caught this). Production = single-writer Cassandra WORM partition.
- **Access control:** `app/services/access_control.py` maps role+division → permitted systems;
  `/access/profile` (launcher source) + `/access/guard/{system}` (hard 403). Server is authoritative;
  UI gating is never trusted alone.
- **Register a new router:** add to both the import tuple AND the include tuple in `app/main.py`.
- **Verify before claiming done:** `python3 -m pytest tests/test_governance.py -q` (8/8),
  `python3 tests/stress_chaos.py` (10/10), `python3 smoke_test.py` (34/34, starts its own backend).

## REACT / VITE (frontends + apps)
- `useEffect(() => { refresh(); }, [])` — call inside an arrow fn, not `useEffect(refresh)`.
- Add `src/vite-env.d.ts` with `/// <reference types="vite/client" />`; PWA apps also need
  `/// <reference types="vite-plugin-pwa/client" />`.
- **Runtime-configurable backend URL** pattern (the connect screen): `getBase()` returns
  `localStorage value || import.meta.env.VITE_API_BASE || "http://localhost:8000"`. This lets the
  SAME build connect to localhost, a LAN IP, a tunnel, or the Render URL.
- **Static-site env vars are BUILD-TIME** (Vite bakes them in). Setting `VITE_API_BASE` only takes
  effect on a rebuild. On Render, set it in the dashboard Environment (triggers rebuild) or in
  `render.yaml`. `fromService ... property: host` gives a bare host (no scheme) → use a full
  `value: https://...` instead.
- Build check: `npm install && npm run build`; PWA build should emit `dist/sw.js`.
- **No localStorage/sessionStorage in claude.ai artifacts** — but in these real deployed apps
  localStorage is fine (they run in a normal browser/WebView, not the artifact sandbox).

## DOCX / LARGE FILE BUILDS (from the patent/spec era — still useful)
- `.docx` via the Node `docx` lib: shared helper object + a runtime `tbl()` column-width guard
  prevents header/column mismatch. Landscape = swap PAGE_PROPS width/height. For big builds, split
  into part scripts and merge with `python-docx`. `grep -n` → `sed -n 'A,Bp'` → `str_replace` for
  precise edits.

## RENDER DEPLOYMENT (proven path)
- **Order:** GitHub FIRST (Render builds from a repo), then Render → New → Blueprint → pick repo →
  Apply. `render.yaml` must be at the **repo root**.
- **render.yaml shape:** `databases:` lists Postgres (free plan); `services:` has the web service
  (`runtime: python`, build `pip install -r requirements.txt`, start
  `python seed.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT`, `healthCheckPath: /health`,
  `DATABASE_URL` via `fromDatabase`, `GODS_JWT_SECRET` via `generateValue: true`) plus static sites
  (`runtime: static`, build `npm install && npm run build`, `staticPublishPath: dist`, SPA rewrite
  to `/index.html`, `VITE_API_BASE` as a full https value).
- **Free-tier facts:** web sleeps after 15 min idle (30s–2min cold start); free Postgres expires in
  30 days. For a demo, warm the URL first by hitting `/health`.
- **Debugging a failed deploy:** read the **Events → View Logs**; the red line is the cause. The
  classic first failure here was `ModuleNotFoundError: No module named 'psycopg2'` → the scheme fix above.

## GIT / GITHUB (user-side, Windows)
- VS Code drag-and-drop on github.com caps at ~100 files — for this repo (~400 files) use **VS Code
  Source Control → Initialize → Commit → Publish**, or `git` CLI. The web upload will silently
  partial-fail past the cap.
- **First commit needs identity:** `git config --global user.name "..."` and
  `git config --global user.email "..."` or VS Code errors "configure user.name and user.email".
- If the repo was created WITH a README, histories diverge → `git pull origin main
  --allow-unrelated-histories` then `git push -u origin main`.
- GitHub HTTPS auth: use the browser sign-in popup, or a **Personal Access Token** (classic, `repo`
  scope) as the password — GitHub blocks account passwords.
- **Upload the CONTENTS of GODS_ECOSYSTEM** so `render.yaml` sits at repo root (not nested).

## ANDROID .APK BUILD (Windows, proven end-to-end with udoc-mobile)
- Prereqs: Node 18+ (user had v24), Android Studio (SDK), JDK 17.
- Steps (in the `*-mobile` folder): `npm install` → `npx cap add android` → `npx cap sync` →
  `npx cap open android` → in Studio **Build → Build Bundle(s)/APK(s) → Build APK(s)**.
- Output: `android\app\build\outputs\apk\debug\app-debug.apk`.
- **Gradle/JDK:** Gradle 8.2.1 is incompatible with JVM 21 → when prompted choose **"Use JVM 17"**
  (or Settings → Build Tools → Gradle → Gradle JDK = jbr-17). Studio auto-installs Build-Tools 34 +
  Platform 34. **Do NOT run the AGP Upgrade Assistant** (keeps the first build simple).
- The huge `Download ... .pom/.jar` wall in the sync log is NORMAL (first-build dependency fetch).
- **HTTPS backend needs no extra config** (Capacitor scaffolds INTERNET permission). The
  `android-resources/` (network_security_config cleartext, strings, manifest perms) are only needed
  if pointing at a plain-http LAN backend.
- Signed release (for sharing/Play): Studio → Build → Generate Signed Bundle/APK → APK → keystore.
- Choose **APK** (installable) not **Bundle/.aab** (Play-Store-upload only) for sideload/testing.

## DESKTOP .EXE BUILD (Electron, prepared, user-side)
- Each `*-desktop/` has `main.js` (opens the live site in a native window, external links to browser,
  offline fallback), `package.json` (electron + electron-builder, Windows nsis + portable),
  `preload.js`, `icon.png`. Build on the user's machine: `npm install && npm run dist` →
  `release/`. Electron downloads its runtime on first install (blocked in sandbox, fine on desktop).
- **PWA install is the no-build desktop option:** open the live site in Edge/Chrome → address-bar
  Install icon → standalone desktop app.

## PACKAGING DISCIPLINE (every session)
1. `find . -name __pycache__ -type d -exec rm -rf {} +`; delete `*.pyc`; remove
   `node_modules/`, `dist/`, `release/`, `gods_core.db`, `storage/`.
2. Rebuild `_packages/<system>.zip` for each top-level system (exclude the heavy dirs).
3. `zip -rq /mnt/user-data/outputs/GODS_ECOSYSTEM.zip GODS_ECOSYSTEM -x "*/node_modules/*" ...`.
4. Copy updated `00_*` docs + `render.yaml` into `/mnt/user-data/outputs/GODS_ECOSYSTEM/`.
5. `present_files` the zip + the doc(s) changed.
6. **Verify from a CLEAN extraction** (`/tmp/fvX`) — run `smoke_test.py` (expect 34/34).

## DOMAIN TERMS (use precisely)
EVA engine (6-D: risk, compliance, stability, disparate_impact, spd, ecs → SVS); sovereignty
(SVS=min, non-bypassable); HITL / oversight cases (Pillar VIII); fail-closed; Merkle-linked /
hash-chained immutable audit; HSM dual-custody (emulated deterministic key); SETHS→TS→UDOC→MADIBA
loop; Constitutional Pillars (II capital recycle >50%, VIII human primacy); HQ-OS; SAQA 118707 NQF5.

## STANCE TO KEEP
Honest, verifiable, deployed. Build up to the user's-machine line (git push, signed compile,
on-silicon) and stop there truthfully. Encourage the user to run commands themselves and verify
against you — they want to become a capable developer that AI accelerates, not a button-presser.
Update `00_PROGRESS.md` every session. Never claim capability that isn't tested.
