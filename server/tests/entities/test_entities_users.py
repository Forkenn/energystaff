import pytest
from src.users.models import User, Applicant, Employer, EduWorker
from src.companies.models import Company
from src.tools.models import EduInstitution, EduLevel, Location

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    """Direct user create test"""
    user = User(email="test@example.com", surname="Doe", name="John", hashed_password="pwd")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_unique_email_constraint(db_session: AsyncSession):
    """Test unique email User"""
    user1 = User(email="unique@example.com", surname="User", name="One", hashed_password="pwd")
    user2 = User(email="unique@example.com", surname="User", name="Two", hashed_password="pwd")

    db_session.add(user1)
    await db_session.commit()

    db_session.add(user2)
    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_user_applicant_relationship(db_session: AsyncSession):
    """Test User <-> Applicant"""
    user = User(email="applicant@example.com", name="App", surname="Test", hashed_password="pwd", is_applicant=True)
    applicant = Applicant(user=user)
    db_session.add(applicant)
    await db_session.commit()
    await db_session.refresh(applicant)

    assert applicant.user.email == "applicant@example.com"


@pytest.mark.asyncio
async def test_delete_applicant(db_session: AsyncSession):
    """Test cascade delete User -> Applicant"""
    user = User(email="applicant@example.com", name="App", surname="Test", hashed_password="pwd", is_applicant=True)
    user.applicant = Applicant()
    db_session.add(user)
    await db_session.commit()

    await db_session.delete(user)
    await db_session.commit()

    applicant_in_db = await db_session.get(Applicant, user.id)
    assert applicant_in_db is None


@pytest.mark.asyncio
async def test_user_employer_relationship(db_session: AsyncSession):
    """Test User <-> Employer"""
    company = Company(name="CompanyX", inn="123456789012")
    db_session.add(company)
    await db_session.commit()

    user = User(email="employer@example.com", name="Emp", surname="Test", hashed_password="pwd", is_employer=True)
    employer = Employer(user=user, company_id=company.id)
    db_session.add(employer)
    await db_session.commit()
    await db_session.refresh(employer)

    assert employer.user.email == "employer@example.com"
    assert employer.company_id == 1


@pytest.mark.asyncio
async def test_delete_employer(db_session: AsyncSession):
    """Test cascade delete User -> Employer"""
    company = Company(name="CompanyX", inn="123456789012")
    db_session.add(company)
    await db_session.commit()

    user = User(email="employer@example.com", name="Emp", surname="Test", hashed_password="pwd", is_employer=True)
    employer = Employer(user=user, company_id=company.id)
    db_session.add(employer)
    await db_session.commit()
    await db_session.refresh(employer)

    await db_session.delete(user)
    await db_session.commit()

    employer_in_db = await db_session.get(Employer, user.id)
    assert employer_in_db is None


@pytest.mark.asyncio
async def test_delete_employer_company(db_session: AsyncSession):
    """Test cascade delete User -> Employer -> Company"""
    company = Company(name="CompanyX", inn="123456789012")
    db_session.add(company)
    await db_session.commit()

    user = User(email="employer@example.com", name="Emp", surname="Test", hashed_password="pwd", is_employer=True)
    employer = Employer(user=user, company_id=company.id)
    db_session.add(employer)
    await db_session.commit()
    await db_session.refresh(employer)

    await db_session.delete(company)
    await db_session.commit()
    await db_session.refresh(user)

    user_in_db = await db_session.get(Employer, user.id)
    assert user_in_db is None


@pytest.mark.asyncio
async def test_user_edu_worker_relationship(db_session: AsyncSession):
    """Test User <-> EduWorker"""
    edu = EduInstitution(name="Grand Test University")
    db_session.add(edu)
    await db_session.commit()

    user = User(email="edu@example.com", name="Edu", surname="Test", hashed_password="pwd", is_edu=True)
    worker = EduWorker(user=user, edu_institution_id=edu.id)
    db_session.add(worker)
    await db_session.commit()
    await db_session.refresh(worker)

    assert worker.user.email == "edu@example.com"
    assert worker.edu_institution_id == 1


@pytest.mark.asyncio
async def test_delete_edu_worker(db_session: AsyncSession):
    """Test cascade delete User -> EduWorker"""
    edu = EduInstitution(name="Grand Test University")
    db_session.add(edu)
    await db_session.commit()

    user = User(email="edu@example.com", name="Edu", surname="Test", hashed_password="pwd", is_edu=True)
    worker = EduWorker(user=user, edu_institution_id=edu.id)
    db_session.add(worker)
    await db_session.commit()
    await db_session.refresh(worker)

    await db_session.delete(user)
    await db_session.commit()

    edu_worker_in_db = await db_session.get(EduWorker, user.id)
    assert edu_worker_in_db is None


@pytest.mark.asyncio
async def test_set_null_edu_institution(db_session: AsyncSession):
    """Test SET NULL for edu_institution_id on EduInstitution deletion"""
    edu = EduInstitution(name="Grand Test University")
    db_session.add(edu)
    await db_session.commit()

    user = User(email="applicant@example.com", name="App", surname="Test", hashed_password="pwd", is_applicant=True)
    user.applicant = Applicant(edu_institution_id=edu.id)
    db_session.add(user)
    await db_session.commit()

    await db_session.delete(edu)
    await db_session.commit()

    await db_session.refresh(user.applicant)
    assert user.applicant.edu_institution_id is None


@pytest.mark.asyncio
async def test_set_null_edu_levels(db_session: AsyncSession):
    """Test SET NULL for edu_level_id on EduLevel deletion"""
    edu_level = EduLevel(name="Tested")
    db_session.add(edu_level)
    await db_session.commit()

    user = User(email="applicant@example.com", name="App", surname="Test", hashed_password="pwd", is_applicant=True)
    user.applicant = Applicant(user=user, edu_level_id=edu_level.id)
    db_session.add(user)
    await db_session.commit()

    await db_session.delete(edu_level)
    await db_session.commit()

    await db_session.refresh(user.applicant)
    assert user.applicant.edu_level_id is None


@pytest.mark.asyncio
async def test_set_null_location(db_session: AsyncSession):
    """Test SET NULL for location_id on Location deletion"""
    location = Location(name='TestCity')
    db_session.add(location)
    await db_session.commit()

    user = User(email="applicant@example.com", name="App", surname="Test", hashed_password="pwd", location_id=location.id)
    db_session.add(user)
    await db_session.commit()

    await db_session.delete(location)
    await db_session.commit()

    await db_session.refresh(user)
    assert user.location_id is None
