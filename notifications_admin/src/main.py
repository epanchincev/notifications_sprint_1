from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)

from api.router import router as api_router
from services.exceptions.base import BaseServiceException
from core.logger import setup_root_logger
from core.config import settings


setup_root_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


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
