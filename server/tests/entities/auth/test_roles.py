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

from src.core.services.user import UserService


@pytest_asyncio.fixture
async def user():
    user = User(
        id=1,
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="pwd",
        is_active=True,
        is_superuser=True
    )
    yield user


@pytest.mark.asyncio
async def test_single_role(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()
    current_active = RoleManager(SystemRole.ACTIVE)
    user_test = await current_active(user=user, user_service=user_service)
    assert user_test == user


@pytest.mark.asyncio
async def test_single_role_missing(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()
    current_active = RoleManager(SystemRole.EDU_WORKER)
    with pytest.raises(ForbiddenException):
        await current_active(user=user, user_service=user_service)


@pytest.mark.asyncio
async def test_multiple_role(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()
    current_active = RoleManager(SystemRole.ACTIVE, SystemRole.SUPERUSER)
    user_test = await current_active(user=user, user_service=user_service)
    assert user_test == user


@pytest.mark.asyncio
async def test_multiple_role_missing(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()
    current_active = RoleManager(SystemRole.EDU_WORKER, SystemRole.VERIFIED)
    with pytest.raises(ForbiddenException):
        await current_active(user=user, user_service=user_service)


@pytest.mark.asyncio
async def test_multiple_role_one_missing(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()
    current_active = RoleManager(
        SystemRole.EDU_WORKER, SystemRole.SUPERUSER, SystemRole.ACTIVE
    )
    with pytest.raises(ForbiddenException):
        await current_active(user=user, user_service=user_service)
