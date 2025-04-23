from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.core.repositories.user import UserRepository
from src.core.services.user import UserService
from src.core.repositories.company import CompanyRepository
from src.core.services.company import CompanyService
from src.core.repositories.vacancy import VacancyRepository
from src.core.services.vacancy import VacancyService
from src.core.repositories.resume import ResumeRepository
from src.core.services.resume import ResumeService
from src.core.repositories.catalog import CatalogRepository
from src.core.services.catalog import CatalogService
from src.core.repositories.recommendation import RecommendationRepository
from src.core.services.recommendation import RecommendationService
from src.core.repositories.negotiation import NegotiationRepository
from src.core.services.negotiation import NegotiationService
from src.core.repositories.storage import StorageRepository
from src.core.services.storage import StorageService

from src.tools.models import Location, EduInstitution, EduLevel
from src.vacancies.models import EmploymentFormat, EmploymentSchedule, EmploymentType

async def get_user_repo(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

async def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
    return UserService(repo)


async def get_company_repo(session: AsyncSession = Depends(get_async_session)) -> CompanyRepository:
    return CompanyRepository(session)

async def get_company_service(repo: CompanyRepository = Depends(get_company_repo)) -> CompanyService:
    return CompanyService(repo)


async def get_vacancy_repo(session: AsyncSession = Depends(get_async_session)) -> VacancyRepository:
    return VacancyRepository(session)

async def get_vacancy_service(repo: VacancyRepository = Depends(get_vacancy_repo)) -> VacancyService:
    return VacancyService(repo)


async def get_resume_repo(session: AsyncSession = Depends(get_async_session)) -> ResumeRepository:
    return ResumeRepository(session)

async def get_resume_service(repo: ResumeRepository = Depends(get_resume_repo)) -> ResumeService:
    return ResumeService(repo)


async def get_recomm_repo(session: AsyncSession = Depends(get_async_session)) -> RecommendationRepository:
    return RecommendationRepository(session)

async def get_recomm_service(repo: RecommendationRepository = Depends(get_recomm_repo)) -> RecommendationService:
    storage_repo = StorageRepository(repo.session)
    storage_service = StorageService(storage_repo)

    return RecommendationService(repo, storage_service)


async def get_neg_repo(session: AsyncSession = Depends(get_async_session)) -> NegotiationRepository:
    return NegotiationRepository(session)

async def get_neg_service(repo: NegotiationRepository = Depends(get_neg_repo)) -> NegotiationService:
    vacancy_repo = VacancyRepository(repo.session)
    vacancy_service = VacancyService(vacancy_repo)

    return NegotiationService(repo, vacancy_service)


# Catalog-tools
async def get_locations_repo(session: AsyncSession = Depends(get_async_session)) -> CatalogRepository:
    return CatalogRepository(Location, session)

async def get_locations_service(repo: CatalogRepository = Depends(get_locations_repo)) -> CatalogService:
    return CatalogService(Location, repo)


async def get_institutions_repo(session: AsyncSession = Depends(get_async_session)) -> CatalogRepository:
    return CatalogRepository(EduInstitution, session)

async def get_institutions_service(repo: CatalogRepository = Depends(get_institutions_repo)) -> CatalogService:
    return CatalogService(EduInstitution, repo)


async def get_levels_repo(session: AsyncSession = Depends(get_async_session)) -> CatalogRepository:
    return CatalogRepository(EduLevel, session)

async def get_levels_service(repo: CatalogRepository = Depends(get_levels_repo)) -> CatalogService:
    return CatalogService(EduLevel, repo)


# Catalog-employment
async def get_schedule_repo(session: AsyncSession = Depends(get_async_session)) -> CatalogRepository:
    return CatalogRepository(EmploymentSchedule, session)

async def get_schedule_service(repo: CatalogRepository = Depends(get_schedule_repo)) -> CatalogService:
    return CatalogService(EmploymentSchedule, repo)


async def get_type_repo(session: AsyncSession = Depends(get_async_session)) -> CatalogRepository:
    return CatalogRepository(EmploymentType, session)

async def get_type_service(repo: CatalogRepository = Depends(get_type_repo)) -> CatalogService:
    return CatalogService(EmploymentType, repo)


async def get_format_repo(session: AsyncSession = Depends(get_async_session)) -> CatalogRepository:
    return CatalogRepository(EmploymentFormat, session)

async def get_format_service(repo: CatalogRepository = Depends(get_format_repo)) -> CatalogService:
    return CatalogService(EmploymentFormat, repo)
