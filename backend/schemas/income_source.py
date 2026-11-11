
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class IncomeSourceCreate(BaseModel):
    income_source_id: str = Field(min_length=1, max_length=30)
    applicant_id: str = Field(min_length=1, max_length=30)
    source_type: str | None = None
    source_name: str | None = None
    monthly_amount: Decimal = Field(gt=0)
    verification_status: str = "PENDING"


class IncomeSourceResponse(IncomeSourceCreate):
    reported_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
