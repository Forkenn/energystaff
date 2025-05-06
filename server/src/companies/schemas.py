from datetime import date
from pydantic import BaseModel, Field

from src.core.schemas.common import SBaseQueryCountResponse, SBaseQuerySliceBody


class SComaniesFilteredQuery(BaseModel):
    q: str | None = None
    registration_date: date | None = None
    only_verified: bool | None = False


class SComaniesReadQuery(SComaniesFilteredQuery, SBaseQuerySliceBody):
    desc: bool | None = True


class SCompanyRead(BaseModel):
    id: int
    name: str
    registration_date: date | None
    inn: str | None
    address: str | None
    description: str | None
    is_verified: bool


class SCompaniesRead(SBaseQueryCountResponse):
    items: list[SCompanyRead]


class SCompanyEdit(BaseModel):
    name: str = Field(
        default=...,
        min_length=5,
        max_length=120,
        description="Company name from 5 to 120 symbols"
    )
    registration_date: date
    inn: str = Field(
        default=...,
        min_length=12,
        max_length=12,
        description="Company INN, 12 symbols"
    )
    address: str = Field(
        default=...,
        min_length=0,
        max_length=120,
        description="Company address from 0 to 120 symbols"
    )
    description: str = Field(
        default=...,
        min_length=0,
        max_length=512,
        description="Company description from 0 to 512 symbols"
    )
