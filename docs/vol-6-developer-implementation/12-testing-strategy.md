# Chapter 12 — Testing Strategy

## The G.O.D.S Testing Philosophy

Tests in the G.O.D.S ecosystem are not bureaucratic checkboxes. They are contractual guarantees. When the test suite passes, you are guaranteed that:

1. The constitutional checks enforce their stated limits
2. The governance path produces deterministic, auditable outcomes
3. RBAC prevents unauthorised access
4. The audit chain is complete and verifiable
5. Document integrity is enforced

A test failure is not a development inconvenience. It is a governance signal.

---

## Test Hierarchy

### Level 1: Unit Tests

**What:** Individual functions, classes, and services tested in isolation  
**Where:** `tests/test_*.py` files  
**Mocking:** External dependencies (EVA engine, database) are mocked  
**Speed:** Should complete in < 1 second per test  
**Coverage target:** 80% line coverage on `platform-core/app/`

**Key unit test files:**

| File | What It Tests |
|------|-------------|
| `test_eva_scorer.py` | EVA dimension scorers with known inputs |
| `test_gbs_engine.py` | GBS decision path with mocked EVA scores |
| `test_audit_writer.py` | Audit record creation and chain hash |
| `test_rbac.py` | Permission evaluation logic |
| `test_document_store.py` | SHA-256 integrity sealing |
| `test_evidence_ranker.py` | Evidence scoring and confidence computation |

### Level 2: Integration Tests

**What:** Services tested with real database and infrastructure  
**Where:** `tests/test_*_integration.py`  
**Dependencies:** Docker Compose stack must be running  
**Speed:** 1–30 seconds per test  
**Coverage:** All major service workflows

**Run integration tests:**
```bash
# Start infrastructure
docker compose -f infra/docker-compose.yml up -d

# Wait for databases to be ready
sleep 30

# Run integration tests
python -m pytest tests/ -k "integration" -v
```

### Level 3: Constitutional Tests

**What:** The 11 constitutional checks  
**Where:** `tests/test_constitutional_checks.py`  
**Special status:** These tests are non-negotiable. They must pass 11/11 on every build.  
**Failure behaviour:** Constitutional test failures block the CI pipeline entirely

### Level 4: Security Tests

**What:** RBAC boundaries, injection, rate limiting, cross-tenant isolation  
**Where:** `tests/test_security.py`  
**Run on:** Every PR, full security scan on every merge to main

### Level 5: Smoke Tests

**What:** End-to-end tests against a live deployment  
**Where:** `smoke_test.py` (root level)  
**Run against:** Staging deployment before production promote  
**Success threshold:** 31/31 paths must pass

---

## CI Test Execution Order

```
1. Lint (ruff, mypy) — 30 seconds
2. Unit tests — 2 minutes
3. Constitutional tests — 30 seconds [BLOCKING]
4. Integration tests — 5 minutes
5. Security tests — 3 minutes
6. Smoke tests (staging) — 5 minutes
Total CI time: ~16 minutes
```

Steps 3 (constitutional tests) and 5 (smoke tests) are individually blocking — a failure at either step prevents deployment regardless of other test results.

---

## Test Data

Test data is managed with factories:

```python
# tests/factories.py
def make_decision_record(
    outcome: str = "APPROVE",
    eva_fa: int = 85,
    eva_rc: int = 90,
    policy_version: int = 1,
    **kwargs
) -> DecisionRecord:
    """Creates a test DecisionRecord with sensible defaults."""
    ...
```

Factories allow tests to be explicit about what matters for that test (the fields being tested) and implicit about everything else (use sensible defaults). This makes test intent clear.

---

## Test Coverage Enforcement

The CI pipeline enforces coverage thresholds:

```ini
# pytest.ini
[tool:pytest]
addopts = --cov=platform-core/app --cov-fail-under=80

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    if TYPE_CHECKING
```

Code that drops below 80% coverage fails CI. This is a floor, not a target — aim for 90%+ on governance critical path code.

---

## Testing the Audit Chain

The audit chain is tested with a dedicated test that verifies:

1. A governance decision creates a Cassandra audit record
2. The chain hash is computed correctly
3. The HMAC seal is valid
4. The `prev_record_hash` links correctly to the previous record
5. Modifying any field of the record invalidates the chain hash (tamper detection)

```python
def test_audit_chain_tamper_detection():
    decision = create_test_decision()
    audit_record = audit_chain.get_record(decision.audit_ref_id)
    
    # Verify chain is intact
    assert audit_chain.verify_record(audit_record) == True
    
    # Tamper with the record
    audit_record.outcome = "APPROVE"  # Was BLOCK
    
    # Verify chain detects tampering
    assert audit_chain.verify_record(audit_record) == False
```
