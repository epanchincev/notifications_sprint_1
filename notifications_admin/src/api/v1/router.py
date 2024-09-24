from fastapi import APIRouter

from api.v1.template import router as template_router
from api.v1.notification import router as notification_router

router = APIRouter(prefix="/v1")

router.include_router(template_router)
router.include_router(notification_router)
