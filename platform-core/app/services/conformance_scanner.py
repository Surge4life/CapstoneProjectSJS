"""
24/7 Continuous Conformance Scanner
═══════════════════════════════════
A standing watch over every registered AI system. Registration is a snapshot; conformance is continuous.
On every pass this scanner re-verifies each system in the registry against the EVA mandatory floors
(sovereignty, SVS, risk tier, drift/regression) using the system's *observed* decision telemetry — never
synthetic readings — and auto-remediates any regression:

    NON_CONFORMANT → status SUSPENDED + oversight case opened + sealed audit record
    REVIEW         → oversight case opened + sealed audit record
    UNVERIFIED     → flagged (registered but no recent telemetry to attest) + sealed audit
    CONFORMANT     → counted under the per-scan heartbeat seal

This is the post-market monitoring layer (EU AI Act Art. 72 intent; SA NAIFP continuous oversight) and it
produces an auditable liveness heartbeat proving the governance system is actively watching.
"""
import os, time, uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import AIModel, Decision, OversightCase, ConformanceScan, ConformanceFinding
from app.services.audit_writer import append_audit

# Conformance floors mirror the EVA engine's mandatory blocks (governance_bridge.THRESH); env-overridable.
THRESH = {
    "svs_floor":      float(os.getenv("CONFORMANCE_SVS_FLOOR", "0.60")),
    "svs_review":     float(os.getenv("CONFORMANCE_SVS_REVIEW", "0.75")),
    "block_rate_fail":float(os.getenv("CONFORMANCE_BLOCK_RATE", "0.50")),
    "stale_hours":    float(os.getenv("CONFORMANCE_STALE_HOURS", "24")),
    "recent_window":  int(os.getenv("CONFORMANCE_WINDOW", "20")),
}
INTERVAL_MIN = int(os.getenv("CONFORMANCE_INTERVAL_MIN", "15"))

# in-process liveness heartbeat (durable history lives in conformance_scans)
HEARTBEAT = {"enabled": False, "interval_min": INTERVAL_MIN, "last_scan_at": None,
             "last_scan_ref": None, "next_scan_at": None, "runs": 0}


def _now():
    return datetime.now(timezone.utc)


def _aware(dt):
    return dt if (dt and dt.tzinfo) else (dt.replace(tzinfo=timezone.utc) if dt else None)


def _recent(db, model):
    return db.execute(
        select(Decision).where(Decision.model_pk == model.id)
        .order_by(Decision.created_at.desc()).limit(THRESH["recent_window"])
    ).scalars().all()


def scan_model(db, model) -> dict:
    """Re-verify one registered system against the EVA conformance floors from its observed telemetry."""
    decs = _recent(db, model)
    n = len(decs)
    last = decs[0] if decs else None
    last_svs = float(last.svs) if last else 0.0
    sovereign_now = bool(last.sovereign) if last else True
    last_seen = _aware(last.created_at) if last else None
    block_rate = (sum(1 for d in decs if d.decision == "BLOCK") / n) if n else 0.0
    tier = (model.risk_tier or "").upper()

    verdict, reason = "PASS", "Conformant — within all EVA floors"
    if tier == "UNACCEPTABLE":
        verdict, reason = "FAIL", "Prohibited risk tier (UNACCEPTABLE) — permanent block (SA NAIFP)"
    elif n == 0:
        verdict, reason = "STALE", "Registered but never evaluated — conformance cannot be attested"
    elif last_seen and (_now() - last_seen) > timedelta(hours=THRESH["stale_hours"]):
        hrs = (_now() - last_seen).total_seconds() / 3600
        verdict, reason = "STALE", f"No telemetry in {hrs:.0f}h (> {THRESH['stale_hours']:.0f}h SLA) — unverified"
    elif not sovereign_now:
        verdict, reason = "FAIL", "Sovereignty breach on latest decision (SVS<1.0) — POPIA s.72"
    elif last_svs < THRESH["svs_floor"]:
        verdict, reason = "FAIL", f"SVS {last_svs:.3f} < {THRESH['svs_floor']:.2f} sovereign-validation floor"
    elif block_rate >= THRESH["block_rate_fail"]:
        verdict, reason = "FAIL", f"Block rate {block_rate:.0%} ≥ {THRESH['block_rate_fail']:.0%} — systemic regression"
    elif last_svs < THRESH["svs_review"]:
        verdict, reason = "WARN", f"SVS {last_svs:.3f} < {THRESH['svs_review']:.2f} — review advised"

    state = {"PASS": "CONFORMANT", "WARN": "REVIEW", "FAIL": "NON_CONFORMANT", "STALE": "UNVERIFIED"}[verdict]
    return {"model": model, "model_id": model.model_id, "name": model.name, "verdict": verdict,
            "state": state, "reason": reason, "last_svs": round(last_svs, 4), "sovereign": sovereign_now,
            "block_rate": round(block_rate, 3), "recent_count": n}


def _open_case(db, model_id, reason) -> str:
    existing = db.execute(
        select(OversightCase).where(
            OversightCase.model_id == model_id,
            OversightCase.state.in_(("OPEN", "REVIEWING")),
            OversightCase.reason.like("Conformance:%"))
    ).scalars().first()
    if existing:
        return existing.case_ref
    ref = "OVS-" + uuid.uuid4().hex[:8].upper()
    db.add(OversightCase(case_ref=ref, model_id=model_id, reason=("Conformance: " + reason)[:200],
                         state="OPEN", assigned_to="conformance-scanner"))
    db.commit()
    return ref


