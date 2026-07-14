"""Pytest suite — governance path, audit chain, division flows."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import init_db, SessionLocal
from app.db.models import User
from app.core.security import hash_password

@pytest.fixture(scope="module")
def client():
    if os.path.exists("gods_core.db"):
        os.remove("gods_core.db")
    init_db()
    db = SessionLocal()
    db.add(User(email="admin@gods.local", password_hash=hash_password("admin123"), role="admin", division="GODS"))
    db.commit(); db.close()
    return TestClient(app)

@pytest.fixture(scope="module")
def token(client):
    return client.post("/auth/login", data={"username": "admin@gods.local", "password": "admin123"}).json()["access_token"]

def H(t): return {"Authorization": f"Bearer {t}"}

def test_root_live(client):
    assert client.get("/").json()["status"] == "live"

def test_register_and_decide_approve(client, token):
    client.post("/registry/models", json={"model_id": "m-test", "name": "T", "operator_id": "op"}, headers=H(token))
    r = client.post("/decisions", json={"model_id": "m-test"}, headers=H(token)).json()
    assert r["decision"] == "APPROVE"
    assert r["within_budget"] is True
    assert len(r["seal"]) == 64

def test_biased_blocks(client, token):
    r = client.post("/decisions", json={"model_id": "m-test", "risk_tier": "HIGH",
        "priv_favorable": 600, "unpriv_favorable": 300, "ecs": 0.3}, headers=H(token)).json()
    assert r["decision"] == "BLOCK"
    assert len(r["block_reasons"]) >= 3

def test_sovereignty_breach_blocks(client, token):
    r = client.post("/decisions", json={"model_id": "m-test", "traceroute": 0.4}, headers=H(token)).json()
    assert r["decision"] == "BLOCK"
    assert r["sovereign"] is False

def test_audit_chain_intact(client, token):
    v = client.get("/audit/chain/verify", headers=H(token)).json()
    assert v["intact"] is True
    assert v["records"] >= 3

def test_unknown_model_fail_closed(client, token):
    r = client.post("/decisions", json={"model_id": "does-not-exist"}, headers=H(token))
    assert r.status_code == 404  # fail-closed

def test_unauthenticated_rejected(client):
    assert client.post("/decisions", json={"model_id": "m-test"}).status_code == 401

def test_division_metrics(client, token):
    client.post("/seths/enrol", json={"count": 5}, headers=H(token))
    assert client.get("/seths/metrics").json()["total"] >= 5
