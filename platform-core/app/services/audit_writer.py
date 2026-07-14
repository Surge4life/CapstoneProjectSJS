"""
Immutable audit writer — hash-chained, Dilithium-signature-ref, Merkle-root capable.
Dev/emulation persists the chain head + refs in SQL (AuditRef); production additionally
streams full records to Cassandra/WORM per the hardware spec (10-year append-only).
"""
import hashlib
import threading
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.models import AuditRef

GENESIS = "0" * 64

# Audit appends must be serialized: the hash-chain head is read-modify-write.
# Process-level lock here; production uses a DB advisory lock / single-writer WORM partition
# (the spec's Cassandra audit design already centralises the writer).
_append_lock = threading.Lock()


def _hash(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


def append_audit(db: Session, event_type: str, payload: dict,
                 classification: str = "INTERNAL", actor_class: str = "SYSTEM",
                 dilithium_ref: str = "") -> AuditRef:
    """Append one immutable, hash-chained audit record. Serialized to protect the chain."""
    with _append_lock:
        return _append_locked(db, event_type, payload, classification, actor_class, dilithium_ref)


def _append_locked(db, event_type, payload, classification, actor_class, dilithium_ref):
    last = db.execute(select(AuditRef).order_by(AuditRef.seq.desc()).limit(1)).scalar_one_or_none()
    seq = (last.seq + 1) if last else 1
    prev = last.event_hash if last else GENESIS
    ts = datetime.now(timezone.utc).isoformat()
    body = _hash(event_type, str(sorted(payload.items())), ts, classification, actor_class)
    chained = _hash(prev, body)
    rec = AuditRef(seq=seq, event_type=event_type, event_hash=chained, prev_hash=prev,
                   dilithium_ref=dilithium_ref or f"dil-ref-{seq}",
                   classification=classification, actor_class=actor_class)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def verify_chain(db: Session) -> dict:
    """Walk the chain; confirm each record links to its predecessor."""
    rows = db.execute(select(AuditRef).order_by(AuditRef.seq.asc())).scalars().all()
    ok = True
    broken_at = None
    prev = GENESIS
    for r in rows:
        if r.prev_hash != prev:
            ok = False
            broken_at = r.seq
            break
        prev = r.event_hash
    return {"records": len(rows), "intact": ok, "broken_at": broken_at, "head": prev}


def merkle_root(db: Session) -> str:
    """Compute a Merkle root over all event hashes (published at fixed intervals per spec)."""
    leaves = [r.event_hash for r in
              db.execute(select(AuditRef).order_by(AuditRef.seq.asc())).scalars().all()]
    if not leaves:
        return GENESIS
    layer = leaves
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]
            b = layer[i + 1] if i + 1 < len(layer) else layer[i]
            nxt.append(_hash(a, b))
        layer = nxt
    return layer[0]
