"""24/7 Continuous Conformance API — heartbeat, trigger, findings, per-system state, scan log."""
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.core.dependencies import current_user, require_role
from app.db.session import get_db
from app.db.models import ConformanceScan, ConformanceFinding, AIModel
from app.services import conformance_scanner as cs

router = APIRouter(prefix="/conformance", tags=["Conformance"])


@router.get("/status", summary="24/7 scanner heartbeat + latest conformance posture")
def status(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    total = db.execute(select(func.count(AIModel.id))).scalar() or 0
    last = db.execute(select(ConformanceScan).order_by(ConformanceScan.created_at.desc()).limit(1)).scalar_one_or_none()
    hb = cs.HEARTBEAT
    out = {"scanner_enabled": hb["enabled"], "interval_min": hb["interval_min"], "runs": hb["runs"],
           "last_scan_at": hb["last_scan_at"], "next_scan_at": hb["next_scan_at"],
           "registered_systems": total, "floors": cs.THRESH}
    if last:
        out.update({"last_scan_ref": last.scan_ref, "scanned": last.total, "conformant": last.conformant,
                    "review": last.review, "non_conformant": last.non_conformant,
                    "unverified": last.unverified, "coverage_pct": last.coverage_pct,
                    "last_duration_ms": last.duration_ms})
    return out


@router.post("/scan", summary="Run a full conformance pass now (admin/exec, or Render Cron)")
def trigger(db: Session = Depends(get_db), user: dict = Depends(require_role("admin", "exec"))):
    return cs.scan_all(db, trigger="MANUAL")


@router.get("/systems", summary="Current conformance state of every registered system")
def systems(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    models = db.execute(select(AIModel)).scalars().all()
    out = []
    for m in models:
        f = db.execute(
            select(ConformanceFinding).where(ConformanceFinding.model_id == m.model_id)
            .order_by(ConformanceFinding.created_at.desc()).limit(1)
        ).scalar_one_or_none()
        out.append({"model_id": m.model_id, "name": m.name, "risk_tier": m.risk_tier, "status": m.status,
                    "verdict": f.verdict if f else "—", "state": f.state if f else "UNVERIFIED",
                    "last_svs": f.last_svs if f else None, "sovereign": f.sovereign if f else None,
                    "reason": f.reason if f else "Not yet scanned", "remediation": f.remediation if f else "",
                    "verified_at": f.created_at.isoformat() if (f and f.created_at) else None})
    return out


@router.get("/findings", summary="Recent conformance findings across scans")
def findings(limit: int = 50, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    rows = db.execute(
        select(ConformanceFinding).order_by(ConformanceFinding.created_at.desc()).limit(min(limit, 200))
    ).scalars().all()
    return [{"scan_ref": r.scan_ref, "model_id": r.model_id, "name": r.name, "verdict": r.verdict,
             "state": r.state, "reason": r.reason, "last_svs": r.last_svs, "sovereign": r.sovereign,
             "block_rate": r.block_rate, "recent_count": r.recent_count, "remediation": r.remediation,
             "at": r.created_at.isoformat() if r.created_at else None} for r in rows]


@router.get("/scans", summary="Scan history (the auditable heartbeat log)")
def scans(limit: int = 30, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    rows = db.execute(
        select(ConformanceScan).order_by(ConformanceScan.created_at.desc()).limit(min(limit, 100))
    ).scalars().all()
    return [{"scan_ref": r.scan_ref, "trigger": r.trigger, "total": r.total, "conformant": r.conformant,
             "review": r.review, "non_conformant": r.non_conformant, "unverified": r.unverified,
             "coverage_pct": r.coverage_pct, "duration_ms": r.duration_ms, "audit_seq": r.audit_seq,
             "at": r.created_at.isoformat() if r.created_at else None} for r in rows]


@router.post("/control", summary="Control the 24/7 scanner: scan | pause | resume | set_interval")
def control(payload: dict = Body(...), db: Session = Depends(get_db), user: dict = Depends(require_role("admin","exec"))):
    a = (payload.get("action") or "").lower()
    if a == "scan": return {"action": "scan", **cs.scan_all(db, trigger="MANUAL")}
    if a == "pause": return {"action": "pause", **cs.set_enabled(False)}
    if a == "resume": return {"action": "resume", **cs.set_enabled(True)}
    if a == "set_interval": return {"action": "set_interval", **cs.set_interval(payload.get("interval_min", 15))}
    raise HTTPException(400, "action must be scan|pause|resume|set_interval")
