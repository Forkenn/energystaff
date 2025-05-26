from datetime import datetime

from pydantic import BaseModel, Field

from src.core.schemas.common import SBaseQuerySliceBody, SBaseQueryCountResponse
from src.negotiations.models import NegotiationStatus


class SNegotiationsIdBody(BaseModel):
    negotiation_id: int


class SNegotiationsFilter(SBaseQuerySliceBody):
    status: NegotiationStatus | None = None


class SNegotiationResult(BaseModel):
    id: int
    timestamp: datetime
    status: NegotiationStatus
    applicant_id: int
    vacancy_id: int


class SNegotiationChangeStatus(SNegotiationsIdBody):
    employer_description: str = Field(
        default=...,
        min_length=50,
        max_length=500,
        description="Description from 50 to 500 symbols"
    )


class SNegotiationAppPreview(SNegotiationResult):
    company_name: str
    vacancy_position: str
    vacancy_salary: int
    vacancy_location: str | None = 'Тестовый город, заменить!'
    employer_description: str | None = None


class SNegotiationAppPreviews(SBaseQueryCountResponse):
    items: list[SNegotiationAppPreview]


class SNegotiationEmpPreview(SNegotiationResult):
    vacancy_position: str
    vacancy_salary: int
    user_name: str
    user_surname: str
    user_last_name: str
    user_location: str | None = 'Город не указан'
    employer_description: str | None = None


class SNegotiationEmpPreviews(SBaseQueryCountResponse):
    items: list[SNegotiationEmpPreview]
