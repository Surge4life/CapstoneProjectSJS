"""GODS Platform Core — FastAPI application entry point. Wires all division + UDOC routers."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
import os
from app.core.config import settings
from app.db.session import init_db
from app.routers import (health, auth, registry, decisions, audit, oversight,
                         seths, ts, madiba, compliance, bias, sovereignty,
                         intelligence, admin, analytics,
                         portal_student, portal_employer, portal_employee,
                         documents, saas, madiba_engage, ts_submit, access)

app = FastAPI(title=settings.app_name, version="1.0.0",
              description="Sovereign AI governance backend for the G.O.D.S ecosystem.")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"], allow_credentials=True)

_STATIC = os.path.join(os.path.dirname(__file__), "..", "static")


@app.middleware("http")
async def enforce_https(request: Request, call_next):
    # Render terminates TLS and passes X-Forwarded-Proto. Redirect plain HTTP to
    # HTTPS in production so admin JWT tokens are never transmitted in clear.
    if (settings.environment == "production"
            and request.headers.get("x-forwarded-proto") == "http"):
        url = request.url.replace(scheme="https")
        return RedirectResponse(url, status_code=301)
    return await call_next(request)


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/admin", tags=["root"], include_in_schema=False)
def admin_console():
    """Serve the live G.O.D.S Admin cockpit (HTML, same-origin, requires JWT login)."""
    return FileResponse(os.path.join(_STATIC, "admin.html"))


@app.get("/", tags=["root"])
def root():
    return {"system": "G.O.D.S Platform Core", "status": "live",
            "environment": settings.environment,
            "divisions": ["GODS", "SETHS", "MADIBA", "TS", "UDOC"],
            "governance": "EVA 6-D + UDOC sovereignty, fail-closed for critical"}


for r in (health.router, auth.router, registry.router, decisions.router, audit.router,
          oversight.router, seths.router, ts.router, madiba.router, compliance.router,
          bias.router, sovereignty.router, intelligence.router, admin.router, analytics.router,
          portal_student.router, portal_employer.router, portal_employee.router,
          documents.router, saas.router, madiba_engage.router, ts_submit.router,
          access.router):
    app.include_router(r)
