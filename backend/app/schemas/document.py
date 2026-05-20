from pydantic import BaseModel
from datetime import datetime


class DocumentCreate(BaseModel):
    filename: str


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content: str | None
    created_at: datetime

    class Config:
        from_attributes = True