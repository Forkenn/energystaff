import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import (
    NotFoundException, AlreadyExistException, WrongStateException,
    NotAllowedException
)
from src.users.models import User, Employer
from src.companies.models import Company
from src.negotiations.models import Negotiation, NegotiationStatus
from src.resume.models import Resume
from src.tools.models import Location
from src.vacancies.models import (
    Vacancy, EmploymentFormat, EmploymentSchedule, EmploymentType
)

from src.core.services.negotiation import NegotiationService


async def create_vacancies_fields(session: AsyncSession):
    format = EmploymentFormat(name='test')
    type = EmploymentType(name='test')
    schedule = EmploymentSchedule(name='test')

    session.add_all([format, type, schedule])
    await session.commit()

    return (format, type, schedule)


async def create_vacancy(session: AsyncSession, user: User, location: Location):
    fields = await create_vacancies_fields(session)
    vacancy = Vacancy(
        position='position_test',
        specialization='specialization_test',
        description='description_test',
        work_hours='work_hours_test',
        salary=60000,
        vacancy_formats=[fields[0]],
        vacancy_types=[fields[1]],
        vacancy_schedules=[fields[2]],
        location_id=location.id,
        author_id=user.id,
        company_id=user.employer.company_id
    )
    session.add(vacancy)
    await session.commit()
    return vacancy


@pytest.mark.asyncio
async def test_get_negotiations_applicant(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)
    vacancy_1 = await create_vacancy(db_session, employer, location)

    ng = Negotiation(
        applicant_id=applicant.id,
        vacancy_id=vacancy.id,
        employer_id=employer.id
    )
    ng_1 = Negotiation(
        applicant_id=applicant.id,
        vacancy_id=vacancy_1.id,
        employer_id=employer.id
    )

    db_session.add_all([ng, ng_1])
    await db_session.commit()

    data = await negotiation_service.get_negotiations_applicant(applicant.id, 0, 5)

    assert len(data) == 2
    assert data[0]['id'] == 1
    assert data[1]['id'] == 2


@pytest.mark.asyncio
async def test_count_negotiations_applicant(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)
    vacancy_1 = await create_vacancy(db_session, employer, location)

    ng = Negotiation(
        applicant_id=applicant.id,
        vacancy_id=vacancy.id,
        employer_id=employer.id
    )
    ng_1 = Negotiation(
        applicant_id=applicant.id,
        vacancy_id=vacancy_1.id,
        employer_id=employer.id
    )

    db_session.add_all([ng, ng_1])
    await db_session.commit()

    data = await negotiation_service.count_negotiations_applicant(applicant.id)
    assert data == 2

    data = await negotiation_service.count_negotiations_applicant(
        applicant.id, NegotiationStatus.ACCEPTED
    )
    assert data == 0


@pytest.mark.asyncio
async def test_get_negotiations_employer(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    resume = Resume(
        position='test',
        user_id = applicant.id,
        description='Test'
    )
    db_session.add_all([location, resume])
    await db_session.commit()

    applicant.location = location
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)
    vacancy_1 = await create_vacancy(db_session, employer, location)

    ng = Negotiation(
        applicant_id=applicant.id,
        vacancy_id=vacancy.id,
        employer_id=employer.id
    )
    ng_1 = Negotiation(
        applicant_id=applicant.id,
        vacancy_id=vacancy_1.id,
        employer_id=employer.id
    )

    db_session.add_all([ng, ng_1])
    await db_session.commit()

    data = await negotiation_service.get_negotiations_employer(employer.id, 0, 5)

    assert len(data) == 2
    assert data[0]['id'] == 1
    assert data[1]['id'] == 2


@pytest.mark.asyncio
async def test_count_negotiations_employer(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    applicant.location = location
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)
    vacancy_1 = await create_vacancy(db_session, employer, location)

    ng = Negotiation(
        applicant_id=applicant.id,
        vacancy_id=vacancy.id,
        employer_id=employer.id
    )
    ng_1 = Negotiation(
        applicant_id=applicant.id,
        vacancy_id=vacancy_1.id,
        employer_id=employer.id
    )

    db_session.add_all([ng, ng_1])
    await db_session.commit()

    data = await negotiation_service.count_negotiations_employer(employer.id)
    assert data == 2

    data = await negotiation_service.count_negotiations_employer(
        employer.id, NegotiationStatus.REJECTED
    )
    assert data == 0


@pytest.mark.asyncio
async def test_create_negotiation(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)

    ng = await negotiation_service.create_negotiation(vacancy.id, applicant.id)
    assert ng.id == 1
    assert ng.vacancy_id == vacancy.id


@pytest.mark.asyncio
async def test_create_negotiation_not_found(negotiation_service: NegotiationService):
    with pytest.raises(NotFoundException):
        await negotiation_service.create_negotiation(1, 1)


@pytest.mark.asyncio
async def test_create_negotiation_already_exists(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)

    ng = await negotiation_service.create_negotiation(vacancy.id, applicant.id)

    with pytest.raises(AlreadyExistException):
        await negotiation_service.create_negotiation(vacancy.id, applicant.id)


@pytest.mark.asyncio
async def test_delete_negotiation(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)

    ng = await negotiation_service.create_negotiation(vacancy.id, applicant.id)

    await negotiation_service.delete_by_id(ng.id)
    ng = await db_session.get(Negotiation, ng.id)

    assert ng is None


@pytest.mark.asyncio
async def test_delete_negotiation_not_found(negotiation_service: NegotiationService):
    with pytest.raises(NotFoundException):
        await negotiation_service.delete_by_id(1)


@pytest.mark.asyncio
async def test_delete_negotiation_wrong_state(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)

    ng = await negotiation_service.create_negotiation(vacancy.id, applicant.id)
    ng.status = NegotiationStatus.REJECTED.value
    await db_session.commit()

    with pytest.raises(WrongStateException):
        await negotiation_service.delete_by_id(ng.id)

    ng.status = NegotiationStatus.ACCEPTED.value
    await db_session.commit()

    with pytest.raises(WrongStateException):
        await negotiation_service.delete_by_id(ng.id)


@pytest.mark.asyncio
async def test_update_negotiation(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)

    ng = await negotiation_service.create_negotiation(vacancy.id, applicant.id)
    await db_session.commit()

    ng = await negotiation_service.update_negotiation(
        ng.id, employer.id, NegotiationStatus.REJECTED
    )
    
    assert ng.status == NegotiationStatus.REJECTED.value


@pytest.mark.asyncio
async def test_update_negotiation_not_allowed(db_session: AsyncSession, applicant: User, employer: User, negotiation_service: NegotiationService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)

    ng = await negotiation_service.create_negotiation(vacancy.id, applicant.id)
    await db_session.commit()

    employer_1 = User(
        email="employer1@example.com",
        surname="Doe",
        name="John",
        hashed_password="pwd",
        is_active=True,
        is_superuser=True,
        is_employer=True
    )

    employer_1.employer = Employer(company_id=employer.employer.company_id)
    db_session.add(employer_1)
    await db_session.commit()

    with pytest.raises(NotAllowedException):
        await negotiation_service.update_negotiation(
            ng.id, employer_1.id, NegotiationStatus.REJECTED
        )


@pytest.mark.asyncio
async def test_update_negotiation_not_founf(employer: User, negotiation_service: NegotiationService):
    with pytest.raises(NotFoundException):
        await negotiation_service.update_negotiation(
            1, employer.id, NegotiationStatus.REJECTED
        )
