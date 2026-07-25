# Chapter 02 — platform-core

## The Backend Governance Service

`platform-core` is the central FastAPI application. It is the single API server that all frontend applications, edge components, and external clients communicate with. All governance logic runs here or is orchestrated from here.

---

## Directory Structure

```
platform-core/
├── app/
│   ├── main.py              # FastAPI application factory, startup, lifespan
│   ├── core/
│   │   ├── config.py        # Environment configuration (Pydantic Settings)
│   │   ├── dependencies.py  # FastAPI dependency injection (auth, db session)
│   │   ├── security.py      # JWT, bcrypt, token validation
│   │   └── mtls.py          # mTLS configuration and enforcement
│   ├── db/
│   │   ├── session.py       # SQLAlchemy engine, session factory
│   │   ├── base.py          # Base declarative model
│   │   └── models/          # SQLAlchemy ORM models (one file per domain)
│   │       ├── user.py
│   │       ├── registry.py  # AIModel
│   │       ├── decisions.py # DecisionRecord, OversightCase
│   │       ├── audit_ref.py # AuditRef (queryable audit index)
│   │       ├── workforce.py # Learner, Employer, Employee, Opportunity, Application
│   │       ├── capital.py   # InstitutionalMilestone, CapitalCycle
│   │       ├── projects.py  # TSProject, DivisionRecord
│   │       ├── oversight.py # OversightCase, OperatorAction
│   │       ├── saas.py      # SaaSClient, TenantConfig
│   │       ├── documents.py # Document, KnowledgeDoc
│   │       └── policy.py    # PolicyPack, PolicyRule
│   ├── routers/             # FastAPI routers (one file per domain)
│   │   ├── access.py
│   │   ├── admin.py
│   │   ├── admin_udoc.py
│   │   ├── analytics.py
│   │   ├── audit.py
│   │   ├── auth.py
│   │   ├── bias.py
│   │   ├── client_knowledge.py
│   │   ├── compliance.py
│   │   ├── conformance.py
│   │   ├── decisions.py
│   │   ├── documents.py
│   │   ├── enclave.py
│   │   ├── gis.py
│   │   ├── intelligence.py
│   │   ├── lineage.py
│   │   ├── madiba.py
│   │   ├── policy.py
│   │   ├── portals_employee.py
│   │   ├── portals_employer.py
│   │   ├── portals_student.py
│   │   ├── portals_ops.py
│   │   ├── rbac.py
│   │   ├── registry.py
│   │   ├── saas.py
│   │   ├── sectors.py
│   │   ├── seths.py
│   │   ├── sovereignty.py
│   │   ├── staychain.py
│   │   ├── tenants.py
│   │   ├── ts.py
│   │   ├── udoc_engine.py
│   │   └── workspace.py
│   ├── services/            # Business logic (one file per service)
│   │   ├── access_control.py
│   │   ├── analytics_engine.py
│   │   ├── audit_writer.py
│   │   ├── cetcte_engine.py
│   │   ├── client_knowledge.py
│   │   ├── conformance_scanner.py
│   │   ├── crypto_provider.py
│   │   ├── document_store.py
│   │   ├── event_bus.py
│   │   ├── gbs_engine.py
│   │   ├── gis_engine.py
│   │   ├── gods_intelligence.py
│   │   ├── governance_bridge.py
│   │   ├── key_service.py
│   │   ├── policy_engine.py
│   │   ├── rbac.py
│   │   ├── sectors.py
│   │   └── sovereign_profiles.py
│   └── schemas/             # Pydantic request/response schemas
│       ├── auth.py
│       ├── decisions.py
│       ├── registry.py
│       ├── seths.py
│       ├── madiba.py
│       ├── ts.py
│       ├── audit.py
│       ├── policy.py
│       ├── intelligence.py
│       └── common.py
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container build
└── README.md
```

---

## Responsibility Boundaries

`platform-core` is responsible for:
- ✅ HTTP API serving (FastAPI)
- ✅ Authentication and authorisation
- ✅ Request validation (Pydantic)
- ✅ Database operations (SQLAlchemy)
- ✅ Orchestrating governance engine calls
- ✅ Writing to the audit chain
- ✅ Publishing events to Kafka

`platform-core` is NOT responsible for:
- ❌ AI model inference (that's the governed model's job)
- ❌ EVA scoring logic (that's `governance-engines/eva/`)
- ❌ GBS rule evaluation (that's `governance-engines/udoc/`)
- ❌ FPGA/HSM hardware operations (that's `hw-bringup/`)

---

## Configuration

All configuration is via environment variables. No configuration is hardcoded in application code. The `core/config.py` module uses Pydantic Settings to validate the configuration at startup.

Required environment variables:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing key (RS256 private key PEM) |
| `REDIS_URL` | Redis connection for token blacklist and cache |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker addresses |
| `CASSANDRA_HOSTS` | Cassandra cluster hosts |
| `OPENSEARCH_URL` | OpenSearch for corpus and governance search |
| `OBJECT_STORAGE_URL` | S3-compatible URL for document storage |
| `OBJECT_STORAGE_BUCKET` | Bucket name |
| `HSM_PKCS11_LIB` | Path to PKCS#11 library (software or hardware) |
| `GOVERNANCE_ENGINE_URL` | Internal URL of governance-engines service |
| `ENVIRONMENT` | `development | staging | production` |

---

## Startup Sequence

```python
# main.py lifespan (simplified)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Validate all environment variables
    # 2. Connect to PostgreSQL (test connection)
    # 3. Connect to Redis (test connection)
    # 4. Connect to Kafka (test connection)
    # 5. Connect to governance-engines (health check)
    # 6. Load current PolicyPack from database
    # 7. Write startup audit record
    # 8. Log startup summary (version, governance version, jurisdiction)
    yield
    # Shutdown: write shutdown audit record, close connections
```

If any step in the startup sequence fails, the service does not start. It does not silently fall back to a degraded mode. This is Principle 1 (Fail Closed) applied to service startup.
