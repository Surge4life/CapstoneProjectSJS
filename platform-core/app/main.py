"""GODS Platform Core — FastAPI application entry point. Wires all division + UDOC routers."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from app.core.config import settings
from app.db.session import init_db
from app.routers import (health, auth, registry, decisions, audit, oversight,
                         seths, ts, madiba, compliance, bias, sovereignty,
                         intelligence, admin, analytics,
                         portal_student, portal_employer, portal_employee,
                         documents, saas, madiba_engage, ts_submit, access, policy, intel, tenants)

app = FastAPI(title=settings.app_name, version="1.0.0",
              description="Sovereign AI governance backend for the G.O.D.S ecosystem.")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"], allow_credentials=True)


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/admin", tags=["root"], include_in_schema=False)
def admin_console():
    """Serve the live G.O.D.S Admin cockpit (HTML UI wired to this API, same-origin)."""
    return FileResponse(os.path.join(os.path.dirname(__file__), "..", "static", "admin.html"))


@app.get("/", tags=["root"])
def root():
    return {"system": "G.O.D.S Platform Core", "status": "live",
            "environment": settings.environment,
            "divisions": ["GODS", "SETHS", "MADIBA", "TS", "UDOC"],
            "governance": "EVA 6-D + UDOC sovereignty, fail-closed for critical"}


@app.get("/version", tags=["root"])
def version():
    """Build identity — commit/branch come from Render's git env on deploy (GitHub main -> Render)."""
    return {"service": "platform-core", "environment": settings.environment,
            "commit": os.environ.get("RENDER_GIT_COMMIT", "dev")[:12],
            "branch": os.environ.get("RENDER_GIT_BRANCH", "local"),
            "deployed_at": os.environ.get("RENDER_RELEASE_CREATED_AT", "")}


@app.get("/system/crypto", tags=["system"])
def system_crypto():
    """Active cryptographic provider — reports PQC availability, algorithm, HSM custody mode."""
    from app.services.crypto_provider import provider_info
    return provider_info()


for r in (health.router, auth.router, registry.router, decisions.router, audit.router,
          oversight.router, seths.router, ts.router, madiba.router, compliance.router,
          bias.router, sovereignty.router, intelligence.router, admin.router, analytics.router,
          portal_student.router, portal_employer.router, portal_employee.router,
          documents.router, saas.router, madiba_engage.router, ts_submit.router,
          access.router, policy.router, intel.router, tenants.router):
    app.include_router(r)
