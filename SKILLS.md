# SKILLS.md — how to continue the UDOC build (methods that work here)

## Golden rules
- **Backend persists only within ONE bash call.** Always start uvicorn AND run the test/seed in the *same* `bash_tool` command; it's gone next call.
- **Overwrite existing files** with `cat > path << 'EOF'` (quoted heredoc) or `str_replace`; `create_file` errors if the file exists. Heredoc content must NOT contain a literal `</` + `parameter>` token (JSX `</div>` is fine).
- Keep everything **honest** (see MEMORY.md) and **cockpit-branded** (navy/gold/purple/cyan).

## Run + verify the live system (one shell)
```bash
cd platform-core && rm -f gods_core.db && python3 seed.py >/dev/null 2>&1
nohup python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8077 >/tmp/uv.log 2>&1 & UV=$!
sleep 6
# ... httpx or playwright tests here ...
kill $UV 2>/dev/null
```
Auth: `POST /auth/login` (form) → `access_token`; send `Authorization: Bearer`.

## Build/verify a React app (udoc-app / platform-internal)
```bash
cd udoc-app && npm install --no-audit --no-fund --silent && npm run build   # tsc + vite; catches type errors
```
TS style is lenient (`any` everywhere) — match it. udoc-app has no router (tab state); platform-internal uses react-router + `/api` proxy.

## Update the mobile app
`udoc-mobile` wraps `udoc-app`'s build. To refresh it: `cd udoc-app && npm run build && rm -rf ../udoc-mobile/www && cp -r dist/* ../udoc-mobile/www/`. APK build (needs Android SDK/JDK17): `udoc-mobile/build-apk.sh`.

## Playwright smoke (drives the real UI against the backend)
```python
from playwright.sync_api import sync_playwright
# launch chromium args=["--no-sandbox"]; phone viewport {"width":402,"height":880}
# goto served www/dist; fill connect URL→backend; fill #gl/password; click Sign in
# drive tabs/buttons by text: pg.eval_on_selector_all(".tabs button","bs=>{const x=bs.find(b=>/EVA/.test(b.textContent));x&&x.click();}")
# file upload: pg.set_input_files("input[type=file]","/tmp/sample_ai_act.docx")
# assert via pg.evaluate(...)
```
Serve static: `python3 -m http.server PORT --directory <dir>`.

## Wire a new live page (pattern used throughout)
1. Backend endpoint returns clean JSON (check shape with httpx first).
2. udoc-app: add a tab to `SwTab`/`HwTab` + the `SW`/`HW` array; add state; fetch in `refresh()` (Promise.all or fire-and-forget); render; for writes use `api.post/patch`.
3. HTML cockpit: in `_live_bridge.html`, add a `render*()` that fills the page's `tbody`/KPIs (bind KPIs by label via `setKpi`), call it from `refreshAll()`; re-inject bridge before `</body>` of the demo to rebuild `GODS_Admin_Live.html`; copy to `platform-core/static/admin.html`.

## Policy-to-Code engine (extend it)
- Rule kinds + enforcement live in `app/services/policy_engine.py` (`_RULES` patterns → kinds; `apply()` logic). Add a kind: add a regex row + an `elif r.kind==...` branch in `apply()`.
- Extraction is intentionally **assistive + human-reviewed**; rules are editable via `PATCH /policy/rules/{id}` before `activate`. Don't claim auto-perfect legal NLP.
- Test end-to-end: build a DOCX with `python-docx`, `POST /policy/upload` (httpx `files=`), `/activate`, then `POST /decisions` and check `policy_findings`.

## Packaging
Clean first: `rm -rf */node_modules */dist *.db *.log`. Zip: `zip -rq OUT.zip . -x "*/node_modules/*" -x "*/.git/*" -x "*/dist/*" -x "*.tsbuildinfo"`. Deliver to `/mnt/user-data/outputs/`; `present_files` the zip + progress doc.

## G.O.D.S Intelligence (internal brain) — extend it
- Corpus + reasoning in `app/services/gods_intelligence.py`; internal-only router `app/routers/intel.py` (gate via `_gate(user, write=)`; client/viewer → 403). Add data via `/intel/ingest` (file) or `/intel/ingest-text`; remove via `DELETE /intel/docs/{id}` — both recompute corpus state. `ask()` is retrieval-grounded + citeable; keep it honest (no hallucination; "not in corpus"). Pillar VIII guardrail (`guardrail_check`) is non-overridable — never weaken it. Maturity stages 2–5 stay ROADMAP/gated; do NOT claim AGI/Singularity. Intelligence UI belongs in the ADMIN (platform-internal/cockpit), NOT the client udoc-app.
