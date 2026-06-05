"""Seed the platform with an admin user, a model, and starter division data."""
import sys; sys.path.insert(0, ".")
from app.db.session import init_db, SessionLocal
from app.db.models import User, AIModel, Decision, OversightCase
from app.core.security import hash_password
from app.services.governance_bridge import Evidence, evaluate
from app.services.audit_writer import append_audit
import random, uuid

def run():
    init_db()
    db = SessionLocal()
    if not db.query(User).filter(User.email == "admin@gods.local").first():
        db.add(User(email="admin@gods.local", password_hash=hash_password("admin123"),
                    role="admin", division="GODS"))
    if not db.query(AIModel).filter(AIModel.model_id == "model-001").first():
        db.add(AIModel(model_id="model-001", name="ZA-CreditScorer", operator_id="op-fnb",
                       risk_tier="NOTABLE", use_case="credit scoring", jurisdiction="ZA"))
    # representative staff for role/division access demonstration
    staff = [
        ("seths.op@gods.local", "operator", "SETHS"),
        ("madiba.op@gods.local", "operator", "MADIBA"),
        ("ts.op@gods.local", "operator", "TS"),
        ("auditor@gods.local", "auditor", "GODS"),
        ("exec@gods.local", "exec", "GODS"),
        ("viewer@gods.local", "viewer", "GODS"),
    ]
    for email, role, div in staff:
        if not db.query(User).filter(User.email == email).first():
            db.add(User(email=email, password_hash=hash_password("staff123"), role=role, division=div))
    db.commit()
    # --- starter governance activity (genuine EVA decisions + Merkle audit + an oversight case) ---
    m = db.query(AIModel).filter(AIModel.model_id == "model-001").first()
    if m and db.query(Decision).count() == 0:
        for _ in range(14):
            ev = Evidence(model_id="model-001", risk_tier=m.risk_tier,
                          raw_confidence=round(random.uniform(.72, .97), 2), compliance=1.0,
                          priv_favorable=480, priv_total=1000, unpriv_favorable=470, unpriv_total=1000,
                          ecs=0.75, bgp=1.0, traceroute=1.0, dnssec=1.0, storage=1.0)
            v = evaluate(ev)
            db.add(Decision(model_pk=m.id, decision=v.decision, svs=v.svs, risk=v.risk,
                            compliance=v.compliance, sovereign=v.sovereign, seal=v.seal,
                            latency_ms=v.latency_ms, block_reasons=" | ".join(v.block_reasons)))
            db.commit()
            append_audit(db, "AI_DECISION", {"model_id": "model-001", "decision": v.decision,
                         "svs": v.svs, "seal": v.seal[:16]}, classification="GOVERNANCE", actor_class="admin")
        if db.query(OversightCase).count() == 0:
            c = OversightCase(case_ref=f"COB-{uuid.uuid4().hex[:8]}", model_id="model-001",
                              reason="Disparate impact review — welfare eligibility")
            db.add(c); db.commit()
            append_audit(db, "OVERSIGHT_OPEN", {"case": c.case_ref, "model": "model-001"},
                         classification="GOVERNANCE")
    db.commit(); db.close()
    print("✓ seeded admin@gods.local / admin123 + model-001 + starter governance activity")

if __name__ == "__main__":
    run()
