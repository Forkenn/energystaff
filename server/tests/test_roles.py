import pytest
import pytest_asyncio
import sqlalchemy as alch

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.database import Base
from src.exceptions import ForbiddenException
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User, Applicant, Employer, EduWorker
from src.tools.models import EduInstitution, EduLevel, Location
from src.companies.models import Company

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture
async def async_session():
    async with AsyncSessionLocal() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(alch.text("PRAGMA foreign_keys=ON"))
        yield session
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def user():
    user = User(
        id=1,
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq",
        is_active=True,
        is_superuser=True
    )
    yield user

@pytest.mark.asyncio
async def test_single_role(async_session: AsyncSession, user: User):
    async_session.add(user)
    await async_session.commit()
    current_active = RoleManager(SystemRole.ACTIVE)
    user_test = await current_active(user=user, session=async_session)
    assert user_test == user

@pytest.mark.asyncio
async def test_single_role_missing(async_session: AsyncSession, user: User):
    async_session.add(user)
    await async_session.commit()
    current_active = RoleManager(SystemRole.EDU_WORKER)
    with pytest.raises(ForbiddenException):
        await current_active(user=user, session=async_session)

@pytest.mark.asyncio
async def test_multiple_role(async_session: AsyncSession, user: User):
    async_session.add(user)
    await async_session.commit()
    current_active = RoleManager(SystemRole.ACTIVE, SystemRole.SUPERUSER)
    user_test = await current_active(user=user, session=async_session)
    assert user_test == user

@pytest.mark.asyncio
async def test_multiple_role_missing(async_session: AsyncSession, user: User):
    async_session.add(user)
    await async_session.commit()
    current_active = RoleManager(SystemRole.EDU_WORKER, SystemRole.VERIFIED)
    with pytest.raises(ForbiddenException):
        await current_active(user=user, session=async_session)

@pytest.mark.asyncio
async def test_multiple_role_one_missing(async_session: AsyncSession, user: User):
    async_session.add(user)
    await async_session.commit()
    current_active = RoleManager(
        SystemRole.EDU_WORKER, SystemRole.SUPERUSER, SystemRole.ACTIVE
    )
    with pytest.raises(ForbiddenException):
        await current_active(user=user, session=async_session)
