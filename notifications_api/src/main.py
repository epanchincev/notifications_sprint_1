from contextlib import asynccontextmanager
import aio_pika
from fastapi import FastAPI
from src.config.settings import settings
from src.api.v1.routers import router as api_router
from src.queue import rabbit


@asynccontextmanager
async def lifespan(_: FastAPI):
    rabbit.rabbitmq = await aio_pika.connect_robust(
        url=settings.rabbit_url
    )
    yield
    rabbit.rabbitmq.close()


app = FastAPI(
    title="Notifications API Service",
    lifespan=lifespan,
)

app.include_router(api_router)
