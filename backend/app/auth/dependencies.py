# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer

# from app.auth.jwt_handler import decode_access_token


# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/api/v1/auth/login"
# )


# async def get_current_user(
#     token: str = Depends(oauth2_scheme)
# ):

#     try:

#         payload = decode_access_token(token)

#         user_id = payload.get("sub")
#         email = payload.get("email")
#         role = payload.get("role")

#         if not user_id or not email or not role:
#             raise ValueError("Invalid token payload")

#         return {
#             "id": user_id,
#             "email": email,
#             "role": role
#         }

#     except ValueError:

#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired authentication token",
#             headers={
#                 "WWW-Authenticate": "Bearer"
#             }
#         )

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.jwt_handler import decode_access_token


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload