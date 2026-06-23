"""
Repair all known G.O.D.S accounts with VALID password hashes.

Why: while passlib was broken by bcrypt>=4.1, password writes either failed or stored
unverifiable hashes, so every login returns 401. This re-hashes (or creates) each known
account using the fixed bcrypt-direct hasher in app/core/security.py.

Run from platform-core with your Neon URL and the FIXED security.py in place:
    DATABASE_URL="<your-neon-pooled-url>" python3 fix_passwords.py

Safe to run repeatedly. It only touches these known accounts; it does not delete anything.
"""
from app.db.session import SessionLocal
from app.db.models import User
from app.core.security import hash_password, verify_password

# email, password, role, division  (matches seed.py)
ACCOUNTS = [
    ("admin@gods.local",        "admin123",  "admin",    "GODS"),
    ("client.dsd@gods.local",   "client123", "client",   "DSD"),
    ("client.acme@gods.local",  "client123", "client",   "ACME"),
    ("seths.op@gods.local",     "staff123",  "operator", "SETHS"),
    ("madiba.op@gods.local",    "staff123",  "operator", "MADIBA"),
    ("ts.op@gods.local",        "staff123",  "operator", "TS"),
    ("cob@gods.local",          "staff123",  "gov",      "GODS"),
    ("auditor@gods.local",      "staff123",  "auditor",  "GODS"),
    ("exec@gods.local",         "staff123",  "exec",     "GODS"),
    ("viewer@gods.local",       "staff123",  "viewer",   "GODS"),
]


def main():
    db = SessionLocal()
    created = reset = 0
    for email, pw, role, div in ACCOUNTS:
        u = db.query(User).filter(User.email == email).first()
        h = hash_password(pw)
        if u:
            u.password_hash = h
            reset += 1
            tag = "reset  "
        else:
            db.add(User(email=email, password_hash=h, role=role, division=div))
            created += 1
            tag = "created"
        # prove the new hash verifies before we commit
        ok = verify_password(pw, h)
        print(f"  {tag} {email:28} verify={ok}")
    db.commit()

    # final read-back verification
    print("\n  read-back check:")
    all_ok = True
    for email, pw, *_ in ACCOUNTS:
        u = db.query(User).filter(User.email == email).first()
        ok = bool(u) and verify_password(pw, u.password_hash)
        all_ok = all_ok and ok
        if not ok:
            print(f"    ✗ {email} FAILED")
    db.close()
    print(f"\n  {created} created, {reset} reset. "
          + ("ALL ACCOUNTS VERIFY ✅ — log in now." if all_ok else "SOME FAILED ✗"))


if __name__ == "__main__":
    main()
