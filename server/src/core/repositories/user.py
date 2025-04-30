import sqlalchemy as alch

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.repositories.common import CommonRepository
from src.users.models import User, Applicant


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
    
    async def get_users_by_fullname(
            self, start: int, end: int, q: str = None
    ) -> Sequence[User | None]:
        query = alch.select(User).options(
            selectinload(User.applicant),
            selectinload(User.employer),
            selectinload(User.edu_worker)
        )

        if q:
            query = query.where(
                alch.func.concat_ws(' ', User.surname, User.name, User.last_name)
                .like(f"%{q}%")
            )

        query = query.order_by(User.id.desc()).slice(start, end)
        return (await self.session.execute(query)).scalars().all()
    
    async def get_applicants_by_fullname(
            self, user: User, start: int, end: int, q: str = None
    ) -> Sequence[User | None]:
        query = alch.select(User).where(
            User.is_applicant,
            Applicant.edu_institution_id == user.edu_worker.edu_institution_id
        )

        if q:
            query = query.where(
                alch.func.concat_ws(' ', User.surname, User.name, User.last_name)
                .like(f"%{q}%")
            )

        query = (
            query
            .join(User.applicant)
            .options(
                selectinload(User.applicant),
                selectinload(User.location)
            )
        )

        query = query.order_by(User.id.desc()).slice(start, end)
        return (await self.session.execute(query)).scalars().all()

