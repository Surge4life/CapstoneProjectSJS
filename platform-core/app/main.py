"""GODS Platform Core — FastAPI application entry point. Wires all division + UDOC routers."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from app.division_surfaces import register_division_surfaces
import os
from app.core.config import settings
from app.db.session import init_db
from app.routers import (health, auth, registry, decisions, audit, oversight,
                         seths, ts, madiba, compliance, bias, sovereignty,
                         intelligence, admin, analytics,
                         portal_student, portal_employer, portal_employee,
                         documents, saas, madiba_engage, ts_submit, access, policy, intel, tenants, admin_udoc,
                         system_backup, users_admin, client_knowledge, workspace, sectors, rbac, portal_ops, conformance, manifest, udoc_engine, staychain, enclave,
                         gis, citizen, eif)

app = FastAPI(title=settings.app_name, version="1.0.0",
              description="Sovereign AI governance backend for the G.O.D.S ecosystem.")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"], allow_credentials=False)


@app.middleware("http")
async def enforce_https(request: Request, call_next):
    if (os.environ.get("ENVIRONMENT") == "production"
            and request.headers.get("x-forwarded-proto") == "http"):
        https_url = str(request.url).replace("http://", "https://", 1)
        return RedirectResponse(https_url, status_code=301)
    return await call_next(request)


@app.on_event("startup")
def _startup():
    try:
        init_db()
    except Exception as e:
        print(f"[startup] init_db error (continuing): {e}")
    try:
        _heal_schema()
    except Exception as e:
        print(f"[startup] schema-heal error (continuing): {e}")
    try:
        _heal_seths_learners()
    except Exception as e:
        print(f"[startup] seths-learners heal error (continuing): {e}")
    try:
        _ensure_bootstrap_admin()
    except Exception as e:
        print(f"[startup] bootstrap-admin skipped: {e}")
    try:
        _ensure_udoc_demo_seed()
    except Exception as e:
        print(f"[startup] udoc demo seed skipped: {e}")
    try:
        _ensure_client_kb_demo_seed()
    except Exception as e:
        print(f"[startup] client kb demo seed skipped: {e}")
    try:
        _ensure_division_staff_seed()
    except Exception as e:
        print(f"[startup] division staff seed skipped: {e}")
    try:
        from app.services.conformance_scanner import start_scheduler
        start_scheduler()
    except Exception as e:
        print(f"[startup] conformance scanner not started: {e}")


def _heal_seths_learners():
    """Ensure Capstone Learner columns exist on Neon (enrol 500 if missing)."""
    from sqlalchemy import text
    from app.db.session import engine
    cols = [
        ("cohort", "VARCHAR(24)", "'COHORT_1'"),
        ("stream", "VARCHAR(24)", "'DIGITAL_OPERATIONS'"),
        ("cetcte_stage", "VARCHAR(24)", "'STABILISATION'"),
        ("self_affirmation_json", "TEXT", "'{}'"),
        ("monthly_value", "DOUBLE PRECISION", "0"),
        ("nqf_level", "INTEGER", "5"),
        ("status", "VARCHAR(20)", "'ENROLLED'"),
        ("qualification", "VARCHAR(120)", "'Digital Operations & AI Literacy'"),
        ("created_at", "TIMESTAMP", "NOW()"),
    ]
    with engine.begin() as conn:
        existing = {r[0] for r in conn.execute(text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'seths_learners'"
        )).fetchall()}
        if not existing:
            print("[heal-seths] table seths_learners missing — init_db should create it")
            return
        for name, typ, default in cols:
            if name in existing:
                continue
            ddl = f'ALTER TABLE seths_learners ADD COLUMN IF NOT EXISTS "{name}" {typ} DEFAULT {default}'
            try:
                conn.execute(text(ddl))
                print(f"[heal-seths] added seths_learners.{name}")
            except Exception as e:
                print(f"[heal-seths] skip {name}: {e}")


def _static(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "..", "static", name)


def _html_with_density(path: str):
    """Serve HTML and inject shared div-density.js."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception:
        return FileResponse(path)
    tag = '<script src="/div-density.js" defer></script>'
    if "div-density.js" not in html:
        html = html.replace("</body>", tag + "\n</body>") if "</body>" in html else html + tag
    return HTMLResponse(html, media_type="text/html")


@app.get("/admin-gods-live.js", tags=["root"], include_in_schema=False)
def admin_gods_live_js():
    return FileResponse(_static("admin-gods-live.js"), media_type="application/javascript")


@app.get("/div-density.js", tags=["root"], include_in_schema=False)
def div_density_js():
    return FileResponse(_static("div-density.js"), media_type="application/javascript")


@app.get("/udoc-admin-density.js", tags=["root"], include_in_schema=False)
def udoc_admin_density_js():
    return FileResponse(_static("udoc-admin-density.js"), media_type="application/javascript")


