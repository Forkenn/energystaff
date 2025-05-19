import pytest
from src.users.models import User, Applicant
from src.resume.models import Resume
from src.vacancies.models import EmploymentFormat, EmploymentType

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_resume_types_formats_relationship(db_session: AsyncSession):
    """Test Resume and EmploymentType and EmploymentFormat relationship"""
    user = User(email="resume@example.com", name="Resume", surname="User", hashed_password="pwd", is_applicant=True)
    applicant = Applicant(user=user)
    etype = EmploymentType(name="Part-time")
    etype_1 = EmploymentType(name="Full-time")
    eformat = EmploymentFormat(name="Remote")
    resume = Resume(user=user, position="Analyst", description="Details", resume_types=[etype, etype_1], resume_formats=[eformat])
    db_session.add(resume)
    await db_session.commit()
    await db_session.refresh(resume, attribute_names=('resume_formats', 'resume_types'))

    assert len(resume.resume_types) == 2
    assert len(resume.resume_formats) == 1
    assert resume.resume_types[0].name == "Part-time"
    assert resume.resume_formats[0].name == "Remote"
    assert resume.resume_types[1].name == "Full-time"


@pytest.mark.asyncio
async def test_resume_types_delete(db_session: AsyncSession):
    """Test Resume and EmploymentType relationship set null"""
    user = User(email="resume@example.com", name="Resume", surname="User", hashed_password="pwd", is_applicant=True)
    applicant = Applicant(user=user)
    etype = EmploymentType(name="Part-time")
    resume = Resume(user=user, position="Analyst", description="Details", resume_types=[etype])
    db_session.add(resume)
    await db_session.commit()
    await db_session.refresh(resume, attribute_names=('resume_types',))

    assert len(resume.resume_types) == 1
    assert resume.resume_types[0].name == "Part-time"

    await db_session.delete(etype)
    await db_session.refresh(resume, attribute_names=('resume_types',))
    assert len(resume.resume_types) == 0


@pytest.mark.asyncio
async def test_resume_format_delete(db_session: AsyncSession):
    """Test Resume and EmploymentFormat relationship set null"""
    user = User(email="resume@example.com", name="Resume", surname="User", hashed_password="pwd", is_applicant=True)
    applicant = Applicant(user=user)
    eformat = EmploymentFormat(name="Remote")
    eformat_1 = EmploymentFormat(name="Office")
    resume = Resume(user=user, position="Analyst", description="Details", resume_formats=[eformat, eformat_1])
    db_session.add(resume)
    await db_session.commit()
    await db_session.refresh(resume, attribute_names=('resume_formats',))

    assert len(resume.resume_formats) == 2
    assert resume.resume_formats[0].name == "Remote"
    assert resume.resume_formats[1].name == "Office"

    await db_session.delete(eformat)
    await db_session.refresh(resume, attribute_names=('resume_formats',))
    assert len(resume.resume_formats) == 1
    assert resume.resume_formats[0].name == "Office"
