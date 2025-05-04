import sqlalchemy as alch

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, defer

from src.core.repositories.common import CommonRepository
from src.vacancies.models import EmploymentFormat, EmploymentType
from src.resume.models import Resume
from src.negotiations.models import Negotiation
from src.users.models import User


class ResumeRepository(CommonRepository[Resume]):
    def __init__(self, session: AsyncSession):
        super().__init__(Resume, session)

    async def get_by_uid(self, uid: int) -> Resume | None:
        query = (
            alch.select(Resume)
            .where(Resume.user_id == uid)
        )

        return (await self.session.execute(query)).scalar()

    async def get_full(self, id: int) -> Resume | None:
        query = (
            alch.select(Resume)
            .where(Resume.id == id)
            .options(
                joinedload(Resume.resume_formats),
                joinedload(Resume.resume_types)
            )
        )

        return (await self.session.execute(query)).scalar()
    
    async def get_full_with_recommendation(self, id: int) -> dict | None:
        pass

    async def get_full_by_uid(self, uid: int, user_info: bool = False) -> Resume | None:
        query = (
            alch.select(Resume)
            .where(Resume.user_id == uid)
            .options(
                joinedload(Resume.resume_formats),
                joinedload(Resume.resume_types)
            )
        )

        if user_info:
            query = query.options(
                joinedload(Resume.user).joinedload(User.applicant),
                joinedload(Resume.user).joinedload(User.location)
            )

        return (await self.session.execute(query)).scalar()
    
    async def get_full_with_recommendation_by_uid(self, uid: int) -> dict | None:
        pass
    
    async def get_resume_by_uid_secured(
            self, employer_id: int, uid: int, user_info: bool = False
    ) -> Resume | None:
        exists_criteria = (
            alch.select(Negotiation)
            .where(
                Negotiation.applicant_id == uid,
                Negotiation.employer_id == employer_id
            )
            .exists()
        )

        query = (
            alch.select(Resume)
            .where(
                Resume.user_id == uid,
                exists_criteria
            )
            .options(
                joinedload(Resume.resume_formats),
                joinedload(Resume.resume_types)
            )
        )

        if user_info:
            query = query.options(
                joinedload(Resume.user).joinedload(User.applicant),
                joinedload(Resume.user).joinedload(User.location)
            )

        return (await self.session.execute(query)).scalar()
    
    async def refresh_fields(self, obj: Resume):
        await self.session.refresh(
            obj, ('resume_formats', 'resume_types')
        )
    
    async def get_resume_fields(
            self,
            types_ids: list[int] = [],
            formats_ids: list[int] = []
    ) -> dict[str, list]:
        result: dict = {
            'resume_formats': [],
            'resume_types': []
        }

        query = (
            alch.select(EmploymentFormat)
            .where(EmploymentFormat.id.in_(formats_ids))
        )
        result['resume_formats'] = (await self.session.execute(query)).scalars().all()

        query =  (
            alch.select(EmploymentType)
            .where(EmploymentType.id.in_(types_ids))
        )
        result['resume_types'] = (await self.session.execute(query)).scalars().all()
        return result
    
    async def create(
            self,
            data: dict,
            types_ids: list[int] = [],
            formats_ids: list[int] = []
    ) -> Resume:
        fields = await self.get_resume_fields(types_ids, formats_ids)
        new_vacancy = self.model(**data)

        for field, value in fields.items():
            setattr(new_vacancy, field, value)

        self.session.add(new_vacancy)
        await self.session.commit()
        return new_vacancy

    async def update(
            self,
            resume: Resume,
            data: dict,
            types_ids: list[int] = [],
            formats_ids: list[int] = []
    ) -> None:
        fields = await self.get_resume_fields(types_ids, formats_ids)

        for field, value in data.items():
            setattr(resume, field, value)

        resume.resume_formats = fields['resume_formats']
        resume.resume_types = fields['resume_types']

        await self.session.commit()

    async def exists_by_uid(self, uid: int) -> bool:
        query = alch.select(1).where(Resume.user_id == uid)
        result = await self.session.scalar(query)
        return result is not None
