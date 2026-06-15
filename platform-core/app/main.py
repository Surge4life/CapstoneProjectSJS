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
                         system_backup, users_admin, client_knowledge, workspace)

app = FastAPI(title=settings.app_name, version="1.0.0",
              description="Sovereign AI governance backend for the G.O.D.S ecosystem.")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"], allow_credentials=False)


@app.middleware("http")
async def enforce_https(request: Request, call_next):
    """Redirect HTTP → HTTPS in production. Checks X-Forwarded-Proto set by Render's proxy;
    health-check and internal traffic (no header) pass through unchanged."""
    if (os.environ.get("ENVIRONMENT") == "production"
            and request.headers.get("x-forwarded-proto") == "http"):
        https_url = str(request.url).replace("http://", "https://", 1)
        return RedirectResponse(https_url, status_code=301)
    return await call_next(request)


@app.on_event("startup")
def _startup():
    # Each step is guarded so a database/schema problem can NEVER crash boot — a dead app helps no one.
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


def _heal_schema():
    """Additively reconcile existing tables with the ORM models: ADD any columns the models declare
    that are missing from the live database. Idempotent; never drops or retypes a column. Lets a
    database created under an OLDER schema work without a manual migration and without data loss.
    (This is what was missing: a live table created before new columns were added.)"""
    from sqlalchemy import inspect as sa_inspect, text
    from app.db.session import engine, Base
    from app.db import models  # noqa: F401 — ensure all tables are registered on Base.metadata
    insp = sa_inspect(engine)
    existing = set(insp.get_table_names())
    dialect = engine.dialect.name
    added = 0
    for table in Base.metadata.sorted_tables:
        if table.name not in existing:
            continue  # brand-new table — create_all already built it with every column
        have = {c["name"] for c in insp.get_columns(table.name)}
        for col in table.columns:
            if col.name in have:
                continue
            try:
                coltype = col.type.compile(dialect=engine.dialect)
            except Exception:
                coltype = "TEXT"
            ine = "IF NOT EXISTS " if dialect == "postgresql" else ""
            ddl = f'ALTER TABLE "{table.name}" ADD COLUMN {ine}"{col.name}" {coltype}'
            d = getattr(col, "default", None)
            if d is not None and getattr(d, "is_scalar", False):  # backfill existing rows when sensible
                val = d.arg
                if isinstance(val, bool):
                    ddl += f" DEFAULT {'TRUE' if val else 'FALSE'}"
                elif isinstance(val, (int, float)):
                    ddl += f" DEFAULT {val}"
                elif isinstance(val, str):
                    ddl += " DEFAULT '" + val.replace("'", "''") + "'"
            try:
                with engine.begin() as conn:   # isolate each DDL so one failure can't abort the rest
                    conn.execute(text(ddl))
                added += 1
                print(f"[schema-heal] added {table.name}.{col.name}")
            except Exception as e:
                print(f"[schema-heal] skipped {table.name}.{col.name}: {str(e)[:120]}")
    if added:
        print(f"[schema-heal] reconciled {added} missing column(s)")


def _ensure_bootstrap_admin():
    """On a brand-new EMPTY database (e.g. just after a DB migration), create one admin so the
    operator can log in and run a restore. No-op the moment any user exists. A restore then
    replaces this with the real users from the backup bundle. Override creds via GODS_BOOTSTRAP_*."""
    from app.db.session import SessionLocal
    from app.db.models import User
    from app.core.security import hash_password
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            email = os.environ.get("GODS_BOOTSTRAP_EMAIL", "admin@gods.local")
            pw = os.environ.get("GODS_BOOTSTRAP_PASSWORD", "admin123")
            db.add(User(email=email, password_hash=hash_password(pw), role="admin", division="GODS"))
            db.commit()
            print(f"[bootstrap] empty database detected — created bootstrap admin '{email}'. "
                  f"Restore a backup or change this password immediately.")
    finally:
        db.close()


@app.get("/admin", tags=["root"], include_in_schema=False)
def admin_console():
    """Serve the live G.O.D.S Admin cockpit (HTML UI wired to this API, same-origin)."""
    return FileResponse(os.path.join(os.path.dirname(__file__), "..", "static", "admin.html"))


@app.get("/udoc-admin", tags=["root"], include_in_schema=False)
def udoc_admin_console():
    """Serve the self-contained UDOC v9.3 admin console (same-origin, wired to this API)."""
    return FileResponse(os.path.join(os.path.dirname(__file__), "..", "static", "udoc_admin_v93.html"))


@app.get("/", tags=["root"])
def root():
    return {"system": "G.O.D.S Platform Core", "status": "live",
            "environment": settings.environment,
            "divisions": ["GODS", "SETHS", "MADIBA", "TS", "UDOC"],
            "governance": "EVA 6-D + UDOC sovereignty, fail-closed for critical"}


@app.get("/system/crypto", tags=["root"])
def system_crypto():
    from app.services.crypto_provider import provider_info
    return provider_info()


@app.get("/version", tags=["root"])
def version():
    """Build identity — commit/branch come from Render's git env on deploy (GitHub main -> Render)."""
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
          system_backup.router, users_admin.router, client_knowledge.router, workspace.router):
    app.include_router(r)
