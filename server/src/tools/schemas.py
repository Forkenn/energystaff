from pydantic import BaseModel, Field


class SBaseToolsSearch(BaseModel):
    q: str | None = None
    start: int | None = Field(None, ge=0)
    end: int | None = Field(None, ge=0)


class SEduInstitutionCreate(BaseModel):
    name: str = Field(
        default=...,
        min_length=5,
        max_length=240,
        description="Name from 5 to 240 symbols"
    )


class SEduLevelCreate(BaseModel):
    name: str = Field(
        default=...,
        min_length=5,
        max_length=15,
        description="Name from 5 to 15 symbols"
    )


class SLocationCreate(BaseModel):
    name: str = Field(
        default=...,
        min_length=3,
        max_length=25,
        description="Name from 3 to 25 symbols"
    )
