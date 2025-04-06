from pydantic import BaseModel, Field


class SBaseQueryBody(BaseModel):
    q: str | None = None
    start: int | None = Field(None, ge=0)
    end: int | None = Field(None, ge=0)


class SBaseQueryCountResponse(BaseModel):
    count: int
