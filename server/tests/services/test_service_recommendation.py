import os.path

import pytest

from tempfile import SpooledTemporaryFile

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import (
    NotFoundException, AlreadyExistException, ForbiddenException
)
from src.users.models import User
from src.companies.models import Company
from src.tools.models import Location, EduInstitution
from src.vacancies.models import (
    Vacancy, EmploymentFormat, EmploymentSchedule, EmploymentType
)
from src.recommendations.schemas import SRecommendationCreate, SRecommendationUpdate

from src.core.services.recommendation import RecommendationService
from src.core.dto.file import FileDTO


async def create_vacancy(session: AsyncSession, user: User, location: Location):
    format = EmploymentFormat(name='test')
    type = EmploymentType(name='test')
    schedule = EmploymentSchedule(name='test')

    session.add_all([format, type, schedule])
    await session.commit()

    vacancy = Vacancy(
        position='position_test',
        specialization='specialization_test',
        description='description_test',
        work_hours='work_hours_test',
        salary=60000,
        vacancy_formats=[format.id],
        vacancy_types=[type.id],
        vacancy_schedules=[schedule.id],
        location_id=location.id,
        author_id=user.id,
        company_id=user.employer.company_id
    )
    session.add(vacancy)
    await session.commit()
    return vacancy


@pytest.mark.asyncio
async def test_create_recommendation(
    applicant: User,
    recommendation_service: RecommendationService
):
    data = SRecommendationCreate(
        description='Test recommendation'
    )
    file = SpooledTemporaryFile()
    fileDTO = FileDTO(
        download_name='Test',
        size=0,
        file=file
    )
    fileDTO_1 = FileDTO(
        download_name='Test_1',
        size=0,
        file=file
    )

    rec = await recommendation_service.create_recommendation(
        applicant.id, documents=[fileDTO, fileDTO_1], data=data
    )

    assert rec.id == 1
    assert len(rec.documents) == 2
    assert rec.documents[0].id == 1
    assert rec.documents[0].download_name == 'Test'
    assert rec.documents[0].real_name is not None
    assert rec.documents[0].size == 0

    assert rec.documents[1].id == 2
    assert rec.documents[1].download_name == 'Test_1'
    assert rec.documents[1].real_name is not None
    assert rec.documents[1].size == 0

    assert os.path.isfile(f'storage/proof_documents/{rec.documents[0].real_name}')
    assert os.path.isfile(f'storage/proof_documents/{rec.documents[1].real_name}')


@pytest.mark.asyncio
async def test_create_recommendation_exists(
    applicant: User,
    recommendation_service: RecommendationService
):
    data = SRecommendationCreate(
        description='Test recommendation'
    )

    await recommendation_service.create_recommendation(
        applicant.id, documents=[], data=data
    )

    with pytest.raises(AlreadyExistException):
        await recommendation_service.create_recommendation(
            applicant.id, documents=[], data=data
        )


@pytest.mark.asyncio
async def test_update_recommendation(
    db_session: AsyncSession,
    applicant: User,
    edu_worker: User,
    recommendation_service: RecommendationService
):
    applicant.applicant.edu_institution_id = edu_worker.edu_worker.edu_institution_id
    await db_session.commit()

    data = SRecommendationCreate(
        description='Test recommendation'
    )

    file = SpooledTemporaryFile()
    fileDTO = FileDTO(
        download_name='Test',
        size=0,
        file=file
    )
    fileDTO_1 = FileDTO(
        download_name='Test_1',
        size=0,
        file=file
    )

    rec = await recommendation_service.create_recommendation(
        applicant.id, documents=[fileDTO, fileDTO_1], data=data
    )

    new_data = SRecommendationUpdate(
        description='Test recommendation',
        deleted_documents=[rec.documents[0].real_name]
    )
    deleted_doc_real_name = rec.documents[0].real_name

    rec = await recommendation_service.update_recommendation(
        rec.id, edu_worker.edu_worker, data=new_data, documents=[]
    )

    assert rec.id == 1
    assert len(rec.documents) == 1
    assert rec.documents[0].id == 2
    assert rec.documents[0].download_name == 'Test_1'
    assert rec.documents[0].real_name is not None
    assert rec.documents[0].size == 0

    assert os.path.isfile(f'storage/proof_documents/{rec.documents[0].real_name}')
    assert not os.path.isfile(f'storage/proof_documents/{deleted_doc_real_name}')


@pytest.mark.asyncio
async def test_update_recommendation_not_found(
    db_session: AsyncSession,
    applicant: User,
    edu_worker: User,
    recommendation_service: RecommendationService
):
    applicant.applicant.edu_institution_id = edu_worker.edu_worker.edu_institution_id
    await db_session.commit()

    data = SRecommendationCreate(
        description='Test recommendation'
    )

    rec = await recommendation_service.create_recommendation(
        applicant.id, documents=[], data=data
    )

    with pytest.raises(NotFoundException):
        await recommendation_service.update_recommendation(
            20, edu_worker.edu_worker, data=data, documents=[]
        )

    edu = EduInstitution(
        name='Test University 2'
    )
    db_session.add(edu)
    await db_session.commit()

    edu_worker.edu_worker.edu_institution_id = edu.id

    with pytest.raises(NotFoundException):
        await recommendation_service.update_recommendation(
            rec.id, edu_worker.edu_worker, data=data, documents=[]
        )

    
@pytest.mark.asyncio
async def test_get_secured_recommendation(
    db_session: AsyncSession,
    applicant: User,
    edu_worker: User,
    employer: User,
    recommendation_service: RecommendationService
):
    applicant.applicant.edu_institution_id = edu_worker.edu_worker.edu_institution_id
    await db_session.commit()

    rec = await recommendation_service.create_recommendation(
        applicant.id,
        documents=[],
        data=SRecommendationCreate(
            description='Test recommendation'
        )
    )

    rec_test = await recommendation_service.get_full_by_uid_secured(
        applicant, applicant.id
    )
    assert rec_test.id == rec.id

    rec_test = await recommendation_service.get_full_by_uid_secured(
        employer, applicant.id
    )
    assert rec_test.id == rec.id

    rec_test = await recommendation_service.get_full_by_uid_secured(
        edu_worker, applicant.id
    )
    assert rec_test.id == rec.id


@pytest.mark.asyncio
async def test_get_secured_recommendation_forbidden (
    applicant: User,
    recommendation_service: RecommendationService
):
    await recommendation_service.create_recommendation(
        applicant.id,
        documents=[],
        data=SRecommendationCreate(
            description='Test recommendation'
        )
    )
    with pytest.raises(ForbiddenException):
        await recommendation_service.get_full_by_uid_secured(applicant, 52)


@pytest.mark.asyncio
async def test_get_secured_recommendation_not_found (
    applicant: User,
    edu_worker: User,
    employer: User,
    recommendation_service: RecommendationService
):
    await recommendation_service.create_recommendation(
        applicant.id,
        documents=[],
        data=SRecommendationCreate(
            description='Test recommendation'
        )
    )
    with pytest.raises(NotFoundException):
        await recommendation_service.get_full_by_uid_secured(employer, 52)
    
    with pytest.raises(NotFoundException):
        await recommendation_service.get_full_by_uid_secured(edu_worker, 52)
