"""Shared FastAPI dependencies: auth guard + role enforcement."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def current_user(token: str = Depends(oauth2)) -> dict:
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing token")
    try:
        return decode_token(token)
    except ValueError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))


def require_role(*roles: str):
    def guard(user: dict = Depends(current_user)) -> dict:
        if roles and user.get("role") not in roles and user.get("role") != "admin":
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"requires role {roles}")
        return user
    return guard
