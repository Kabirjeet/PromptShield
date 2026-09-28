from fastapi import FastAPI

from app.api.router import api_router
from app.config.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "application": settings.APP_NAME,
        "status": "running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }