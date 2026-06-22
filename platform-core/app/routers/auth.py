from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.core.security import verify_password, hash_password, create_token
from app.core.dependencies import current_user
from pydantic import BaseModel, field_validator

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterReq(BaseModel):
    email: str
    password: str
    role: str = "viewer"
    division: str = "GODS"

    @field_validator("email")
    @classmethod
    def _normalise_email(cls, v: str) -> str:
        v = (v or "").strip().lower()
        local, _, domain = v.partition("@")
        if not local or "@" in domain or "." not in domain:
            raise ValueError("invalid email address")
        return v

@router.post("/register")
def register(req: RegisterReq, db: Session = Depends(get_db)):
    if db.execute(select(User).where(User.email == req.email)).scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "email exists")
    u = User(email=req.email, password_hash=hash_password(req.password), role=req.role, division=req.division)
    db.add(u); db.commit(); db.refresh(u)
    return {"id": u.id, "email": u.email, "role": u.role, "division": u.division}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = db.execute(select(User).where(User.email == form.username)).scalar_one_or_none()
    if not u or not verify_password(form.password, u.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "bad credentials")
    if not u.active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "account deactivated — contact an administrator")
    token = create_token(u.email, u.role, {"division": u.division,
                          "tenant_id": u.tenant_id or "", "tenant_pk": u.tenant_pk})
    return {"access_token": token, "token_type": "bearer", "role": u.role,
            "division": u.division, "tenant_id": u.tenant_id or ""}

@router.get("/me")
def me(user: dict = Depends(current_user)):
    return user
