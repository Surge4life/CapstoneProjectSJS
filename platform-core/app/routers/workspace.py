"""
Sovereign-Operator Workspace API — the live console behind each of the 24 profiles.
GET /workspace          -> the caller's profile, live tiles, and available capability actions
POST /workspace/action  -> execute one of the caller's OWN capabilities (server-enforced + audited)
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import current_user
from app.services import workspace as ws

router = APIRouter(prefix="/workspace", tags=["Sovereign-Operator workspace"])


@router.get("")
def get_workspace(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    p = ws.resolve_profile(db, user)
    return {
        "profile": {k: p[k] for k in ("key", "title", "group", "base_role", "division")},
        "tiles": ws.tiles_for(db, p),
        "actions": ws.actions_for(p),
    }


class ActionReq(BaseModel):
    capability: str
    params: dict | None = None


@router.get("/options")
def get_options(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    """Select-source data (open cases, AI systems) for parameterised actions."""
    return ws.options(db, user)


@router.get("/actions")
def get_actions(limit: int = 30, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    """The caller's recent operator-action history (structured + inspectable)."""
    return {"actions": ws.op_history(db, user.get("sub", ""), min(max(limit, 1), 100))}


@router.post("/action")
def post_action(body: ActionReq, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    p = ws.resolve_profile(db, user)
    allowed = {c.lower() for c in p["capabilities"]}
    if (body.capability or "").lower() not in allowed:
        raise HTTPException(403, f"capability '{body.capability}' is not authorised for the {p['title']} profile")
    return ws.run_action(db, user, p, body.capability, body.params)
