import src.config as config

from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (
    FastAPIUsers, BaseUserManager, IntegerIDMixin
)
from fastapi_users.db import SQLAlchemyUserDatabase

from src.exceptions import LoginBadCredentials
from src.auth.tools import get_user_db
from src.auth.config import auth_backend
from src.users.models import User

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = config.SECRET_TOKEN
    verification_token_secret = config.SECRET_TOKEN

    async def update_password(
            self,
            user: User,
            old_password: str,
            new_password: str
    ) -> None:
        verified, updated_password_hash = self.password_helper.verify_and_update(
            old_password, user.hashed_password
        )
        if not verified:
            raise LoginBadCredentials()

        await self._update(user, {"password": new_password})

    async def update_email(self, user: User, new_email: str, password: str) -> None:
        verified, updated_password_hash = self.password_helper.verify_and_update(
            password, user.hashed_password
        )

        if not verified:
            raise LoginBadCredentials()
        
        await self._update(user, {"email": new_email})

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
