"""Seed the platform with an admin user, a model, and starter division data."""
import sys; sys.path.insert(0, ".")
from app.db.session import init_db, SessionLocal
from app.db.models import User, AIModel, Decision, OversightCase, Tenant
from app.core.tiers import tier_info
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
    db.commit()
    # --- SaaS tenants (Public + Private) + tenant client users ---
    def ensure_tenant(tid, name, sector, tier):
        t = db.query(Tenant).filter(Tenant.tenant_id == tid).first()
        if not t:
            t = Tenant(tenant_id=tid, name=name, sector=sector, tier=tier, status="ACTIVE",
                       decision_quota=tier_info(tier)["decision_quota"])
            db.add(t); db.commit(); db.refresh(t)
        return t
    dsd = ensure_tenant("gov-dsd", "Dept. of Social Development (Public)", "PUBLIC", "ENTERPRISE")
    acme = ensure_tenant("acme-bank", "Acme Bank (Private)", "PRIVATE", "GROWTH")
    for email, t in [("client.dsd@gods.local", dsd), ("client.acme@gods.local", acme)]:
        if not db.query(User).filter(User.email == email).first():
            db.add(User(email=email, password_hash=hash_password("client123"), role="client",
                        division="UDOC", tenant_id=t.tenant_id, tenant_pk=t.id))
    db.commit()
    if not db.query(AIModel).filter(AIModel.model_id == "model-001").first():
        db.add(AIModel(model_id="model-001", name="ZA-CreditScorer", operator_id="op-fnb",
                       risk_tier="NOTABLE", use_case="credit scoring", jurisdiction="ZA", tenant_pk=dsd.id))
    if not db.query(AIModel).filter(AIModel.model_id == "model-002").first():
        db.add(AIModel(model_id="model-002", name="Acme-FraudScore", operator_id="op-acme",
                       risk_tier="NOTABLE", use_case="fraud detection", jurisdiction="ZA", tenant_pk=acme.id))
    # representative staff for role/division access demonstration
    staff = [
        ("seths.op@gods.local", "operator", "SETHS"),
        ("madiba.op@gods.local", "operator", "MADIBA"),
        ("ts.op@gods.local", "operator", "TS"),
        ("cob@gods.local", "gov", "GODS"),
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
    print("✓ seeded admin + 2 tenants (gov-dsd, acme-bank) + client users + models + activity")

if __name__ == "__main__":
    run()
