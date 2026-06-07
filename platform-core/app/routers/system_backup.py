"""System backup & restore — full, database-agnostic export and restore of the ENTIRE datastore.

Purpose: let an operator preserve every record before a hosting/database migration (for example a
free-tier Postgres that is about to expire and be deleted) and restore it, verifiably, into a fresh
empty database — SQLite or Postgres, any provider.

Design:
  * GET  /system/backup            -> one signed JSON bundle of every table (admin only).
  * POST /system/restore           -> load a bundle into THIS database (admin only).
       - seal is verified before anything is touched (override with ?skip_verify=true);
       - DRY-RUN by default (returns what it WOULD load); only ?confirm=true wipes + loads;
       - exact restore: primary keys preserved, tables loaded in FK-dependency order,
         Postgres id sequences/identities reset afterwards so new inserts don't collide.

Honesty note: the bundle contains password hashes and API-key hashes (so logins/keys survive a
restore). It is sensitive — store it securely. It is NOT a substitute for managed backups on a
paid plan; it is the portable, provider-independent safety net.
"""
from datetime import datetime
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy import select, text

from app.db.session import engine, Base, SessionLocal
from app.db import models  # noqa: F401 — ensure every table is registered on Base.metadata
from app.core.dependencies import current_user
from app.services.crypto_provider import sign, verify, provider_info

router = APIRouter(prefix="/system", tags=["system-backup"])

BACKUP_SCHEMA = "gods.backup/v1"


def _require_admin(user: dict) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="admin only")
    return user


def _enc(v):
    """JSON-encode a column value; datetimes are tagged so they round-trip exactly."""
    if isinstance(v, datetime):
        return {"__dt__": v.isoformat()}
    return v


def _dec(v):
    """Reverse _enc for restore."""
    if isinstance(v, dict) and "__dt__" in v:
        return datetime.fromisoformat(v["__dt__"])
    return v


def _canonical(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def build_backup() -> dict:
    """Serialise every table in FK-dependency order and seal the result."""
    data: dict = {}
    counts: dict = {}
    with engine.connect() as conn:
        for table in Base.metadata.sorted_tables:
            rows = [{k: _enc(v) for k, v in dict(m).items()}
                    for m in conn.execute(select(table)).mappings()]
            data[table.name] = rows
            counts[table.name] = len(rows)
    seal = sign(_canonical(data))
    return {
        "schema": BACKUP_SCHEMA,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": {"crypto": provider_info(), "tables": len(counts)},
        "counts": counts,
        "total_rows": sum(counts.values()),
        "data": data,
        "seal": seal,
        "seal_note": "HMAC-SHA256 (PQC/Dilithium-ref) over canonical(data). Verify on restore with the SAME GODS_SOV_KEY.",
    }


@router.get("/backup", summary="Export the entire datastore as one signed JSON bundle (admin)")
def backup(user: dict = Depends(current_user)):
    _require_admin(user)
    return build_backup()


@router.get("/backup/summary", summary="Row counts per table without exporting the data (admin)")
def backup_summary(user: dict = Depends(current_user)):
    _require_admin(user)
    counts = {}
    with engine.connect() as conn:
        for table in Base.metadata.sorted_tables:
            counts[table.name] = conn.execute(
                text(f"SELECT COUNT(*) FROM {table.name}")  # noqa: S608 — table.name is from our own metadata
            ).scalar()
    return {"tables": len(counts), "counts": counts, "total_rows": sum(counts.values()),
            "dialect": engine.dialect.name}


@router.post("/restore", summary="Restore a backup bundle into THIS database (admin; dry-run unless confirm=true)")
def restore(bundle: dict = Body(...),
            confirm: bool = Query(False, description="WIPE current data and load the bundle"),
            skip_verify: bool = Query(False, description="Skip seal verification (NOT recommended)"),
            user: dict = Depends(current_user)):
    _require_admin(user)
    if bundle.get("schema") != BACKUP_SCHEMA:
        raise HTTPException(status_code=400, detail=f"unrecognised backup schema (expected {BACKUP_SCHEMA})")
    data = bundle.get("data") or {}

    seal_ok = None
    if not skip_verify:
        seal_ok = verify(_canonical(data), bundle.get("seal", ""))
        if not seal_ok:
            raise HTTPException(status_code=400,
                                detail="seal verification FAILED — refusing restore. "
                                       "If you intentionally changed GODS_SOV_KEY, re-run with ?skip_verify=true")

    would = {t: len(rows) for t, rows in data.items()}
    if not confirm:
        return {"dry_run": True, "seal_verified": seal_ok, "schema": bundle.get("schema"),
                "generated_at": bundle.get("generated_at"), "would_restore": would,
                "total_rows": sum(would.values()), "target_dialect": engine.dialect.name,
                "note": "Nothing changed. Re-call with ?confirm=true to WIPE current data and load this bundle."}

    sorted_tables = list(Base.metadata.sorted_tables)
    dialect = engine.dialect.name
    db = SessionLocal()
    try:
        # 1) wipe — children first (reverse FK-dependency order)
        for table in reversed(sorted_tables):
            db.execute(table.delete())
        # 2) load — parents first; preserve primary keys; drop unknown columns defensively
        loaded = {}
        for table in sorted_tables:
            rows = data.get(table.name) or []
            if rows:
                cols = set(c.name for c in table.columns)
                clean = [{k: _dec(v) for k, v in r.items() if k in cols} for r in rows]
                db.execute(table.insert(), clean)
            loaded[table.name] = len(rows)
        db.commit()
        # 3) Postgres only — realign id sequences/identities to MAX(id)
        seq_reset = 0
        if dialect == "postgresql":
            for table in sorted_tables:
                if "id" not in (c.name for c in table.columns):
                    continue
                try:
                    seq = db.execute(text("SELECT pg_get_serial_sequence(:t, 'id')"),
                                     {"t": table.name}).scalar()
                    if seq:
                        db.execute(text(f"SELECT setval('{seq}', (SELECT COALESCE(MAX(id), 1) FROM {table.name}))"))
                    else:  # IDENTITY column (SQLAlchemy 2.0 default on Postgres)
                        mx = db.execute(text(f"SELECT COALESCE(MAX(id), 0) FROM {table.name}")).scalar() or 0
                        db.execute(text(f'ALTER TABLE "{table.name}" ALTER COLUMN id RESTART WITH {mx + 1}'))
                    seq_reset += 1
                except Exception:
                    db.rollback()  # best-effort; one table's reset failing must not abort the rest
            db.commit()
        return {"restored": True, "seal_verified": seal_ok, "dialect": dialect,
                "loaded": loaded, "total_rows": sum(loaded.values()),
                "sequences_realigned": seq_reset}
    finally:
        db.close()
