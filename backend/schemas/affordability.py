
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class AffordabilityResponse(BaseModel):
    check_id: str
    application_id: str
    monthly_income: Decimal
    monthly_existing_obligations: Decimal
    proposed_emi: Decimal
    debt_to_income_ratio: Decimal
    disposable_income: Decimal
    check_status: str
    checked_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
