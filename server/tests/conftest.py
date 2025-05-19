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
