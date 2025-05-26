import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import NotAllowedException, NotFoundException
from src.users.models import User
from src.vacancies.models import Vacancy, EmploymentFormat, EmploymentSchedule, EmploymentType
from src.vacancies.schemas import SVacancyCreate
from src.companies.models import Company
from src.tools.models import Location

from src.core.services.vacancy import VacancyService

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
async def test_create_vacancy(db_session: AsyncSession, employer: User, vacancy_service: VacancyService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    fields = await create_vacancies_fields(db_session)
    data = SVacancyCreate(
        position='position_test',
        specialization='specialization_test',
        description='description_test',
        vacancy_formats_ids=[fields[0].id],
        vacancy_types_ids=[fields[1].id],
        vacancy_schedules_ids=[fields[2].id],
        work_hours='work_hours_test',
        salary=60000,
        location_id=location.id
    )
    await vacancy_service.create_vacancy(employer, data)

    vacancy = await db_session.get(Vacancy, 1)

    assert vacancy.author_id == employer.id
    assert vacancy.position == 'position_test'
    assert vacancy.specialization == 'specialization_test'
    assert vacancy.description == 'description_test'
    assert vacancy.work_hours == 'work_hours_test'
    assert vacancy.salary == 60000
    assert vacancy.location_id == location.id


@pytest.mark.asyncio
async def test_get_full_vacancy(db_session: AsyncSession, employer: User, vacancy_service: VacancyService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    vacancy = await create_vacancy(db_session, employer, location)
    vacancy_test = await vacancy_service.get_full_vacancy(vacancy.id)

    assert vacancy_test.author_id == employer.id
    assert vacancy_test.position == 'position_test'
    assert vacancy_test.specialization == 'specialization_test'
    assert vacancy_test.description == 'description_test'
    assert vacancy_test.work_hours == 'work_hours_test'
    assert vacancy_test.salary == 60000
    assert vacancy_test.location_id == location.id
    assert vacancy_test.location.name == location.name
    assert vacancy_test.company.id == 1
    assert vacancy_test.vacancy_formats[0].id == 1
    assert vacancy_test.vacancy_schedules[0].id == 1
    assert vacancy_test.vacancy_types[0].id == 1


@pytest.mark.asyncio
async def test_delete_vacancy_author(db_session: AsyncSession, employer: User, vacancy_service: VacancyService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()
    vacancy = await create_vacancy(db_session, employer, location)

    await vacancy_service.delete_by_id(employer.id, vacancy.id)

    vacancy = await db_session.get(Vacancy, vacancy.id)
    assert vacancy is None


@pytest.mark.asyncio
async def test_delete_vacancy_user(db_session: AsyncSession, employer: User, vacancy_service: VacancyService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()
    vacancy = await create_vacancy(db_session, employer, location)

    with pytest.raises(NotAllowedException):
        await vacancy_service.delete_by_id(2, vacancy.id)


@pytest.mark.asyncio
async def test_delete_vacancy_forced(db_session: AsyncSession, employer: User, vacancy_service: VacancyService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()
    vacancy = await create_vacancy(db_session, employer, location)

    await vacancy_service.force_delete_by_id(vacancy.id)

    vacancy = await db_session.get(Vacancy, vacancy.id)
    assert vacancy is None


@pytest.mark.asyncio
async def test_update_vacancy_author(db_session: AsyncSession, employer: User, vacancy_service: VacancyService):
    location = Location(name='Talmberg')
    location_1 = Location(name='Ratau')
    db_session.add_all([location, location_1])
    await db_session.commit()
    vacancy = await create_vacancy(db_session, employer, location)

    format = EmploymentFormat(name='test_1')
    type = EmploymentType(name='test_1')
    schedule = EmploymentSchedule(name='test_1')

    db_session.add_all([format, type, schedule])
    await db_session.commit()

    data = SVacancyCreate(
        position='position_test_new',
        specialization='position_test_new',
        description='position_test_new',
        vacancy_formats_ids=[vacancy.vacancy_formats[0].id, format.id],
        vacancy_types_ids=[vacancy.vacancy_types[0].id, type.id],
        vacancy_schedules_ids=[vacancy.vacancy_schedules[0].id, schedule.id],
        work_hours='work_hours_test_new',
        salary=60010,
        location_id=location_1.id
    )

    vacancy_test = await vacancy_service.update_vacancy(employer.id, vacancy.id, data)
    assert vacancy_test.position == 'position_test_new'
    assert vacancy_test.specialization == 'position_test_new'
    assert vacancy_test.description == 'position_test_new'
    assert vacancy_test.work_hours == 'work_hours_test_new'
    assert vacancy_test.salary == 60010
    #assert vacancy_test.location_id == location_1.id
    #assert vacancy_test.location.name == location_1.name
    assert vacancy_test.vacancy_formats[0].id == 1
    assert vacancy_test.vacancy_schedules[0].id == 1
    assert vacancy_test.vacancy_types[0].id == 1
    assert vacancy_test.vacancy_formats[1].id == 2
    assert vacancy_test.vacancy_schedules[1].id == 2
    assert vacancy_test.vacancy_types[1].id == 2


@pytest.mark.asyncio
async def test_update_vacancy_user(db_session: AsyncSession, employer: User, vacancy_service: VacancyService):
    location = Location(name='Talmberg')
    location_1 = Location(name='Ratau')
    db_session.add_all([location, location_1])
    await db_session.commit()
    vacancy = await create_vacancy(db_session, employer, location)

    format = EmploymentFormat(name='test_1')
    type = EmploymentType(name='test_1')
    schedule = EmploymentSchedule(name='test_1')

    db_session.add_all([format, type, schedule])
    await db_session.commit()

    data = SVacancyCreate(
        position='position_test_new',
        specialization='position_test_new',
        description='position_test_new',
        salary=5000,
        vacancy_formats_ids=[vacancy.vacancy_formats[0].id, format.id],
        vacancy_types_ids=[vacancy.vacancy_types[0].id, type.id],
        vacancy_schedules_ids=[vacancy.vacancy_schedules[0].id, schedule.id],
        work_hours='work_hours_test_new',
    )

    with pytest.raises(NotAllowedException):
        await vacancy_service.update_vacancy(2, vacancy.id, data)


@pytest.mark.asyncio
async def test_update_vacancy_not_found(db_session: AsyncSession, employer: User, vacancy_service: VacancyService):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()
    vacancy = await create_vacancy(db_session, employer, location)

    data = SVacancyCreate(
        position='position_test_new',
        specialization='position_test_new',
        description='position_test_new',
        salary=5000,
        vacancy_formats_ids=[vacancy.vacancy_formats[0].id],
        vacancy_types_ids=[vacancy.vacancy_types[0].id],
        vacancy_schedules_ids=[vacancy.vacancy_schedules[0].id],
        work_hours='work_hours_test_new',
    )

    with pytest.raises(NotFoundException):
        await vacancy_service.update_vacancy(2, 52, data)
