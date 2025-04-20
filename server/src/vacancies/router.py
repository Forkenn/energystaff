from fastapi import APIRouter, Depends

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.responses import openapi_404, openapi_403, openapi_204, response_204
from src.exceptions import NotFoundException, NotAllowedException
from src.deps import get_schedule_service, get_format_service, get_type_service
from src.core.services.catalog import CatalogService
from src.core.schemas.catalog import SBaseCatalogRead
from src.core.schemas.common import SBaseQueryBody, SBaseQueryCountResponse
from src.core.dao.common import fetch_all, fetch_one
from src.core.dao.vacancies import fetch_vacancies_cards, count_vacancies
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.vacancies.models import (
    Vacancy, EmploymentFormat, EmploymentSchedule, EmploymentType
)
from src.vacancies.schemas import SVacancyCreate, SVacancyRead, SVacanciesPreview

router = APIRouter(prefix='/vacancies', tags=['Vacancies'])

current_user = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE)
current_employer = RoleManager(SystemRole.VERIFIED, SystemRole.EMPLOYER)
current_superuser = RoleManager(SystemRole.SUPERUSER)

@router.get('/schedules')
async def get_vacancies_schedules(
        schedule_service: CatalogService = Depends(get_schedule_service)
) -> SBaseCatalogRead:
    results = await schedule_service.get_all()
    return {'count': len(results), 'items': results}

@router.get('/formats')
async def get_vacancies_formats(
        format_service: CatalogService = Depends(get_format_service)
) -> SBaseCatalogRead:
    results = await format_service.get_all()
    return {'count': len(results), 'items': results}

@router.get('/types')
async def get_vacancies_types(
        type_service: CatalogService = Depends(get_type_service)
) -> SBaseCatalogRead:
    results = await type_service.get_all()
    return {'count': len(results), 'items': results}

@router.get('')
async def get_vacancies_cards(
    data: SBaseQueryBody = Depends(),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> SVacanciesPreview:
    vacancies = await fetch_vacancies_cards(session, user.id, data.start, data.end)
    return {'count': len(vacancies), 'items': vacancies}

@router.get('/count')
async def get_vacancies_count(
    q: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> SBaseQueryCountResponse:
    count = await count_vacancies(session)
    return {'count': count}

@router.get('/{id}', responses={**openapi_404, **openapi_403})
async def get_vacancy_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> SVacancyRead:
    vacancy: Vacancy = await fetch_one(
        session,
        Vacancy,
        where=(Vacancy.id == id,),
        options=(
            joinedload(Vacancy.vacancy_formats),
            joinedload(Vacancy.vacancy_schedules),
            joinedload(Vacancy.vacancy_types)
        )
    )

    if not vacancy:
        raise NotFoundException()

    return vacancy

@router.delete('/{id}', responses={**openapi_404, **openapi_403, **openapi_204})
async def delete_vacancy_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_employer)
):
    vacancy: Vacancy = await fetch_one(
        session,
        Vacancy,
        where=(Vacancy.id == id,)
    )

    if not vacancy:
        raise NotFoundException()
    
    if vacancy.author_id != user.id:
        raise NotAllowedException()
    
    await session.delete(vacancy)
    await session.commit()

    return response_204

@router.post('', responses={**openapi_403})
async def add_vacancy(
    data: SVacancyCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_employer)
) -> SVacancyRead:
    formats = await fetch_all(
        session,
        EmploymentFormat,
        EmploymentFormat.id.in_(data.vacancy_formats_ids)
    )
    schedules = await fetch_all(
        session,
        EmploymentSchedule,
        EmploymentSchedule.id.in_(data.vacancy_schedules_ids)
    )
    types = await fetch_all(
        session,
        EmploymentType,
        EmploymentType.id.in_(data.vacancy_types_ids)
    )

    new_vacancy = Vacancy(
        position=data.position,
        specialization=data.specialization,
        salary=data.salary,
        description=data.description,
        company_id=user.employer.company_id,
        author_id=user.id
    )

    new_vacancy.vacancy_formats = formats
    new_vacancy.vacancy_schedules = schedules
    new_vacancy.vacancy_types = types

    session.add(new_vacancy)
    await session.commit()
    return new_vacancy

@router.post('/{id}', responses={**openapi_404, **openapi_403})
async def edit_vacancy_by_id(
        id: int,
        data: SVacancyCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_employer)
) -> SVacancyRead:
    vacancy: Vacancy = await fetch_one(
        session,
        Vacancy,
        where=(Vacancy.id == id,),
        options=(
            joinedload(Vacancy.vacancy_formats),
            joinedload(Vacancy.vacancy_schedules),
            joinedload(Vacancy.vacancy_types)
        )
    )
    if not vacancy:
        raise NotFoundException()
    
    if vacancy.author_id != user.id:
        raise NotAllowedException()
    
    formats = await fetch_all(
        session,
        EmploymentFormat,
        EmploymentFormat.id.in_(data.vacancy_formats_ids)
    )
    schedules = await fetch_all(
        session,
        EmploymentSchedule,
        EmploymentSchedule.id.in_(data.vacancy_schedules_ids)
    )
    types = await fetch_all(
        session,
        EmploymentType,
        EmploymentType.id.in_(data.vacancy_types_ids)
    )

    vacancy.position = data.position
    vacancy.specialization = data.specialization
    vacancy.description = data.description
    vacancy.salary = data.salary
    vacancy.vacancy_formats = formats
    vacancy.vacancy_schedules = schedules
    vacancy.vacancy_types = types
    await session.commit()
    
    return vacancy
