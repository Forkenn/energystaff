from enum import Enum
from typing import Annotated, Any
from pydantic import BaseModel, Field, field_validator

from src.core.schemas.catalog import SBaseCatalogItemRead
from src.core.schemas.common import SBaseQuerySliceBody
from src.negotiations.models import NegotiationStatus


class SortBy(Enum):
    DATE = 'date'
    SALARY = 'salary'


class SVacanciesCountQuery(BaseModel):
    q: str | None = None
    location_id: int | None = None
    salary_from: int | None = None
    salary_to: int | None = None
    employment_types_ids: list[int] | None = Field(None, exclude=True)
    employment_formats_ids: list[int] | None = Field(None, exclude=True)
    employment_schedules_ids: list[int] | None = Field(None, exclude=True)


class SVacanciesPreviewsQuery(SVacanciesCountQuery, SBaseQuerySliceBody):
    sort_by: SortBy | None = SortBy.DATE.value
    desc: bool | None = True


class SCompany(BaseModel):
    id: int
    name: str


class SVacancyCreate(BaseModel):
    position: str = Field(
        default=...,
        min_length=4,
        max_length=120,
        description="Position from 4 to 120 symbols"
    )
    specialization: str = Field(
        default=...,
        min_length=4,
        max_length=120,
        description="Specialization from 4 to 120 symbols"
    )
    work_hours: str | None = Field(
        default=...,
        min_length=0,
        max_length=50,
        description="Work hours from 0 to 50 symbols"
    )
    salary: int | None = Field(..., ge=0, le=5000000)
    description: str = Field(
        default=...,
        min_length=0,
        max_length=5000,
        description="Description from 0 to 5000 symbols"
    )
    location_id: int | None = None
    vacancy_types_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)
    vacancy_formats_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)
    vacancy_schedules_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)

    @field_validator("salary", mode="before")
    @classmethod
    def set_default_if_none(cls, v):
        return v if v is not None else 0


class SVacancyRead(BaseModel):
    id: int
    position: str
    specialization: str
    work_hours: str | None
    salary: int
    description: str
    location: SBaseCatalogItemRead | None
    author_id: int
    vacancy_types: list[SBaseCatalogItemRead]
    vacancy_formats: list[SBaseCatalogItemRead]
    vacancy_schedules: list[SBaseCatalogItemRead]


class SVacancyReadFull(SVacancyRead):
    company: SCompany


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
