import pytest
import pytest_asyncio

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User, Applicant, Employer, EduWorker
from src.users.schemas import SUserEdit
from src.companies.models import Company
from src.tools.models import EduInstitution, Location, EduLevel

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
async def test_create_applicant(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()
    
    await user_service.create_applicant(user)
    await db_session.refresh(user, attribute_names=('applicant',))

    assert user.applicant.user_id == user.id


@pytest.mark.asyncio
async def test_create_employer(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()

    company = Company(name='CompanyX')
    db_session.add(company)
    await db_session.commit()
    
    await user_service.create_employer(user, company.id)
    await db_session.refresh(user, attribute_names=('employer',))

    assert user.employer.company_id == company.id


@pytest.mark.asyncio
async def test_create_edu(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()

    edu = EduInstitution(name='EduX')
    db_session.add(edu)
    await db_session.commit()
    
    await user_service.create_edu_worker(user, edu.id)
    await db_session.refresh(user, attribute_names=('edu_worker',))

    assert user.edu_worker.edu_institution_id == edu.id


@pytest.mark.asyncio
async def test_verify_user(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()
    
    await user_service.verify_user_by_id(user.id)
    await db_session.refresh(user)

    assert user.is_verified == True


@pytest.mark.asyncio
async def test_unverify_user(db_session: AsyncSession, user: User, user_service: UserService):
    user.is_verified = True
    db_session.add(user)
    await db_session.commit()
    
    await user_service.unverify_user_by_id(user.id)
    await db_session.refresh(user)

    assert user.is_verified == False


@pytest.mark.asyncio
async def test_deactivate_user(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()
    
    await user_service.deactivate_user_by_id(user.id)
    await db_session.refresh(user)

    assert user.is_active == False


@pytest.mark.asyncio
async def test_activate_user(db_session: AsyncSession, user: User, user_service: UserService):
    user.is_active = False
    db_session.add(user)
    await db_session.commit()
    
    await user_service.activate_user_by_id(user.id)
    await db_session.refresh(user)

    assert user.is_active == True


@pytest.mark.asyncio
async def test_get_user(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()

    user_test = await user_service.get_by_id(user.id)
    assert user_test.id == user.id


@pytest.mark.asyncio
async def test_get_user_full(db_session: AsyncSession, user: User, user_service: UserService):
    db_session.add(user)
    await db_session.commit()

    company = Company(name='CompanyX')
    edu = EduInstitution(name='EduX')
    db_session.add_all([company, edu])
    await db_session.commit()

    applicant = Applicant(user=user)
    employer = Employer(user=user, company_id=company.id)
    edu_worker = EduWorker(user=user, edu_institution_id=edu.id)
    db_session.add_all([applicant, employer, edu_worker])
    await db_session.commit()

    user_test = await user_service.get_full_by_id(user.id)
    assert user_test.applicant
    assert user_test.employer.company_id == company.id
    assert user_test.edu_worker.edu_institution_id == edu.id


@pytest.mark.asyncio
async def test_update_user(db_session: AsyncSession, user: User, user_service: UserService):
    location = Location(name='Test')
    location_1 = Location(name='Test1')
    edu_level = EduLevel(name='Level')
    edu_level_1 = EduLevel(name='Level_1')
    company = Company(name='CompanyX')
    edu = EduInstitution(name='Edu')
    edu_1 = EduInstitution(name='Edu_1')
    db_session.add_all([location, location_1, company, edu, edu_1, edu_level, edu_level_1])
    await db_session.commit()

    user.last_name = 'TestLast'
    user.birthdate = date(1993, 2, 10)
    user.sex = False
    user.location_id = location.id
    user.is_edu = False
    user.is_employer = False
    user.is_applicant = False
    user.is_verified = False

    db_session.add(user)
    await db_session.commit()

    applicant = Applicant(user=user, edu_institution_id=edu.id, edu_status='pending', edu_level_id=edu_level.id)
    employer = Employer(user=user, company_id=company.id)
    edu_worker = EduWorker(user=user, edu_institution_id=edu.id)
    db_session.add_all([applicant, employer, edu_worker])
    await db_session.commit()

    new_data = {
        'email': "testNew@example.com",
        'surname': "DoeNew",
        'name': "JohnNew",
        'hashed_password': "pwdNew",
        'is_active': False,
        'is_superuser': False,
        'last_name': 'TestLastNew',
        'birthdate': date(1994, 3, 11),
        'sex': True,
        'location_id': location_1.id,
        'is_edu': True,
        'is_employer': True,
        'is_applicant': True,
        'is_verified': True,
    }

    await user_service.update_user(user, SUserEdit(**new_data))
    user = await user_service.get_full_by_id(user.id)

    assert user.email == "test@example.com"
    assert user.surname == "DoeNew"
    assert user.name == "JohnNew"
    assert user.hashed_password == "pwd"
    assert user.is_active == True
    assert user.is_superuser == True
    assert user.last_name == 'TestLastNew'
    assert user.birthdate == date(1994, 3, 11)
    assert user.sex == True
    assert user.location_id == location_1.id
    assert user.is_edu == False
    assert user.is_employer == False
    assert user.is_applicant == False
    assert user.is_verified == False
