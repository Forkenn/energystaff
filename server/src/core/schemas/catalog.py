from pydantic import BaseModel


class SBaseCatalogItemRead(BaseModel):
    id: int
    name: str


class SBaseCatalogRead(BaseModel):
    count: int
    items: list[SBaseCatalogItemRead]
