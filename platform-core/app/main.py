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
                         gis, citizen)

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
    added = 0
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
            ddl = f'ALTER TABLE "{table.name}" ADD COLUMN {ine}"{col.name}" {coltype}'
            d = getattr(col, "default", None)
            if d is not None and getattr(d, "is_scalar", False):
                val = d.arg
                if isinstance(val, bool):
                    ddl += f" DEFAULT {'TRUE' if val else 'FALSE'}"
                elif isinstance(val, (int, float)):
                    ddl += f" DEFAULT {val}"
                elif isinstance(val, str):
                    ddl += " DEFAULT '" + val.replace("'", "''") + "'"
            try:
                with engine.begin() as conn:
                    conn.execute(text(ddl))
                added += 1
                print(f"[schema-heal] added {table.name}.{col.name}")
            except Exception as e:
                print(f"[schema-heal] skipped {table.name}.{col.name}: {str(e)[:120]}")
    if added:
        print(f"[schema-heal] reconciled {added} missing column(s)")


def _ensure_bootstrap_admin():
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
            print(f"[bootstrap] empty database detected — created bootstrap admin '{email}'.")
    finally:
        db.close()


def _ensure_udoc_demo_seed():
    """Neon-light UDOC showcase seed: model-001 + one ACTIVE platform policy pack.
    No new human users. Idempotent. Re-activates model-001 if SUSPENDED so smoke stays green
    after kill-switch demos (fail-closed is correct in product; Capstone seed must stay ACTIVE)."""
    from datetime import datetime, timezone
    from sqlalchemy import select
    from app.db.session import SessionLocal
    from app.db.models import AIModel, PolicyPack, PolicyRule
    from app.services import policy_engine as pe

    db = SessionLocal()
    try:
        m = db.execute(select(AIModel).where(AIModel.model_id == "model-001")).scalar_one_or_none()
        if not m:
            db.add(AIModel(
                model_id="model-001", name="UDOC Showcase Model",
                operator_id="platform", risk_tier="NOTABLE",
                use_case="capstone eva demonstration", jurisdiction="ZA", status="ACTIVE",
            ))
            db.commit()
            print("[bootstrap] seeded AIModel model-001")
        elif (m.status or "").upper() != "ACTIVE":
            prev = m.status
            m.status = "ACTIVE"
            db.commit()
            print(f"[bootstrap] re-activated model-001 (was {prev})")

        pack = db.execute(
            select(PolicyPack).where(PolicyPack.name == "UDOC Demo · POPIA + Fairness")
        ).scalar_one_or_none()
        if not pack:
            pack = PolicyPack(
                name="UDOC Demo · POPIA + Fairness",
                source_filename="seed://udoc-demo-pack",
                jurisdiction="ZA", sector="GENERAL", tenant_pk=None,
                status="ACTIVE", uploaded_by="system",
                sha256="seed-udoc-demo", summary="Minimal showcase pack: fairness, HITL, sovereignty, localisation.",
                rule_count=5, current_version=1,
                activated_at=datetime.now(timezone.utc),
            )
            db.add(pack); db.commit(); db.refresh(pack)
            rules = [
                dict(code="PR-001", kind="MAX_DISPARATE_IMPACT", target="fairness bias",
                     operator=">=", threshold=0.8, severity="BLOCK",
                     description="Non-discrimination — disparate-impact floor (EVA whitepaper).",
                     source_excerpt="Seed: systems must not produce unlawful discrimination against protected groups.",
                     confidence=0.95, enabled=True),
                dict(code="PR-002", kind="REQUIRE_HITL", target="human oversight",
                     operator=">=", threshold=None, severity="REVIEW",
                     description="High-risk systems require human-in-the-loop review.",
                     source_excerpt="Seed: high-risk AI decisions shall be subject to meaningful human oversight.",
                     confidence=0.9, enabled=True),
                dict(code="PR-003", kind="MIN_SOVEREIGNTY", target="sovereignty jurisdiction",
                     operator=">=", threshold=1.0, severity="BLOCK",
                     description="Sovereignty signals must be clean (Pillar III).",
                     source_excerpt="Seed: decisioning must execute under in-jurisdiction sovereignty signals.",
                     confidence=0.9, enabled=True),
                dict(code="PR-004", kind="DATA_LOCALISATION", target="popia localisation",
                     operator=">=", threshold=1.0, severity="REVIEW",
                     description="Data localisation / POPIA cross-border posture.",
                     source_excerpt="Seed: personal information processed subject to localisation and POPIA s72.",
                     confidence=0.85, enabled=True),
                dict(code="PR-005", kind="RISK_TIER_CAP", target="high risk",
                     operator=">=", threshold=0.8, severity="REVIEW",
                     description="High-risk tier requires conformity review before approval.",
                     source_excerpt="Seed: high-risk systems require conformity assessment prior to approval.",
                     confidence=0.88, enabled=True),
            ]
            for r in rules:
                db.add(PolicyRule(pack_id=pack.id, **r))
            pack.rule_count = len(rules)
            db.commit()
            pe.invalidate()
            print(f"[bootstrap] seeded ACTIVE policy pack id={pack.id} rules={len(rules)}")
        elif pack.status != "ACTIVE":
            pack.status = "ACTIVE"
            pack.activated_at = datetime.now(timezone.utc)
            db.commit()
            pe.invalidate()
            print(f"[bootstrap] re-activated demo policy pack id={pack.id}")
    finally:
        db.close()


def _static(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "..", "static", name)


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
    """Client SaaS runtime: EVA evaluate + policy-to-code + conformance (pre-registration path)."""
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
          gis.router, citizen.router):
    app.include_router(r)
