from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.common import CommonRepository
from src.users.models import User


class UserRepository(CommonRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def refresh_fields(self, user: User) -> None:
        await self.session.refresh(
            user, ('applicant', 'employer', 'edu_worker', 'location')
        )

    async def update_user(self, user: User, data: dict) -> User:
        for field, value in data.items():
            setattr(user, field, value)

        await self.session.commit()
        return user
    
    async def update_applicant(self, user: User, data: dict) -> User:
        for field, value in data.items():
            setattr(user.applicant, field, value)

        await self.session.commit()
        return user
