from fastapi import APIRouter
from app.core.config import settings
router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name, "environment": settings.environment}

@router.get("/health/ready")
def ready():
    # In prod this checks DB/Kafka/HSM reachability; emulation returns ready.
    return {"ready": True, "governance_budget_ms": settings.governance_overhead_budget_ms}
