from enum import Enum
from typing import Annotated, Any
from pydantic import BaseModel, Field

from src.core.schemas.catalog import SBaseCatalogItemRead
from src.negotiations.models import NegotiationStatus


class SortBy(Enum):
    DATE = 'date'
    SALARY = 'salary'


class SCompany(BaseModel):
    id: int
    name: str


class SVacancyCreate(BaseModel):
    position: str = Field(
        default=...,
        min_length=10,
        max_length=120,
        description="Position from 10 to 120 symbols"
    )
    specialization: str = Field(
        default=...,
        min_length=10,
        max_length=120,
        description="Specialization from 10 to 120 symbols"
    )
    work_hours: str | None = Field(
        default=...,
        min_length=0,
        max_length=50,
        description="Work hours from 0 to 50 symbols"
    )
    salary: int = Field(None, ge=0)
    description: str = Field(
        default=...,
        min_length=0,
        max_length=500,
        description="Description from 0 to 500 symbols"
    )
    location_id: int | None = None
    vacancy_types_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)
    vacancy_formats_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)
    vacancy_schedules_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)


class SVacancyRead(BaseModel):
    id: int
    position: str
    specialization: str
    work_hours: str | None
    salary: int
    description: str
    company: SCompany
    location: SBaseCatalogItemRead | None
    author_id: int
    vacancy_types: list[SBaseCatalogItemRead]
    vacancy_formats: list[SBaseCatalogItemRead]
    vacancy_schedules: list[SBaseCatalogItemRead]


class SVacancyNegotiation(BaseModel):
    id: int
    status: NegotiationStatus


class SVacancyPreview(BaseModel):
    id: int
    position: str
    salary: int
    location_name: str | None = "Любой регион"
    company_id: int
    author_id: int
    company_name: str
    negotiation_id: int | None = Field(..., exclude=True)
    negotiation_status: NegotiationStatus | None = Field(..., exclude=True)
    negotiation: SVacancyNegotiation | None = None

    def model_post_init(self, __context: Any):
        if self.negotiation_id:
            self.negotiation = SVacancyNegotiation(
                id=self.negotiation_id, status=self.negotiation_status
            )


class SVacanciesPreview(BaseModel):
    count: int
    items: list[SVacancyPreview]
