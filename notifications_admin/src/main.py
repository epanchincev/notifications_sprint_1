from contextlib import asynccontextmanager

from aiohttp import ClientSession
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)

from api.router import router as api_router
from services.exceptions.base import BaseServiceException
from core.config import settings
from core.init_db import init_db
from utils import send_notification


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    send_notification.session = ClientSession()
    yield
    await send_notification.session.close()


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)
app.include_router(api_router)


@app.exception_handler(BaseServiceException)
async def service_exception_handler(
    request: Request,
    exc: BaseServiceException,
):
    raise HTTPException(
        status_code=exc.status_code,
        detail=exc.message,
    )


@app.get("/ping")
async def ping():
    return {"ping": "pong"}
