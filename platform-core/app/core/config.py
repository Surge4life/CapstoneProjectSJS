"""Central configuration. Sovereign-deployment-aware; env-overridable."""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GODS_", env_file=".env", extra="ignore")

    app_name: str = "GODS Platform Core"
    environment: str = "development"          # development | sovereign | airgapped
    # Database: SQLite for local/dev & emulation; Postgres DSN in production.
    database_url: str = "sqlite:///./gods_core.db"
    # Auth
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    # Governance
    governance_overhead_budget_ms: int = 50    # spec: sub-50ms synchronous enforcement
    fail_closed_for_critical: bool = True      # spec: fail-closed for critical AI classes
    # Hardware integration (emulation flags; real adapters set these false)
    emulate_hsm: bool = True
    emulate_fpga: bool = True
    # Event bus / audit (Kafka + Cassandra in prod; in-memory in dev)
    event_bus_backend: str = "memory"          # memory | kafka
    audit_backend: str = "memory"              # memory | cassandra


def _resolve_database_url(s: "Settings") -> str:
    # Render (and most PaaS) inject an unprefixed DATABASE_URL. Prefer it when present.
    url = os.environ.get("DATABASE_URL") or s.database_url
    # SQLAlchemy needs postgresql:// (psycopg), not the legacy postgres:// scheme.
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


settings = Settings()
settings.database_url = _resolve_database_url(settings)
