from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)

import aio_pika
from src.api.routers import router as api_router
from src.config.loging import get_logger
from src.config.settings import settings
from src.errors.base import ServiceException
from src.queue import rabbit
from src.services.errors import UnexpectedProducerError


logger = get_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    rabbit.rabbitmq = await aio_pika.connect_robust(
        url=settings.rabbit_url,
    )
    yield
    await rabbit.rabbitmq.close()


app = FastAPI(
    title="Notifications API Service",
    lifespan=lifespan,
)


@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    if isinstance(exc, UnexpectedProducerError):
        logger.error(exc.main_error, exc_info=True)
    raise HTTPException(
        status_code=exc.status_code,
        detail=exc.message,
    )

app.include_router(api_router)
