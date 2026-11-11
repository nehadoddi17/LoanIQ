
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LoanDecisionResponse(BaseModel):
    decision_id: str
    application_id: str
    decision: str
    reason: str | None = None
    decided_by: str | None = None
    decision_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
