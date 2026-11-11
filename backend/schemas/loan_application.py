
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class LoanApplicationCreate(BaseModel):
    application_id: str = Field(min_length=1, max_length=30)
    applicant_id: str = Field(min_length=1, max_length=30)
    product_id: str = Field(min_length=1, max_length=30)
    requested_amount: Decimal = Field(gt=0)
    requested_term_months: int = Field(gt=0)


class LoanApplicationResponse(LoanApplicationCreate):
    application_status: str
    submitted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
