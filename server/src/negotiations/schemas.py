from datetime import datetime

from pydantic import BaseModel

from src.core.schemas.common import SBaseQuerySliceBody, SBaseQueryCountResponse
from src.negotiations.models import NegotiationStatus


class SNegotiationsFilter(SBaseQuerySliceBody):
    status: NegotiationStatus | None = None


class SNegotiationResult(BaseModel):
    id: int
    timestamp: datetime
    status: NegotiationStatus
    applicant_id: int
    vacancy_id: int


class SNegotiationAppPreview(SNegotiationResult):
    company_name: str
    vacancy_position: str
    vacancy_salary: int
    vacancy_location: str | None = 'Тестовый город, заменить!'


class SNegotiationAppPreviews(SBaseQueryCountResponse):
    items: list[SNegotiationAppPreview]


class SNegotiationEmpPreview(SNegotiationResult):
    vacancy_position: str
    vacancy_salary: int
    user_name: str
    user_surname: str
    user_last_name: str
    user_location: str | None = 'Тестовый город, заменить!'


class SNegotiationEmpPreviews(SBaseQueryCountResponse):
    items: list[SNegotiationEmpPreview]
