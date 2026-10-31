from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.api.firewall import router as firewall_router
from app.api.logs import router as logs_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(firewall_router)
api_router.include_router(logs_router)