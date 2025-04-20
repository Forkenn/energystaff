import sqlalchemy as alch

from typing import TypeVar, Generic, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.common import CommonRepository

T = TypeVar("T")


class CatalogRepository(CommonRepository[T], Generic[T]):
    def __init__(self, model: type[T], session: AsyncSession):
        super().__init__(model, session)

    async def get_all(self):
        query = alch.select(self.model)
        return (await self.session.execute(query)).scalars().all()
    
    async def get_by_name(self, name: str) -> T:
        query = alch.select(self.model).where(self.model.name == name)
        return (await self.session.execute(query)).scalar()
    
    async def exists_by_name(self, name: str) -> bool:
        query = alch.select(1).where(self.model.name == name)
        result = await self.session.scalar(query)
        return result is not None
    
    async def create(self, name: str) -> T:
        new_item = self.model(name=name)
        self.session.add(new_item)

        await self.session.commit()
        return new_item
    
    async def edit(self, item: T, name: str) -> None:
        item.name = name
        await self.session.commit()

    async def search_catalog(
            self,
            q: str | None = None,
            start: int | None = None,
            end: int | None = None
    ) -> Sequence[T | None]:
        query = alch.select(self.model)
        if q:
            query = query.where(self.model.name.like(f'%{q}%'))
        if start and end:
            query = query.slice(start, end)

        return (await self.session.execute(query)).scalars().all()
