"""GODS Platform Core — FastAPI application entry point. Wires all division + UDOC routes."""
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GODS Platform Core", version="9.3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _static(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "..", "static", name)


def _html_with_density(path: str):
    """Serve HTML and inject shared div-density.js (same pattern as admin-gods-live)."""
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
    """Additive GODS Admin density (constitutional + GBS + division nav)."""
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
    """UDOC internal controller — inject additive density script."""
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
@app.get("/eif-ui/", tags=["root"], include_in_schema=False)
def eif_ui_console():
    return _html_with_density(_static("eif.html"))


@app.get("/Sentinel", tags=["root"], include_in_schema=False)
@app.get("/sentinel", tags=["root"], include_in_schema=False)
def sentinel_console():
    return _html_with_density(_static("sentinel.html"))


@app.get("/", tags=["root"], include_in_schema=False)
def root():
    return RedirectResponse("/health")


# Routers wired at import / startup by platform package
try:
    from app.routers import (
        auth,
        health,
        decisions,
        udoc,
        policy,
        intel,
        oversight,
        citizen,
        eif,
        gis,
        seths,
        ts,
        madiba,
        portal,
        enclave,
    )
    for r in (
        auth.router,
        health.router,
        decisions.router,
        udoc.router,
        policy.router,
        intel.router,
        oversight.router,
        citizen.router,
        eif.router,
        gis.router,
        seths.router,
        ts.router,
        madiba.router,
        portal.router,
        enclave.router,
    ):
        app.include_router(r)
except Exception as _wire_err:
    # Fail-open for static surfaces; API may partially load depending on deploy
    import logging
    logging.getLogger("gods").warning("router wire partial: %s", _wire_err)


@app.on_event("startup")
async def _startup():
    try:
        from app.startup_seed import ensure_seeds
        ensure_seeds()
    except Exception:
        pass
