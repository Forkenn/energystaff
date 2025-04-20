import sqlalchemy as alch

from typing import TypeVar, Generic, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class CommonRepository(Generic[T]):
    def __init__(self, model: type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> T | None:
        obj: T = await self.session.get(self.model, id)
        return obj
    
    async def get_many(self, start: int, end: int) -> Sequence[T | None]:
        query = alch.select(self.model).slice(start, end)
        return (await self.session.execute(query)).scalars().all()
    
    async def delete(self, id: int) -> None:
        query = alch.delete(self.model).where(self.model.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_object(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.commit()
