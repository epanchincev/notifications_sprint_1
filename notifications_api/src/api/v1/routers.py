from fastapi import APIRouter
from .ping.handlers import router as ping_router

router = APIRouter(
    prefix="/v1"
)

router.include_router(ping_router, tags=["ping"])
