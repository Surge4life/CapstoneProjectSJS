"""Seed the platform with an admin user, a model, and starter division data."""
import sys; sys.path.insert(0, ".")
from app.db.session import init_db, SessionLocal
from app.db.models import User, AIModel
from app.core.security import hash_password

def run():
    init_db()
    db = SessionLocal()
    if not db.query(User).filter(User.email == "admin@gods.za").first():
        db.add(User(email="admin@gods.za", password_hash=hash_password("admin123"),
                    role="admin", division="GODS"))
    if not db.query(AIModel).filter(AIModel.model_id == "model-001").first():
        db.add(AIModel(model_id="model-001", name="ZA-CreditScorer", operator_id="op-fnb",
                       risk_tier="NOTABLE", use_case="credit scoring", jurisdiction="ZA"))
    # representative staff for role/division access demonstration
    staff = [
        ("seths.op@gods.za", "operator", "SETHS"),
        ("madiba.op@gods.za", "operator", "MADIBA"),
        ("ts.op@gods.za", "operator", "TS"),
        ("auditor@gods.za", "auditor", "GODS"),
        ("exec@gods.za", "exec", "GODS"),
        ("viewer@gods.za", "viewer", "GODS"),
    ]
    for email, role, div in staff:
        if not db.query(User).filter(User.email == email).first():
            db.add(User(email=email, password_hash=hash_password("staff123"), role=role, division=div))
    db.commit(); db.close()
    print("✓ seeded admin@gods.za / admin123 + model-001")

if __name__ == "__main__":
    run()
