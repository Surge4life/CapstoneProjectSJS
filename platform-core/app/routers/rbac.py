"""
RBAC API — lets the consoles render role-aware UI from one source of truth.
GET /rbac/me      -> the caller's role, permitted views, permitted action categories, read-only flag
GET /rbac/matrix  -> the full role -> permission matrix (for a transparent permissions view)
"""
from fastapi import APIRouter, Depends
from app.core.dependencies import current_user
from app.services import rbac

router = APIRouter(prefix="/rbac", tags=["RBAC"])


@router.get("/me")
def my_permissions(user: dict = Depends(current_user)):
    return rbac.permissions_for(user.get("role", "viewer"))


@router.get("/matrix")
def role_matrix(user: dict = Depends(current_user)):
    return rbac.matrix()
