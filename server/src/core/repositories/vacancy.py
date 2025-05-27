import sqlalchemy as alch

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.repositories.common import CommonRepository
from src.vacancies.models import (
    Vacancy, EmploymentSchedule, EmploymentFormat, EmploymentType,
    vacancies_formats, vacancies_schedules, vacancies_types
)
from src.companies.models import Company
from src.negotiations.models import Negotiation
from src.tools.models import Location


class VacancyRepository(CommonRepository[Vacancy]):
    def __init__(self, session: AsyncSession):
        super().__init__(Vacancy, session)

    async def get_full(self, id: int) -> Vacancy | None:
        query = (
            alch.select(Vacancy)
            .where(Vacancy.id == id)
            .options(
                selectinload(Vacancy.vacancy_formats),
                selectinload(Vacancy.vacancy_schedules),
                selectinload(Vacancy.vacancy_types),
                selectinload(Vacancy.company),
                selectinload(Vacancy.location)
            )
        )

        return (await self.session.execute(query)).scalar()
    
    async def refresh_fields(self, obj: Vacancy):
        await self.session.refresh(
            obj, ('location', 'vacancy_formats', 'vacancy_schedules', 'vacancy_types')
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

    async def _vacancies_plain_query(
            self,
            requester_id: int,
            q: str = None,
            location_id: int = None,
            salary_from: int = None,
            salary_to: int = None,
            types_ids: list[int] = None,
            formats_ids: list[int] = None,
            schedules_ids: list[int] = None
    ) -> alch.Select:
        query = (
            alch.select(
                Vacancy.id,
                Vacancy.position,
                Vacancy.work_hours,
                Vacancy.salary,
                Vacancy.author_id,
                Vacancy.company_id,
                Vacancy.timestamp,
                Location.name.label("location_name"),
                Company.name.label("company_name"),
                Negotiation.id.label("negotiation_id"),
                Negotiation.status.label("negotiation_status")
            )
            .join(Company, Vacancy.company_id == Company.id)
            .join(
                Location,
                Vacancy.location_id == Location.id,
                isouter=True
            )
            .join(
                Negotiation,
                alch.and_(
                    Negotiation.vacancy_id == Vacancy.id,
                    Negotiation.applicant_id == requester_id
                ),
                isouter=True
            )
            .where(Company.is_verified)
        )

        if location_id is not None:
            query = query.where(Vacancy.location_id == location_id)

        if q:
            query = query.where(Vacancy.position.like(f'%{q}%'))

        if types_ids:
            query = query.join(vacancies_types).where(vacancies_types.c.type_id.in_(types_ids))

        if formats_ids:
            query = query.join(vacancies_formats).where(vacancies_formats.c.format_id.in_(formats_ids))

        if schedules_ids:
            query = query.join(vacancies_schedules).where(vacancies_schedules.c.schedule_id.in_(schedules_ids))

        if types_ids or formats_ids or schedules_ids:
            query = query.distinct()

        if salary_from is not None and salary_to is not None:
            query = query.where(Vacancy.salary.between(salary_from, salary_to))
            return query

        if salary_from is not None:
            query = query.where(Vacancy.salary >= salary_from)
            return query

        if salary_to is not None:
            query = query.where(Vacancy.salary <= salary_to)

        return query
    
    async def _vacancies_sort_date(
            self,
            query: alch.Select,
            desc: bool = True,
            start: int = None,
            end: int = None
    ) -> alch.Select:
        if desc:
            query = query.order_by(Vacancy.timestamp.desc())
        else:
            query = query.order_by(Vacancy.timestamp.asc())

        query = query.slice(start, end)
        return query
    
    async def _vacancies_sort_salary(
            self,
            query: alch.Select,
            desc: bool = True,
            start: int = None,
            end: int = None
    ) -> alch.Select:
        if desc:
            query = query.order_by(Vacancy.salary.desc())
        else:
            query = query.order_by(Vacancy.salary.asc())

        query = query.slice(start, end)
        return query
    
    async def get_vacancies_plain(
            self,
            requester_id: int,
            q: str = None,
            location_id: int = None,
            salary_from: int = None,
            salary_to: int = None,
            types_ids: list[int] = None,
            formats_ids: list[int] = None,
            schedules_ids: list[int] = None,
            sort_date: bool = True,
            desc: bool = True,
            start: int = None,
            end: int = None
    ) -> Sequence[dict | None]:
        query = await self._vacancies_plain_query(
            requester_id=requester_id,
            q=q,
            location_id=location_id,
            salary_from=salary_from,
            salary_to=salary_to,
            types_ids=types_ids,
            formats_ids=formats_ids,
            schedules_ids=schedules_ids
        )

        if sort_date:
            query = await self._vacancies_sort_date(query, desc, start, end)
        else:
            query = await self._vacancies_sort_salary(query, desc, start, end)

        result = await self.session.execute(query)
        return result.mappings().all()

    async def count_vacancies(
            self,
            q: str = None,
            location_id: int = None,
            salary_from: int = None,
            salary_to: int = None,
            types_ids: list[int] = None,
            formats_ids: list[int] = None,
            schedules_ids: list[int] = None
    ) -> int:
        query = (
            alch.select(alch.func.count())
            .select_from(Vacancy)
        )

        if location_id is not None:
            query = query.where(Vacancy.location_id == location_id)

        if q:
            query = query.where(Vacancy.position.like(f'%{q}%'))

        if types_ids:
            query = query.join(vacancies_types).where(
                vacancies_types.c.type_id.in_(types_ids)
            )

        if formats_ids:
            query = query.join(vacancies_formats).where(
                vacancies_formats.c.format_id.in_(formats_ids)
            )

        if schedules_ids:
            query = query.join(vacancies_schedules).where(
                vacancies_schedules.c.schedule_id.in_(schedules_ids)
            )

        if types_ids or formats_ids or schedules_ids:
            query = query.distinct()

        if salary_from is not None and salary_to is not None:
            query = query.where(Vacancy.salary.between(salary_from, salary_to))

        elif salary_from is not None:
            query = query.where(Vacancy.salary >= salary_from)

        elif salary_to is not None:
            query = query.where(Vacancy.salary <= salary_to)

        result = await self.session.execute(query)
        return result.scalar()
