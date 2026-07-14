"""Auth: bcrypt password hashing + JWT issue/verify. Real, not stubbed."""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
import bcrypt
from app.core.config import settings

# Password hashing uses bcrypt DIRECTLY (not via passlib) so it is immune to the
# passlib<->bcrypt version clash: passlib 1.7.4 throws on bcrypt >= 4.1
# ("module 'bcrypt' has no attribute '__about__'"), which 500s every login.
# bcrypt.checkpw still verifies existing passlib-created $2b$ hashes unchanged.

def hash_password(p: str) -> str:
    # bcrypt has a hard 72-byte limit on the input; truncate defensively.
    return bcrypt.hashpw(p.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8")[:72], hashed.encode("utf-8"))
    except Exception:
        return False


def create_token(subject: str, role: str, extra: Optional[dict] = None) -> str:
    now = datetime.now(timezone.utc)
    claims = {
        "sub": subject,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_expire_minutes),
    }
    if extra:
        claims.update(extra)
    return jwt.encode(claims, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as e:
        raise ValueError(f"invalid token: {e}")
