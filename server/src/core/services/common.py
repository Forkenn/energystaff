from typing import TypeVar, Generic, Optional, List, Type
from pydantic import BaseModel

T = TypeVar('T')
P = TypeVar('P', bound=BaseModel)


class CommonService(Generic[T, P]):
    def __init__(self, model: Type[T]):
        self.model = model
