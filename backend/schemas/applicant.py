
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class ApplicantCreate(BaseModel):
    applicant_id: str = Field(min_length=1, max_length=30)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str | None = None
    date_of_birth: date | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    credit_score: int | None = Field(default=None, ge=300, le=900)
    credit_score_verified: bool = False


class ApplicantResponse(ApplicantCreate):
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
