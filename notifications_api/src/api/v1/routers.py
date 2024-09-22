from fastapi import APIRouter
from .ping.handlers import router as ping_router
from .register_notification.handlers import router as register_notification_router

router = APIRouter(
    prefix="/v1"
)

router.include_router(ping_router, tags=["ping"])
router.include_router(
    register_notification_router,
    tags=["register-notification"],
)
