"""
UDOC Analytics Engine — turns recorded division events into queryable analytics.
This is the 'data record and analytics' UDOC provides to SETHS, MADIBA, and TS:
record an event once, then derive time-series, totals, rates, and KPIs from it.
Dev: SQL aggregation over DivisionRecord. Prod: same queries against Postgres +
OpenSearch indices (interface identical).
"""
from collections import defaultdict
from datetime import datetime, timezone
import json
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.models import DivisionRecord


def record(db: Session, division: str, event_type: str, entity_ref: str = "",
           metric_name: str = "", metric_value: float = 0.0, period: str = "",
           meta: dict | None = None) -> DivisionRecord:
    """Capture one division event into the UDOC record store."""
    if not period:
        period = datetime.now(timezone.utc).strftime("%Y-%m")
    r = DivisionRecord(division=division, event_type=event_type, entity_ref=entity_ref,
                       metric_name=metric_name, metric_value=metric_value, period=period,
                       meta=json.dumps(meta or {}))
    db.add(r); db.commit(); db.refresh(r)
    return r


def timeseries(db: Session, division: str, metric_name: str) -> list[dict]:
    """Monthly time-series of a metric (sum per period)."""
    rows = db.execute(
        select(DivisionRecord.period, func.sum(DivisionRecord.metric_value))
        .where(DivisionRecord.division == division, DivisionRecord.metric_name == metric_name)
        .group_by(DivisionRecord.period).order_by(DivisionRecord.period)
    ).all()
    return [{"period": p, "value": round(v or 0.0, 2)} for p, v in rows]


def totals(db: Session, division: str) -> dict:
    """Totals + event counts per metric/event for a division."""
    metric_rows = db.execute(
        select(DivisionRecord.metric_name, func.sum(DivisionRecord.metric_value),
               func.count(DivisionRecord.id))
        .where(DivisionRecord.division == division)
        .group_by(DivisionRecord.metric_name)
    ).all()
    event_rows = db.execute(
        select(DivisionRecord.event_type, func.count(DivisionRecord.id))
        .where(DivisionRecord.division == division)
        .group_by(DivisionRecord.event_type)
    ).all()
    return {
        "division": division,
        "metrics": {m or "_": {"sum": round(s or 0.0, 2), "count": c} for m, s, c in metric_rows},
        "events": {e: c for e, c in event_rows},
        "total_records": sum(c for _e, c in event_rows),
    }


def recent(db: Session, division: str, limit: int = 50) -> list[dict]:
    rows = db.execute(
        select(DivisionRecord).where(DivisionRecord.division == division)
        .order_by(DivisionRecord.id.desc()).limit(limit)
    ).scalars().all()
    return [{"id": r.id, "event_type": r.event_type, "entity_ref": r.entity_ref,
             "metric_name": r.metric_name, "metric_value": r.metric_value,
             "period": r.period, "created_at": r.created_at.isoformat()} for r in rows]


def kpis(db: Session, division: str) -> dict:
    """Division-specific KPIs derived from the record store."""
    t = totals(db, division)
    m = t["metrics"]
    if division == "SETHS":
        enrolled = m.get("enrolled", {}).get("sum", 0)
        placed = m.get("placed", {}).get("sum", 0)
        return {"enrolled": enrolled, "placed": placed,
                "placement_rate": round(placed / enrolled, 3) if enrolled else 0.0,
                "monthly_output": m.get("monthly_value", {}).get("sum", 0)}
    if division == "MADIBA":
        inflow = m.get("inflow", {}).get("sum", 0)
        recycled = m.get("recycled", {}).get("sum", 0)
        return {"total_inflow": inflow, "total_recycled": recycled,
                "recycle_ratio": round(recycled / inflow, 3) if inflow else 0.0}
    if division == "TS":
        rev = m.get("revenue", {}).get("sum", 0)
        profit = m.get("profit", {}).get("sum", 0)
        workers = m.get("workers", {}).get("sum", 0)
        return {"total_revenue": rev, "total_profit": profit, "workers_absorbed": workers,
                "avg_margin": round(profit / rev, 3) if rev else 0.0}
    return t
