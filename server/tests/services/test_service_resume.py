import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import NotFoundException, AlreadyExistException
from src.users.models import User
from src.companies.models import Company
from src.resume.models import Resume
from src.resume.schemas import SResumeCreate
from src.negotiations.models import Negotiation
from src.tools.models import Location
from src.vacancies.models import (
    Vacancy, EmploymentFormat, EmploymentSchedule, EmploymentType
)

from src.core.services.resume import ResumeService


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
async def test_create_resume(
    db_session: AsyncSession,
    applicant: User,
    resume_service: ResumeService
):
    fields = await create_vacancies_fields(db_session)
    data = SResumeCreate(
        position='test_position',
        specialization='test_specializaion',
        salary=60000,
        description='test_description',
        resume_formats_ids=[fields[0].id],
        resume_types_ids=[fields[2].id]
    )

    resume = await resume_service.create_resume(applicant.id, data=data)

    assert resume.id == 1
    assert resume.description == data.description
    assert resume.position == data.position
    assert resume.salary == data.salary
    assert resume.specialization == data.specialization
    assert len(resume.resume_formats) == 1
    assert len(resume.resume_types) == 1


@pytest.mark.asyncio
async def test_create_resume_exists(
    db_session: AsyncSession,
    applicant: User,
    resume_service: ResumeService
):
    fields = await create_vacancies_fields(db_session)
    data = SResumeCreate(
        position='test_position',
        specialization='test_specializaion',
        salary=60000,
        description='test_description',
        resume_formats_ids=[fields[0].id],
        resume_types_ids=[fields[2].id]
    )

    await resume_service.create_resume(applicant.id, data=data)

    with pytest.raises(AlreadyExistException):
        await resume_service.create_resume(applicant.id, data=data)


@pytest.mark.asyncio
async def test_get_full_resume(
    db_session: AsyncSession,
    applicant: User,
    resume_service: ResumeService
):
    fields = await create_vacancies_fields(db_session)
    data = SResumeCreate(
        position='test_position',
        specialization='test_specializaion',
        salary=60000,
        description='test_description',
        resume_formats_ids=[fields[0].id],
        resume_types_ids=[fields[2].id]
    )

    await resume_service.create_resume(applicant.id, data=data)
    resume = await resume_service.get_full_resume_by_uid(applicant.id)

    assert resume.id == 1
    assert resume.description == data.description
    assert resume.position == data.position
    assert resume.salary == data.salary
    assert resume.specialization == data.specialization
    assert len(resume.resume_formats) == 1
    assert len(resume.resume_types) == 1


@pytest.mark.asyncio
async def test_get_full_resume_not_found(
    resume_service: ResumeService
):
    with pytest.raises(NotFoundException):
        await resume_service.get_full_resume_by_uid(52)


@pytest.mark.asyncio
async def test_get_full_secured_resume(
    db_session: AsyncSession,
    applicant: User,
    employer: User,
    resume_service: ResumeService
):
    data = SResumeCreate(
        position='test_position',
        specialization='test_specializaion',
        salary=60000,
        description='test_description',
        resume_formats_ids=[1],
        resume_types_ids=[1]
    )

    await resume_service.create_resume(applicant.id, data=data)

    with pytest.raises(NotFoundException):
        await resume_service.get_full_resume_by_uid_secured(
            employer.id,
            applicant.id,
            include_user=True
        )

    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()
    vacancy = await create_vacancy(db_session, employer, location)
    ng = Negotiation(
        applicant_id=applicant.id,
        vacancy_id=vacancy.id,
        employer_id=employer.id
    )

    db_session.add(ng)
    await db_session.commit()

    resume = await resume_service.get_full_resume_by_uid_secured(
        employer.id,
        applicant.id,
        include_user=True
    )

    assert resume.id == 1
    assert resume.description == data.description
    assert resume.position == data.position
    assert resume.salary == data.salary
    assert resume.specialization == data.specialization
    assert len(resume.resume_formats) == 0
    assert len(resume.resume_types) == 0

    assert resume.user.id == applicant.id


@pytest.mark.asyncio
async def test_update_resume(
    db_session: AsyncSession,
    applicant: User,
    resume_service: ResumeService
):
    fields = await create_vacancies_fields(db_session)
    data = SResumeCreate(
        position='test_position',
        specialization='test_specializaion',
        salary=60000,
        description='test_description',
        resume_formats_ids=[fields[0].id],
        resume_types_ids=[fields[2].id]
    )

    await resume_service.create_resume(applicant.id, data=data)

    type = EmploymentType(name='test')
    db_session.add(type)
    await db_session.commit()

    new_data = SResumeCreate(
        position='test_position_new',
        specialization='test_specializaion_new',
        salary=60000,
        description='test_description_new',
        resume_formats_ids=[fields[0].id],
        resume_types_ids=[fields[2].id, type.id]
    )

    resume = await resume_service.update_resume(applicant.id, new_data)

    assert resume.id == 1
    assert resume.description == new_data.description
    assert resume.position == new_data.position
    assert resume.salary == new_data.salary
    assert resume.specialization == new_data.specialization
    assert len(resume.resume_formats) == 1
    assert len(resume.resume_types) == 2


@pytest.mark.asyncio
async def test_update_resume_not_found(resume_service: ResumeService):
    with pytest.raises(NotFoundException):
        await resume_service.update_resume(52, data=None)


@pytest.mark.asyncio
async def test_delete_resume(
    db_session: AsyncSession,
    applicant: User,
    resume_service: ResumeService
):
    fields = await create_vacancies_fields(db_session)
    data = SResumeCreate(
        position='test_position',
        specialization='test_specializaion',
        salary=60000,
        description='test_description',
        resume_formats_ids=[fields[0].id],
        resume_types_ids=[fields[2].id]
    )

    resume = await resume_service.create_resume(applicant.id, data=data)
    await resume_service.delete_by_uid(applicant.id)

    resume = await db_session.get(Resume, resume.id)
    assert resume is None


@pytest.mark.asyncio
async def test_delete_resume_not_found(resume_service: ResumeService):
    with pytest.raises(NotFoundException):
        await resume_service.delete_by_uid(52)
