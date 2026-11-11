
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class DisbursementResponse(BaseModel):
    disbursement_id: str
    application_id: str
    amount: Decimal
    disbursement_status: str
    disbursed_at: datetime | None
    transaction_reference: str | None

    model_config = ConfigDict(from_attributes=True)
