
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class InstallmentResponse(BaseModel):
    installment_id: str
    schedule_id: str
    installment_number: int
    due_date: date
    principal_component: Decimal | None
    interest_component: Decimal | None
    installment_amount: Decimal | None
    payment_status: str

    model_config = ConfigDict(from_attributes=True)


class RepaymentScheduleResponse(BaseModel):
    schedule_id: str
    application_id: str
    principal_amount: Decimal
    total_interest: Decimal | None
    total_payable: Decimal | None
    expected_installment_count: int | None
    calculated_installment_total: Decimal | None
    reconciliation_status: str
    generated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
