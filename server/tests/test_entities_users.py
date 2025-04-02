import pytest
import pytest_asyncio
import sqlalchemy as alch

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.database import Base
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

@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession):
    """Direct user create test"""
    user = User(
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq"
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"

@pytest.mark.asyncio
async def test_unique_email_constraint(async_session: AsyncSession):
    """Test email User"""
    user1 = User(
        email="unique@example.com",
        surname="User",
        name="One",
        hashed_password="asdasdafdsawerq"
    )
    user2 = User(
        email="unique@example.com",
        surname="User",
        name="Two",
        hashed_password="asdasdafdsawerq"
    )

    async_session.add(user1)
    await async_session.commit()

    async_session.add(user2)
    with pytest.raises(alch.exc.IntegrityError):
        await async_session.commit()

@pytest.mark.asyncio
async def test_create_applicant(async_session: AsyncSession):
    """One-to-One test between User and Applicant"""
    user = User(
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq"
    )
    user.applicant = Applicant()
    async_session.add(user)
    await async_session.commit()
    
    assert user.applicant is not None

@pytest.mark.asyncio
async def test_delete_applicant(async_session: AsyncSession):
    """Test cascade delete User -> Applicant"""
    user = User(
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq"
    )
    user.applicant = Applicant()
    async_session.add(user)
    await async_session.commit()

    await async_session.delete(user)
    await async_session.commit()

    applicant_in_db = await async_session.get(Applicant, user.id)
    assert applicant_in_db is None

@pytest.mark.asyncio
async def test_create_edu_worker(async_session: AsyncSession):
    """Test EduWorker creation and connection to User and EduInstitution"""
    user = User(
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq"
    )
    edu_inst = EduInstitution(name="Grand Test University")
    async_session.add(edu_inst)
    await async_session.commit()
    
    edu_worker = EduWorker(user=user, edu_institution_id=edu_inst.id)
    async_session.add(user)
    async_session.add(edu_worker)
    await async_session.commit()
    
    assert edu_worker.user_id == user.id
    assert edu_worker.edu_institution_id == edu_inst.id
    assert user.edu_worker is not None

@pytest.mark.asyncio
async def test_delete_edu_worker(async_session: AsyncSession):
    """Test cascade delete User -> EduWorker"""
    user = User(
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq"
    )
    edu_inst = EduInstitution(name="Grand Test University")
    async_session.add(edu_inst)
    await async_session.commit()

    edu_worker = EduWorker(user=user, edu_institution_id=edu_inst.id)
    async_session.add(user)
    async_session.add(edu_worker)
    await async_session.commit()

    await async_session.delete(user)
    await async_session.commit()

    edu_worker_in_db = await async_session.get(EduWorker, user.id)
    assert edu_worker_in_db is None

@pytest.mark.asyncio
async def test_create_employer(async_session: AsyncSession):
    """Test the creation of Employer and the relationship to User and Company"""
    user = User(
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq"
    )
    company = Company(name="Grand Test Company")
    async_session.add(company)
    await async_session.commit()

    employer = Employer(user=user, company_id=company.id)
    async_session.add(user)
    async_session.add(employer)
    await async_session.commit()
    
    assert employer.user_id == user.id
    assert employer.company_id == 1
    assert user.employer is not None

@pytest.mark.asyncio
async def test_delete_employer(async_session: AsyncSession):
    """Test cascade delete User -> Employer"""
    user = User(
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq"
    )
    company = Company(name="Grand Test Company")
    async_session.add(company)
    await async_session.commit()

    employer = Employer(user=user, company_id=company.id)
    async_session.add(user)
    async_session.add(employer)
    await async_session.commit()

    await async_session.delete(user)
    await async_session.commit()

    employer_in_db = await async_session.get(Employer, user.id)
    assert employer_in_db is None

@pytest.mark.asyncio
async def test_unique_companies_names(async_session: AsyncSession):
    """Test unique companies names"""
    company1 = Company(name="Grand Test Company")
    company2 = Company(name="Grand Test Company")

    async_session.add(company1)
    await async_session.commit()

    async_session.add(company2)
    with pytest.raises(alch.exc.IntegrityError):
        await async_session.commit()

@pytest.mark.asyncio
async def test_set_null_edu_institution(async_session: AsyncSession):
    """Test SET NULL for edu_institution_id on EduInstitution deletion"""
    edu_inst = EduInstitution(name="Grand Test University")
    async_session.add(edu_inst)
    await async_session.commit()

    user = User(
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq"
    )

    user.applicant = Applicant(user=user, edu_institution_id=edu_inst.id)
    async_session.add(user)
    await async_session.commit()

    await async_session.delete(edu_inst)
    await async_session.commit()

    await async_session.refresh(user.applicant)
    assert user.applicant.edu_institution_id is None

@pytest.mark.asyncio
async def test_set_null_edu_levels(async_session: AsyncSession):
    """Test SET NULL for edu_level_id on EduLevel deletion"""
    edu_level = EduLevel(name="Tested")
    async_session.add(edu_level)
    await async_session.commit()

    user = User(
        email="test@example.com",
        surname="Doe",
        name="John",
        hashed_password="asdasdafdsawerq"
    )

    user.applicant = Applicant(user=user, edu_level_id=edu_level.id)
    async_session.add(user)
    await async_session.commit()

    await async_session.delete(edu_level)
    await async_session.commit()

    await async_session.refresh(user.applicant)
    assert user.applicant.edu_level_id is None