@app.get("/verify-redteam-panel.js", tags=["root"], include_in_schema=False)
def verify_redteam_panel_js():
    """Capstone Verify · Red-Team operator panel (probes Core only)."""
    return FileResponse(_static("verify-redteam-panel.js"), media_type="application/javascript")


@app.get("/admin", tags=["root"], include_in_schema=False)
@app.get("/admin/", tags=["root"], include_in_schema=False)
def admin_console():
    path = _static("admin.html")
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception:
        return FileResponse(path)
    tag = '<script src="/admin-gods-live.js" defer></script>'
    if "admin-gods-live.js" not in html:
        html = html.replace("</body>", tag + "\n</body>") if "</body>" in html else html + tag
    return HTMLResponse(html, media_type="text/html")


@app.get("/udoc-admin", tags=["root"], include_in_schema=False)
@app.get("/udoc-admin/", tags=["root"], include_in_schema=False)
def udoc_admin_console():
    path = _static("udoc_admin_v93.html")
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception:
        return FileResponse(path)
    tag = '<script src="/udoc-admin-density.js" defer></script>\n<script src="/verify-redteam-panel.js" defer></script>'
    if "udoc-admin-density.js" not in html:
        html = html.replace("</body>", tag + "\n</body>") if "</body>" in html else html + tag
    elif "verify-redteam-panel.js" not in html:
        html = html.replace("</body>", '<script src="/verify-redteam-panel.js" defer></script>\n</body>') if "</body>" in html else html + '<script src="/verify-redteam-panel.js" defer></script>'
    return HTMLResponse(html, media_type="text/html")


@app.get("/portals", tags=["root"], include_in_schema=False)
@app.get("/portals/", tags=["root"], include_in_schema=False)
def portals_console():
    return _html_with_density(_static("portals.html"))


@app.get("/divisions", tags=["root"], include_in_schema=False)
@app.get("/divisions/", tags=["root"], include_in_schema=False)
def divisions_console():
    return _html_with_density(_static("divisions.html"))


@app.get("/seths", tags=["root"], include_in_schema=False)
@app.get("/seths/", tags=["root"], include_in_schema=False)
def seths_console():
    return _html_with_density(_static("seths.html"))


@app.get("/ts", tags=["root"], include_in_schema=False)
@app.get("/ts/", tags=["root"], include_in_schema=False)
def ts_console():
    return _html_with_density(_static("ts.html"))


@app.get("/madiba", tags=["root"], include_in_schema=False)
@app.get("/madiba/", tags=["root"], include_in_schema=False)
def madiba_console():
    return _html_with_density(_static("madiba.html"))


@app.get("/gbs", tags=["root"], include_in_schema=False)
@app.get("/gbs/", tags=["root"], include_in_schema=False)
@app.get("/holdings", tags=["root"], include_in_schema=False)
def gbs_console():
    return _html_with_density(_static("gbs.html"))


@app.get("/eif-ui", tags=["root"], include_in_schema=False)
def eif_ui_console():
    return _html_with_density(_static("eif.html"))


@app.get("/Sentinel", tags=["root"], include_in_schema=False)
@app.get("/sentinel", tags=["root"], include_in_schema=False)
def sentinel_console():
    return _html_with_density(_static("sentinel.html"))


# Register division surface helpers if present
try:
    register_division_surfaces(app, _static)
except Exception as e:
    print(f"[wire] division_surfaces: {e}")

# Include all routers
for r in (
    health.router, auth.router, registry.router, decisions.router, audit.router,
    oversight.router, seths.router, ts.router, madiba.router, compliance.router,
    bias.router, sovereignty.router, intelligence.router, admin.router,
    analytics.router, portal_student.router, portal_employer.router,
    portal_employee.router, documents.router, saas.router, madiba_engage.router,
    ts_submit.router, access.router, policy.router, intel.router, tenants.router,
    admin_udoc.router, system_backup.router, users_admin.router,
    client_knowledge.router, workspace.router, sectors.router, rbac.router,
    portal_ops.router, conformance.router, manifest.router, udoc_engine.router,
    staychain.router, enclave.router, gis.router, citizen.router, eif.router,
):
    app.include_router(r)


def _heal_schema():
    pass  # retained from production main; detailed heal in services if present


def _ensure_bootstrap_admin():
    pass


def _ensure_udoc_demo_seed():
    try:
        from app.startup_seed import ensure_udoc_demo_seed
        ensure_udoc_demo_seed()
    except Exception:
        pass


def _ensure_client_kb_demo_seed():
    try:
        from app.startup_seed import ensure_client_kb_demo_seed
        ensure_client_kb_demo_seed()
    except Exception:
        pass


def _ensure_division_staff_seed():
    try:
        from app.startup_seed import ensure_division_staff_seed
        ensure_division_staff_seed()
    except Exception:
        pass
