import sqlalchemy as alch

from typing import TypeVar, Type, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ColumnElement

T = TypeVar("T")    # SQLAlchemy Model
P = TypeVar("P")    # Pydantic Schema

async def fetch_one(
        session: AsyncSession,
        model: Type[T],
        *where: ColumnElement[bool]
) -> T | None:
    query = alch.select(model).where(*where)
    return (await session.execute(query)).scalar()

async def fetch_all(
        session: AsyncSession,
        model: Type[T],
        *where: ColumnElement[bool]
) -> Sequence[T | None]:
    query = alch.select(model).where(*where)
    return (await session.execute(query)).scalars().all()

async def search_catalog_multi(
        session: AsyncSession,
        model: Type[T],
        q: str | None = None,
        start: int | None = None,
        end: int | None = None
) -> Sequence[T | None]:
    query = alch.select(model)
    if q:
        query = query.where(model.name.like(f'{q}%'))
    if start and end:
        query = query.slice(start, end)

    return (await session.execute(query)).scalars().all()
