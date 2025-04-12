from pydantic import BaseModel, Field


class SBaseQuerySliceBody(BaseModel):
    start: int | None = Field(None, ge=0)
    end: int | None = Field(None, ge=0)


class SBaseQueryBody(SBaseQuerySliceBody):
    q: str | None = None


class SBaseQueryCountResponse(BaseModel):
    count: int
