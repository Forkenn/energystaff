from src.core.repositories.user import UserRepository
from src.users.models import User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def refresh_fields(self, user: User) -> None:
        await self.user_repo.refresh_fields(user)
