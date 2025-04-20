from fastapi import APIRouter, Depends

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.responses import openapi_404, openapi_403, openapi_204, response_204
from src.exceptions import NotFoundException, NotAllowedException
from src.deps import (
    get_schedule_service, get_format_service, get_type_service,
    get_vacancy_service
)
from src.core.services.catalog import CatalogService
from src.core.services.vacancy import VacancyService
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
        user: User = Depends(current_user),
        vacancy_service: VacancyService = Depends(get_vacancy_service)
) -> SVacanciesPreview:
    vacancies = await vacancy_service.get_vacancies_cards(
        user.id, data.start, data.end
    )
    return {'count': len(vacancies), 'items': vacancies}

@router.get('/count')
async def get_vacancies_count(
        q: str,
        user: User = Depends(current_user),
        vacancy_service: VacancyService = Depends(get_vacancy_service)
) -> SBaseQueryCountResponse:
    count = await vacancy_service.count_vacancies()
    return {'count': count}

@router.get('/{id}', responses={**openapi_404, **openapi_403})
async def get_vacancy_by_id(
        id: int,
        user: User = Depends(current_user),
        vacancy_service: VacancyService = Depends(get_vacancy_service)
) -> SVacancyRead:
    vacancy: Vacancy = await vacancy_service.get_full_vacancy(id)
    return vacancy

@router.delete('/{id}', responses={**openapi_404, **openapi_403, **openapi_204})
async def delete_vacancy_by_id(
        id: int,
        user: User = Depends(current_employer),
        vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    await vacancy_service.delete_by_id(user.id, id)
    return response_204

@router.post('', responses={**openapi_403})
async def add_vacancy(
        data: SVacancyCreate,
        user: User = Depends(current_employer),
        vacancy_service: VacancyService = Depends(get_vacancy_service)
) -> SVacancyRead:
    new_vacancy = await vacancy_service.create_vacancy(user, data)
    return new_vacancy

@router.post('/{id}', responses={**openapi_404, **openapi_403})
async def edit_vacancy_by_id(
        id: int,
        data: SVacancyCreate,
        user: User = Depends(current_employer),
        vacancy_service: VacancyService = Depends(get_vacancy_service)
) -> SVacancyRead:
    vacancy: Vacancy = await vacancy_service.update_vacancy(user.id, id, data)
    return vacancy
