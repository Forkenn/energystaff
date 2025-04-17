import sqlalchemy as alch

from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User, Applicant

async def edit_user(session: AsyncSession, user: User, data: dict) -> User:
    applciant_data: dict = data.pop('applicant', None)
    for field, value in data.items():
        setattr(user, field, value)

    if applciant_data:
        for field, value in applciant_data.items():
            if field == 'edu_status' and value is not None:
                value = value.value

            setattr(user.applicant, field, value)

    await session.commit()
    return user

async def fetch_users(
        session: AsyncSession,
        q: str | None = None,
        start: int | None = None,
        end: int | None = None,
        *where: ColumnElement[bool]
):
    query = (
        alch.select(User)
        .where(*where)
        .options(
            selectinload(User.applicant),
            selectinload(User.employer),
            selectinload(User.edu_worker)
        )
    )
    if start and end:
        query = query.slice(start, end)

    return (await session.execute(query)).scalars().all()

async def fetch_applicants(
        session: AsyncSession,
        user: User,
        q: str | None = None,
        start: int | None = None,
        end: int | None = None
) -> list:
    query = (
        alch.select(User)
        .where(
            User.is_applicant,
            Applicant.edu_institution_id == user.edu_worker.edu_institution_id
        )
        .join(User.applicant)
        .options(
            selectinload(User.applicant)
        )
    )
    if start and end:
        query = query.slice(start, end)

    return (await session.execute(query)).scalars().all()