def remediate(db, f) -> str:
    """Auto-remediate a finding via the real status / oversight / audit machinery."""
    model, verdict = f["model"], f["verdict"]
    actions = []
    if verdict == "FAIL":
        if model.status != "SUSPENDED":
            model.status = "SUSPENDED"; db.add(model); db.commit(); actions.append("status→SUSPENDED")
        actions.append("oversight " + _open_case(db, f["model_id"], f["reason"]))
        ev = "CONFORMANCE_BLOCK"
    elif verdict == "WARN":
        actions.append("oversight " + _open_case(db, f["model_id"], f["reason"]))
        ev = "CONFORMANCE_REVIEW"
    elif verdict == "STALE":
        actions.append("flagged unverified"); ev = "CONFORMANCE_STALE"
    else:
        ev = None
    if ev:
        append_audit(db, ev, {"model_id": f["model_id"], "verdict": verdict, "reason": f["reason"],
                              "svs": f["last_svs"], "sovereign": f["sovereign"]},
                     classification="GOVERNANCE", actor_class="CONFORMANCE_SCANNER")
    return "; ".join(actions) if actions else "none"


def scan_all(db: Session, trigger: str = "SCHEDULED") -> dict:
    """One full 24/7 conformance pass over every registered system."""
    t0 = time.perf_counter()
    ref = "CSCAN-" + uuid.uuid4().hex[:8].upper()
    models = db.execute(select(AIModel)).scalars().all()
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "STALE": 0}
    for m in models:
        f = scan_model(db, m)
        rem = remediate(db, f)
        counts[f["verdict"]] += 1
        db.add(ConformanceFinding(
            scan_ref=ref, model_id=f["model_id"], name=f["name"], verdict=f["verdict"], state=f["state"],
            reason=f["reason"], last_svs=f["last_svs"], sovereign=f["sovereign"],
            block_rate=f["block_rate"], recent_count=f["recent_count"], remediation=rem))
    total = len(models)
    verified = counts["PASS"] + counts["WARN"] + counts["FAIL"]
    coverage = round(100.0 * verified / total, 1) if total else 100.0
    dur = round((time.perf_counter() - t0) * 1000, 1)
    summary = {"total": total, "conformant": counts["PASS"], "review": counts["WARN"],
               "non_conformant": counts["FAIL"], "unverified": counts["STALE"], "coverage_pct": coverage}
    seal = append_audit(db, "CONFORMANCE_SCAN", {**summary, "ref": ref, "trigger": trigger},
                        classification="GOVERNANCE", actor_class="CONFORMANCE_SCANNER")
    db.add(ConformanceScan(scan_ref=ref, trigger=trigger, total=total, conformant=counts["PASS"],
           review=counts["WARN"], non_conformant=counts["FAIL"], unverified=counts["STALE"],
           coverage_pct=coverage, duration_ms=dur, audit_seq=seal.seq))
    db.commit()
    HEARTBEAT.update({"last_scan_at": _now().isoformat(), "last_scan_ref": ref,
                      "next_scan_at": (_now() + timedelta(minutes=INTERVAL_MIN)).isoformat(),
                      "runs": HEARTBEAT["runs"] + 1})
    return {"scan_ref": ref, "trigger": trigger, "duration_ms": dur, "audit_seq": seal.seq, **summary}


_scheduler = None
def start_scheduler():
    """Start the in-process 24/7 loop (APScheduler). Render Cron can also drive POST /conformance/scan."""
    global _scheduler
    if _scheduler is not None:
        return
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from app.db.session import SessionLocal

        def _job():
            db = SessionLocal()
            try:
                scan_all(db, trigger="SCHEDULED")
            except Exception as e:
                print(f"[conformance] scan error: {e}")
            finally:
                db.close()

        boot = os.getenv("CONFORMANCE_BOOT_SCAN", "1") == "1"
        _scheduler = BackgroundScheduler(daemon=True)
        _scheduler.add_job(_job, "interval", minutes=INTERVAL_MIN, id="conformance_scan",
                           next_run_time=(datetime.now() if boot else None))
        _scheduler.start()
        HEARTBEAT["enabled"] = True
        HEARTBEAT["next_scan_at"] = (_now() + timedelta(minutes=INTERVAL_MIN)).isoformat()
        print(f"[conformance] 24/7 scanner started — every {INTERVAL_MIN} min")
    except Exception as e:
        print(f"[conformance] scheduler not started: {e}")


# -- live control surface (pause / resume / cadence) --
def set_enabled(on: bool) -> dict:
    HEARTBEAT["enabled"] = bool(on)
    if _scheduler is not None:
        try:
            if on:
                _scheduler.resume_job("conformance_scan")
                HEARTBEAT["next_scan_at"] = (_now() + timedelta(minutes=INTERVAL_MIN)).isoformat()
            else:
                _scheduler.pause_job("conformance_scan"); HEARTBEAT["next_scan_at"] = None
        except Exception as e:
            return {"enabled": HEARTBEAT["enabled"], "error": str(e)}
    return {"enabled": HEARTBEAT["enabled"], "next_scan_at": HEARTBEAT["next_scan_at"]}


def set_interval(minutes) -> dict:
    global INTERVAL_MIN
    try:
        minutes = max(1, min(1440, int(minutes)))
    except Exception:
        return {"error": "interval_min must be an integer (minutes)"}
    INTERVAL_MIN = minutes; HEARTBEAT["interval_min"] = minutes
    if _scheduler is not None and HEARTBEAT["enabled"]:
        try:
            _scheduler.reschedule_job("conformance_scan", trigger="interval", minutes=minutes)
            HEARTBEAT["next_scan_at"] = (_now() + timedelta(minutes=minutes)).isoformat()
        except Exception as e:
            return {"interval_min": minutes, "error": str(e)}
    return {"interval_min": minutes, "next_scan_at": HEARTBEAT["next_scan_at"]}
