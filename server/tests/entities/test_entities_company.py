import pytest
from src.companies.models import Company

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


@pytest.mark.asyncio
async def test_unique_name_constraint(db_session: AsyncSession):
    """Test unique companies names"""
    company1 = Company(name="Grand Test Company")
    company2 = Company(name="Grand Test Company")

    db_session.add(company1)
    await db_session.commit()

    db_session.add(company2)
    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_unique_inn_constraint(db_session: AsyncSession):
    """Test unique companies inn"""
    company1 = Company(name="Grand Test Company", inn='123456789012')
    company2 = Company(name="Big Test Company", inn='123456789012')

    db_session.add(company1)
    await db_session.commit()

    db_session.add(company2)
    with pytest.raises(IntegrityError):
        await db_session.commit()
