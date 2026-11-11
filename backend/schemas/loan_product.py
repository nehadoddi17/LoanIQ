
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class LoanProductCreate(BaseModel):
    product_id: str = Field(min_length=1, max_length=30)
    product_name: str = Field(min_length=1, max_length=150)
    min_loan_amount: Decimal = Field(gt=0)
    max_loan_amount: Decimal = Field(gt=0)
    min_term_months: int = Field(gt=0)
    max_term_months: int = Field(gt=0)
    annual_interest_rate: Decimal = Field(ge=0, le=100)
    min_credit_score: int | None = Field(default=None, ge=300, le=900)
    active: bool = True

    @model_validator(mode="after")
    def validate_ranges(self):
        if self.min_loan_amount > self.max_loan_amount:
            raise ValueError("Minimum loan amount cannot exceed maximum")
        if self.min_term_months > self.max_term_months:
            raise ValueError("Minimum tenure cannot exceed maximum")
        return self


class LoanProductResponse(LoanProductCreate):
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
