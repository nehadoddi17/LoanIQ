
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ApplicationDocumentCreate(BaseModel):
    document_id: str = Field(min_length=1, max_length=30)
    application_id: str = Field(min_length=1, max_length=30)
    document_type: str
    file_name: str
    verification_status: str = "PENDING"


class ApplicationDocumentResponse(ApplicationDocumentCreate):
    uploaded_at: datetime | None = None
    verified_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
