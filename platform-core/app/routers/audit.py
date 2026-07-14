"""Immutable audit — chain verification + Merkle root publication."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import AuditRef
from app.services.audit_writer import verify_chain, merkle_root
from app.core.dependencies import require_role

router = APIRouter(prefix="/audit", tags=["UDOC audit"])

@router.get("/chain/verify")
def chain_verify(db: Session = Depends(get_db), _=Depends(require_role("auditor", "admin"))):
    return verify_chain(db)

@router.get("/chain/merkle-root")
def get_merkle(db: Session = Depends(get_db), _=Depends(require_role("auditor", "admin"))):
    return {"merkle_root": merkle_root(db)}

@router.get("/records")
def records(db: Session = Depends(get_db), _=Depends(require_role("auditor", "admin"))):
    rows = db.execute(select(AuditRef).order_by(AuditRef.seq.desc()).limit(100)).scalars().all()
    return [{"seq": r.seq, "event_type": r.event_type, "event_hash": r.event_hash[:16],
             "classification": r.classification, "created_at": r.created_at.isoformat()} for r in rows]
