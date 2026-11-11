
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class CreditFacilityCreate(BaseModel):
    facility_id: str = Field(min_length=1, max_length=30)
    applicant_id: str = Field(min_length=1, max_length=30)
    lender_name: str | None = None
    facility_type: str | None = None
    outstanding_balance: Decimal = Field(default=0, ge=0)
    monthly_obligation: Decimal = Field(default=0, ge=0)
    facility_status: str = "ACTIVE"


class CreditFacilityResponse(CreditFacilityCreate):
    reported_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
