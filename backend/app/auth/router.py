from fastapi import APIRouter, HTTPException, status

from app.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(request: RegisterRequest):

    try:

        user = await AuthService.register_user(
            name=request.name,
            email=request.email,
            password=request.password
        )

        return user

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(request: LoginRequest):

    token = await AuthService.authenticate_user(
        email=request.email,
        password=request.password
    )

    if not token:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }