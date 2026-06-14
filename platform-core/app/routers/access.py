"""
Access API — the G.O.D.S core uses this to open the right internal systems by role/division.
Server-authoritative: /access/profile returns ONLY the systems the user may open, and
/access/guard/{system} enforces it (403 if not permitted) so consoles can verify on entry.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import current_user
from app.services.access_control import systems_for, may_open
from app.services import sovereign_profiles as sp

router = APIRouter(prefix="/access", tags=["Access control"])


@router.get("/profile")
def profile(user: dict = Depends(current_user)):
    role = user.get("role", "viewer")
    division = user.get("division", "GODS")
    systems = systems_for(role, division)
    return {
        "email": user.get("sub"),
        "role": role,
        "division": division,
        "systems": systems,                       # the launcher renders exactly these
        "is_admin": role in ("admin", "exec"),
    }


@router.get("/profiles", summary="The 24 Sovereign-Operator profiles (grouped) + their capabilities")
def profiles(user: dict = Depends(current_user)):
    return {"profiles": sp.catalog(), "by_group": sp.by_group(),
            "groups": sp.GROUPS, "count": len(sp.PROFILES)}


@router.get("/matrix", summary="Profile × capability matrix + role→systems grid")
def matrix(user: dict = Depends(current_user)):
    return sp.matrix()


@router.get("/guard/{system_key}")
def guard(system_key: str, user: dict = Depends(current_user)):
    """Consoles call this on entry; 403 if the user may not open this system."""
    if not may_open(user.get("role", "viewer"), user.get("division", "GODS"), system_key):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            f"access denied: {user.get('role')}/{user.get('division')} may not open {system_key}")
    return {"system": system_key, "granted": True}
