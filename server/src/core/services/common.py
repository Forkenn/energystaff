from typing import TypeVar, Generic, Type

from src.exceptions import NotFoundException
from src.core.repositories.common import CommonRepository

R = TypeVar('R', bound=CommonRepository)


class CommonService(Generic[R]):
    def __init__(self, repository: Type[R]):
        self.repository = repository

    async def get_by_id(self, id: int):
        result = await self.repository.get(id)
        if not result:
            raise NotFoundException()
        
        return result
