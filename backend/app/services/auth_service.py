from datetime import datetime, timezone

from app.auth.jwt_handler import create_access_token
from app.auth.password import hash_password, verify_password
from app.database.mongodb import db


class AuthService:

    users = db.users

    @classmethod
    async def register_user(
        cls,
        name: str,
        email: str,
        password: str
    ):

        existing_user = await cls.users.find_one({
            "email": email
        })

        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = hash_password(password)

        user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": "guest",
            "created_at": datetime.now(timezone.utc)
        }   

        result = await cls.users.insert_one(user)

        return {
            "id": str(result.inserted_id),
            "name": name,
            "email": email,
            "role": "guest"
        }


    @classmethod
    async def authenticate_user(
        cls,
        email: str,
        password: str
    ):

        user = await cls.users.find_one({
            "email": email
        })

        if not user:
            return None

        if not verify_password(
            password,
            user["password"]
        ):
            return None

        token = create_access_token({
            "sub": str(user["_id"]),
            "email": user["email"],
            "role": user["role"]
        })

        return token