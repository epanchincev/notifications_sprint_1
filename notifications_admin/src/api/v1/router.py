from fastapi import APIRouter

from api.v1.template import router as template_router

router = APIRouter(prefix="/v1")

router.include_router(template_router)
