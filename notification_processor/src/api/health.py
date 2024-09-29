from fastapi import APIRouter
from schemas.health import HealthCheck

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck(status="OK")
