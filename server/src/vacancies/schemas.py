from typing import Annotated
from pydantic import BaseModel, Field

from src.schemas import SBaseCatalogItemRead

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
    salary: int = Field(None, ge=0)
    description: str = Field(
        default=...,
        min_length=0,
        max_length=500,
        description="Description from 0 to 500 symbols"
    )
    vacancy_types_ids: list[Annotated[int, Field(strict=True, gt=0)]] = Field(..., min_length=1)
    vacancy_formats_ids: list[Annotated[int, Field(strict=True, gt=0)]] = Field(..., min_length=1)
    vacancy_schedules_ids: list[Annotated[int, Field(strict=True, gt=0)]] = Field(..., min_length=1)


class SVacancyRead(BaseModel):
    position: str
    specialization: str
    salary: int
    vacancy_types: list[SBaseCatalogItemRead]
    vacancy_formats: list[SBaseCatalogItemRead]
    vacancy_schedules: list[SBaseCatalogItemRead]


class SVacancyPreview(BaseModel):
    position: str
    salary: int
    city: str | None = "Тестовый город, заменить!"
    company_id: int
    company_name: str| None = 'Тестовая комания, заменить!'


class SVacanciesPreview(BaseModel):
    count: int
    items: list[SVacancyPreview]
