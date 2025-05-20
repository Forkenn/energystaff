import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import NotFoundException, AlreadyExistException
from src.tools.models import Location

from src.core.services.catalog import CatalogService
from src.core.schemas.common import SBaseQueryBody

@pytest.mark.asyncio
async def test_create_catalog(
    location_service: CatalogService
):
    data: Location = await location_service.add_item('Talmberg')
    assert data.id == 1
    assert data.name == 'Talmberg'


@pytest.mark.asyncio
async def test_create_catalog_exists(
    db_session: AsyncSession,
    location_service: CatalogService
):
    location = Location(name='Talmberg')
    db_session.add(location)
    await db_session.commit()

    with pytest.raises(AlreadyExistException):
        await location_service.add_item('Talmberg')


@pytest.mark.asyncio
async def test_edit_catalog(
    db_session: AsyncSession,
    location_service: CatalogService
):
    location = Location(name='Talmberg')
    location_1 = Location(name='Ratau')
    db_session.add_all([location, location_1])
    await db_session.commit()

    location: Location = await location_service.edit_item(location.id, 'Sasau')

    assert location.name == 'Sasau'


@pytest.mark.asyncio
async def test_edit_catalog_exists(
    db_session: AsyncSession,
    location_service: CatalogService
):
    location = Location(name='Talmberg')
    location_1 = Location(name='Ratau')
    db_session.add_all([location, location_1])
    await db_session.commit()

    with pytest.raises(AlreadyExistException):
        await location_service.edit_item(location.id, 'Ratau')


@pytest.mark.asyncio
async def test_edit_catalog_not_found(location_service: CatalogService):
    with pytest.raises(NotFoundException):
        await location_service.edit_item(52, 'Ratau')


@pytest.mark.asyncio
async def test_get_all_catalog(
    db_session: AsyncSession,
    location_service: CatalogService
):
    location = Location(name='Talmberg')
    location_1 = Location(name='Ratau')
    db_session.add_all([location, location_1])
    await db_session.commit()

    locations: list[Location] = await location_service.get_all()
    assert len(locations) == 2
    assert locations[0].id == location.id
    assert locations[1].id == location_1.id


@pytest.mark.asyncio
async def test_search_catalog(
    db_session: AsyncSession,
    location_service: CatalogService
):
    location = Location(name='Talmberg')
    location_1 = Location(name='Ratau')
    db_session.add_all([location, location_1])
    await db_session.commit()

    locations: list[Location] = await location_service.search_catalog(
        SBaseQueryBody(
            q='lmb'
        )
    )

    assert len(locations) == 1
    assert locations[0].id == location.id

    locations: list[Location] = await location_service.search_catalog(
        SBaseQueryBody(
            q='ata'
        )
    )

    assert len(locations) == 1
    assert locations[0].id == location_1.id

    locations: list[Location] = await location_service.search_catalog(
        SBaseQueryBody(
            q='a'
        )
    )

    assert len(locations) == 2
    assert locations[0].id == location.id
    assert locations[1].id == location_1.id
    