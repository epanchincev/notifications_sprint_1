from fastapi import FastAPI
from api.v1.routers import router as api_router

app = FastAPI(
    title="Notifications API Service"
)

app.include_router(api_router)
