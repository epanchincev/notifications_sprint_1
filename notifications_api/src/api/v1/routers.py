from fastapi import APIRouter

from .default_notification.handlers import router as register_notification_router
from .ping.handlers import router as ping_router


router = APIRouter(
    prefix="/v1",
)

router.include_router(ping_router, tags=["ping"])
router.include_router(
    register_notification_router,
    tags=["register-notification"],
)
