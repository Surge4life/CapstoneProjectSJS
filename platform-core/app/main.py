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
        from app.services.conformance_scanner import start_scheduler
        start_scheduler()
    except Exception as e:
        print(f"[startup] conformance scanner not started: {e}")


def _heal_schema():
    from sqlalchemy import inspect as sa_inspect, text
    from app.db.session import engine, Base
    from app.db import models  # noqa: F401
    insp = sa_inspect(engine)
    existing = set(insp.get_table_names())
    dialect = engine.dialect.name
    for table in Base.metadata.sorted_tables:
        if table.name not in existing:
            continue
        have = {c["name"] for c in insp.get_columns(table.name)}
        for col in table.columns:
            if col.name in have:
                continue
            try:
                coltype = col.type.compile(dialect=engine.dialect)
            except Exception:
                coltype = "TEXT"
            ine = "IF NOT EXISTS " if dialect == "postgresql" else ""
            try:
                with engine.begin() as conn:
                    conn.execute(text(f'ALTER TABLE "{table.name}" ADD COLUMN {ine}"{col.name}" {coltype}'))
            except Exception as e:
                print(f"[heal] {table.name}.{col.name}: {e}")


def _ensure_bootstrap_admin():
    from sqlalchemy import select
    from app.db.session import SessionLocal
    from app.db.models import User
    from app.core.security import hash_password
    db = SessionLocal()
    try:
        u = db.execute(select(User).where(User.email == "admin@gods.local")).scalar_one_or_none()
        if not u:
            return
    finally:
        db.close()


def _ensure_udoc_demo_seed():
    pass


def _ensure_client_kb_demo_seed():
    pass


def _static(name: str):
    base = os.path.join(os.path.dirname(__file__), "..", "static")
    return os.path.abspath(os.path.join(base, name))


@app.get("/admin", tags=["root"], include_in_schema=False)
def admin_console():
    return FileResponse(_static("admin.html"))


@app.get("/udoc-admin", tags=["root"], include_in_schema=False)
def udoc_admin_console():
    return FileResponse(_static("udoc_admin_v93.html"))


@app.get("/portals", tags=["root"], include_in_schema=False)
def portals_console():
    return FileResponse(_static("portals.html"))


@app.get("/Sentinel", tags=["root"], include_in_schema=False)
@app.get("/sentinel", tags=["root"], include_in_schema=False)
def sentinel_console():
    return FileResponse(_static("sentinel.html"))


@app.get("/", tags=["root"])
def root():
    return {"system": "G.O.D.S Platform Core", "status": "live",
            "environment": settings.environment,
            "divisions": ["GODS", "SETHS", "MADIBA", "TS", "UDOC"],
            "surfaces": {"admin": "/admin", "udoc_admin": "/udoc-admin",
                         "portals": "/portals", "sentinel": "/Sentinel"},
            "governance": "EVA 6-D + policy-to-code + conformance, fail-closed for critical"}


@app.get("/system/crypto", tags=["root"])
def system_crypto():
    from app.services.crypto_provider import provider_info
    return provider_info()


@app.get("/version", tags=["root"])
def version():
    return {"service": "platform-core", "environment": settings.environment,
            "commit": os.environ.get("RENDER_GIT_COMMIT", "dev")[:12],
            "branch": os.environ.get("RENDER_GIT_BRANCH", "local"),
            "deployed_at": os.environ.get("RENDER_RELEASE_CREATED_AT", "")}


for r in (health.router, auth.router, registry.router, decisions.router, audit.router,
          oversight.router, seths.router, ts.router, madiba.router, compliance.router,
          bias.router, sovereignty.router, intelligence.router, admin.router, analytics.router,
          portal_student.router, portal_employer.router, portal_employee.router,
          documents.router, saas.router, madiba_engage.router, ts_submit.router,
          access.router, policy.router, intel.router, tenants.router, admin_udoc.router,
          system_backup.router, users_admin.router, client_knowledge.router, workspace.router, sectors.router, rbac.router, portal_ops.router, conformance.router,
          manifest.router, udoc_engine.router, staychain.router, enclave.router,
          gis.router, citizen.router, eif.router):
    app.include_router(r)
