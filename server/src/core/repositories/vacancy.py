import sqlalchemy as alch

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.core.repositories.common import CommonRepository
from src.vacancies.models import (
    Vacancy, EmploymentSchedule, EmploymentFormat, EmploymentType
)
from src.companies.models import Company
from src.negotiations.models import Negotiation


class VacancyRepository(CommonRepository[Vacancy]):
    def __init__(self, session: AsyncSession):
        super().__init__(Vacancy, session)

    async def get_full(self, id: int) -> Vacancy | None:
        query = (
            alch.select(Vacancy)
            .where(Vacancy.id == id)
            .options(
                joinedload(Vacancy.vacancy_formats),
                joinedload(Vacancy.vacancy_schedules),
                joinedload(Vacancy.vacancy_types),
                selectinload(Vacancy.company)
            )
        )

        return (await self.session.execute(query)).scalar()
    
    async def refresh_fields(self, obj: Vacancy):
        await self.session.refresh(
            obj, ('vacancy_formats', 'vacancy_schedules', 'vacancy_types')
        )
    
    async def get_vacancy_fields(
            self,
            schedules_ids: list[int] = [],
            types_ids: list[int] = [],
            formats_ids: list[int] = []
    ) -> dict[str, list]:
        result: dict = {
            'vacancy_schedules': [],
            'vacancy_formats': [],
            'vacancy_types': []
        }

        query = (
            alch.select(EmploymentSchedule)
            .where(EmploymentSchedule.id.in_(schedules_ids))
        )
        result['vacancy_schedules'] = (await self.session.execute(query)).scalars().all()

        query = (
            alch.select(EmploymentFormat)
            .where(EmploymentFormat.id.in_(formats_ids))
        )
        result['vacancy_formats'] = (await self.session.execute(query)).scalars().all()

        query =  (
            alch.select(EmploymentType)
            .where(EmploymentType.id.in_(types_ids))
        )
        result['vacancy_types'] = (await self.session.execute(query)).scalars().all()
        return result
    
    async def create(
            self,
            data: dict,
            schedules_ids: list[int] = [],
            types_ids: list[int] = [],
            formats_ids: list[int] = []
    ) -> Vacancy:
        fields = await self.get_vacancy_fields(schedules_ids, types_ids, formats_ids)
        new_vacancy = self.model(**data)

        for field, value in fields.items():
            setattr(new_vacancy, field, value)

        self.session.add(new_vacancy)
        await self.session.commit()
        return new_vacancy

    async def update(
            self,
            vacancy: Vacancy,
            data: dict,
            schedules_ids: list[int] = [],
            types_ids: list[int] = [],
            formats_ids: list[int] = []
    ) -> None:
        fields = await self.get_vacancy_fields(schedules_ids, types_ids, formats_ids)

        for field, value in data.items():
            setattr(vacancy, field, value)

        vacancy.vacancy_formats = fields['vacancy_formats']
        vacancy.vacancy_schedules = fields['vacancy_schedules']
        vacancy.vacancy_types = fields['vacancy_types']

        await self.session.commit()
    
    async def get_vacancies_plain(
            self, requester_id: int, start: int, end: int
    ) -> Sequence[dict | None]:
        query = (
            alch.select(
                Vacancy.id,
                Vacancy.position,
                Vacancy.salary,
                Vacancy.company_id,
                Vacancy.author_id,
                Company.name.label("company_name"),
                Negotiation.id.label("negotiation_id"),
                Negotiation.status.label("negotiation_status")
            )
            .join(Company, Vacancy.company_id == Company.id)
            .join(
                Negotiation,
                alch.and_(
                    Negotiation.vacancy_id == Vacancy.id,
                    Negotiation.applicant_id == requester_id
                ),
                isouter=True
            )
            .order_by(Vacancy.timestamp.desc())
            .slice(start, end)
        )

        result = await self.session.execute(query)
        return result.mappings().all()
    
    async def count_vacancies(self) -> int:
        query = (
            alch.select(alch.func.count())
            .select_from(Vacancy)
        )

        result = await self.session.execute(query)
        return result.scalar()
