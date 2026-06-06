"""Shared FastAPI dependencies: auth guard + role enforcement."""
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
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


PLATFORM_ROLES = {"admin", "operator", "gov", "auditor"}


def principal(request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2)) -> dict:
    """Authenticated principal via Bearer JWT OR X-API-Key (tenant-scoped service access)."""
    key = request.headers.get("x-api-key")
    if key:
        import hashlib
        from datetime import datetime, timezone
        from sqlalchemy import select
        from app.db.models import ApiKey, Tenant
        kh = hashlib.sha256(key.encode()).hexdigest()
        ak = db.execute(select(ApiKey).where(ApiKey.key_hash == kh, ApiKey.active == True)).scalar_one_or_none()  # noqa: E712
        if not ak:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid API key")
        t = db.get(Tenant, ak.tenant_pk)
        ak.last_used_at = datetime.now(timezone.utc); db.commit()
        return {"sub": f"apikey:{ak.prefix}", "role": "client", "division": "UDOC",
                "tenant_id": (t.tenant_id if t else ""), "tenant_pk": ak.tenant_pk, "via": "api_key"}
    if token:
        try:
            return decode_token(token)
        except ValueError as e:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing credentials")


def scope_pk(user: dict):
    """tenant_pk a caller is restricted to, or None for platform-wide (staff) access."""
    tpk = user.get("tenant_pk")
    if tpk:
        return tpk
    if user.get("role") in PLATFORM_ROLES:
        return None
    return -1  # tenant-less non-platform caller -> sees nothing


def require_role(*roles: str):
    def guard(user: dict = Depends(current_user)) -> dict:
        if roles and user.get("role") not in roles and user.get("role") != "admin":
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"requires role {roles}")
        return user
    return guard
