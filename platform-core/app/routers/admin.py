"""GODS Admin — cross-system status for the admin mainframe."""
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User, AIModel, Decision, Learner, TSProject, OversightCase
from app.core.dependencies import require_role

router = APIRouter(prefix="/admin", tags=["GODS Admin"])

@router.get("/status")
def status(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    def c(model): return db.execute(select(func.count(model.id))).scalar() or 0
    return {"users": c(User), "models": c(AIModel), "decisions": c(Decision),
            "learners": c(Learner), "ts_projects": c(TSProject),
            "open_oversight": db.execute(select(func.count(OversightCase.id))
                                         .where(OversightCase.state == "OPEN")).scalar() or 0,
            "divisions": ["GODS", "SETHS", "MADIBA", "TS", "UDOC"]}
