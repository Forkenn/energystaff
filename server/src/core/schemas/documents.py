from pydantic import BaseModel


class SBaseDocumentRead(BaseModel):
    id: int
    download_name: str
    real_name: str
    size: int
