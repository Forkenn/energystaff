import json

from pydantic import BaseModel, Field, model_validator

from src.core.schemas.documents import SBaseDocumentRead


class SRecommendationCreate(BaseModel):
    description: str | None = Field(
        default=...,
        min_length=0,
        max_length=5000,
        description="Description from 0 to 5000 symbols"
    )

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value



class SRecommendationUpdate(SRecommendationCreate):
    deleted_documents: list[str] | None = None


class SRecommendationRead(BaseModel):
    id: int
    description: str
    documents: list[SBaseDocumentRead]
