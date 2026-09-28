from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/firewall",
    tags=["Firewall"]
)


@router.get("/ping")
async def ping():

    return {
        "message": "Firewall Module Ready"
    }


@router.get("/protected")
async def protected_route(
    current_user: dict = Depends(get_current_user)
):

    return {
        "message": "You have accessed a protected endpoint",
        "user": current_user
    }