import pytest_asyncio

import sqlalchemy as alch

from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)

from src.database import Base

from src.core.repositories.user import UserRepository
from src.core.services.user import UserService
from src.core.repositories.vacancy import VacancyRepository
from src.core.services.vacancy import VacancyService
from src.core.repositories.company import CompanyRepository
from src.core.services.company import CompanyService
from src.core.repositories.negotiation import NegotiationRepository
from src.core.services.negotiation import NegotiationService
from src.core.repositories.recommendation import RecommendationRepository
from src.core.services.recommendation import RecommendationService
from src.core.repositories.storage import StorageRepository
from src.core.services.storage import StorageService

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True, future=True
)

AsyncSessionLocal: AsyncSession = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(alch.text("PRAGMA foreign_keys=ON"))
        yield session
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def user_service(db_session: AsyncSession):
    user_repo = UserRepository(session=db_session)
    user_service = UserService(user_repo=user_repo)

    yield user_service


@pytest_asyncio.fixture
async def vacancy_service(db_session: AsyncSession):
    vacancy_repo = VacancyRepository(session=db_session)
    vacancy_service = VacancyService(vacancy_repo=vacancy_repo)

    yield vacancy_service


@pytest_asyncio.fixture
async def company_service(db_session: AsyncSession):
    company_repo = CompanyRepository(session=db_session)
    company_service = CompanyService(company_repo=company_repo)

    yield company_service


@pytest_asyncio.fixture
async def negotiation_service(vacancy_service: VacancyService):
    negotiation_repo = NegotiationRepository(session=vacancy_service.repository.session)
    negotiation_service = NegotiationService(
        negotiation_repo=negotiation_repo,
        vacancy_service=vacancy_service
    )

    yield negotiation_service


@pytest_asyncio.fixture
async def storage_service(db_session: AsyncSession):
    storage_repo = StorageRepository(session=db_session)
    storage_service = StorageService(storage_repo=storage_repo)

    yield storage_service


@pytest_asyncio.fixture
async def recommendation_service(storage_service: StorageService):
    recommendation_repo = RecommendationRepository(session=storage_service.repository.session)
    recommendation_service = RecommendationService(
        recommendation_repo=recommendation_repo,
        storage_service=storage_service
    )

    yield recommendation_service
