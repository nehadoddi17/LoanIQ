
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class EmploymentCreate(BaseModel):
    employment_id: str = Field(min_length=1, max_length=30)
    applicant_id: str = Field(min_length=1, max_length=30)
    employer_name: str | None = None
    employment_type: str | None = None
    job_title: str | None = None
    employment_start_date: date | None = None
    annual_salary: Decimal | None = Field(default=None, ge=0)
    employment_status: str | None = None


class EmploymentResponse(EmploymentCreate):
    created_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
