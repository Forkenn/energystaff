import sqlalchemy as alch

from datetime import date
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.repositories.common import CommonRepository
from src.users.models import User, Applicant, Employer, EduWorker


class UserRepository(CommonRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def create_applicant(self, user: User) -> None:
        user.applicant = Applicant(user_id=user.id)
        await self.session.commit()

    async def create_employer(self, user: User, company_id: int) -> None:
        user.employer = Employer(company_id=company_id)
        await self.session.commit()

    async def create_edu_worker(self, user: User, edu_institution_id: int) -> None:
        user.edu_worker = EduWorker(edu_institution_id=edu_institution_id)
        await self.session.commit()

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
    
    async def _get_users_by_fullname_query(
            self,
            query: alch.Select,
            birthdate: date = None,
            only_verified: bool = False,
            location_id: int = None,
            q: str = None
    ) -> alch.Select:
        if birthdate:
            query = query.where(User.birthdate == birthdate)

        if only_verified:
            query = query.where(User.is_verified == True)

        if location_id is not None:
            query = query.where(User.location_id == location_id)

        if q:
            query = query.where(
                alch.func.concat_ws(' ', User.surname, User.name, User.last_name)
                .like(f"%{q}%")
            )

        return query
    
    async def get_users_by_fullname(
            self,
            birthdate: date = None,
            only_verified: bool = False,
            location_id: int = None,
            q: str = None,
            start: int = None,
            end: int = None,
            desc: bool = True
    ) -> Sequence[User | None]:
        query = alch.select(User).options(
            selectinload(User.applicant),
            selectinload(User.employer),
            selectinload(User.edu_worker),
            selectinload(User.location)
        )

        query = await self._get_users_by_fullname_query(
            query=query,
            birthdate=birthdate,
            only_verified=only_verified,
            location_id=location_id,
            q=q
        )

        if desc:
            query = query.order_by(User.id.desc())
        else:
            query = query.order_by(User.id.asc())

        query = query.slice(start, end)
        return (await self.session.execute(query)).scalars().all()

    async def count_users_by_fullname(
            self,
            birthdate: date = None,
            only_verified: bool = False,
            location_id: int = None,
            q: str = None
    ) -> int:
        query = alch.select(alch.func.count()).select_from(User)
        query = await self._get_users_by_fullname_query(
            query=query,
            birthdate=birthdate,
            only_verified=only_verified,
            location_id=location_id,
            q=q
        )

        result = await self.session.execute(query)
        return result.scalar()

    async def get_applicant_by_id(
            self,
            edu_institution_id: int,
            id: int
    ) -> User:
        query = alch.select(User).where(
            User.is_applicant,
            User.id == id,
            Applicant.edu_institution_id == edu_institution_id
        )

        query = (
            query
            .join(User.applicant)
            .options(
                selectinload(User.applicant),
                selectinload(User.location)
            )
        )

        return (await self.session.execute(query)).scalar()

    async def get_applicant_by_edu_num(
            self,
            edu_institution_id: int,
            edu_number: str
    ):
        query = alch.select(User).where(
            User.is_applicant,
            Applicant.edu_number == edu_number,
            Applicant.edu_institution_id == edu_institution_id
        )

        query = (
            query
            .join(User.applicant)
            .options(
                selectinload(User.applicant),
                selectinload(User.location)
            )
        )

        return (await self.session.execute(query)).scalar()

    async def get_applicants_by_fullname(
            self,
            edu_institution_id: int,
            birthdate: date = None,
            only_verified: bool = False,
            location_id: int = None,
            q: str = None,
            start: int = None,
            end: int = None
    ) -> Sequence[User | None]:
        query = alch.select(User).where(
            User.is_applicant,
            Applicant.edu_institution_id == edu_institution_id
        )

        query = await self._get_users_by_fullname_query(
            query=query,
            birthdate=birthdate,
            only_verified=only_verified,
            location_id=location_id,
            q=q
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
    
    async def count_applicants_by_fullname(
            self,
            edu_institution_id: int,
            birthdate: date = None,
            only_verified: bool = False,
            location_id: int = None,
            q: str = None
    ) -> int:
        query = alch.select(alch.func.count()).select_from(User).where(
            User.is_applicant,
            Applicant.edu_institution_id == edu_institution_id
        )

        query = await self._get_users_by_fullname_query(
            query=query,
            birthdate=birthdate,
            only_verified=only_verified,
            location_id=location_id,
            q=q
        )

        query = query.join(User.applicant)

        result = await self.session.execute(query)
        return result.scalar()
