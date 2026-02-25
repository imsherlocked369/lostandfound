import os

import bcrypt
import jwt

from app.constant.error import AuthError
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


SECRET_TOKEN = os.environ.get("SECRET_TOKEN", "dev-secret-change-me")


class UserService:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    def create_user(self, payload: UserCreate) -> User:
        existing_user = self.userRepository.get_by_email(payload.email)
        if existing_user:
            raise ValueError(AuthError.EMAIL_ALREADY_EXISTS)

        password_hash = bcrypt.hashpw(
            payload.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            email=payload.email,
            firstName=payload.firstName,
            lastName=payload.lastName,
            phone=payload.phone,
            password_hash=password_hash,
        )

        return self.userRepository.create(user)

    def login(self, email: str, password: str) -> str:
        user = self.userRepository.get_by_email(email)

        if not user:
            raise ValueError(AuthError.USER_NOT_FOUND)

        checkPassword = bcrypt.checkpw(
            password.encode("utf-8"), user.password_hash.encode("utf-8")
        )
        if not checkPassword:
            raise ValueError(AuthError.INVALID_PASSWORD)

        payload = {
            "user_id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "role": user.role,
        }

        token = jwt.encode(payload, SECRET_TOKEN, algorithm="HS256")

        return token
