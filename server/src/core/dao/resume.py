import sqlalchemy as alch

from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.resume.models import Resume
from src.negotiations.models import Negotiation

async def get_secure_resume(
        session: AsyncSession,
        employer_id: int,
        applicant_id: int
) -> Resume:
    exists_criteria = (
        alch.select(Negotiation)
        .where(
            Negotiation.applicant_id == applicant_id,
            Negotiation.employer_id == employer_id
        )
        .exists()
    )
    query = (
        alch.select(Resume)
        .where(
            Resume.user_id == applicant_id,
            exists_criteria
        )
        .options(
            joinedload(Resume.resume_formats),
            joinedload(Resume.resume_types)
        )
    )

    resume: Resume = (await session.execute(query)).scalar()
    return resume
