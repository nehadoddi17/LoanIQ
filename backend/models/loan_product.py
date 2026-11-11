
from sqlalchemy import Column, String, Numeric, Integer, Boolean, DateTime, func
from backend.database import Base


class LoanProduct(Base):
    __tablename__ = "loan_products"

    product_id = Column(String(30), primary_key=True)
    product_name = Column(String(150), nullable=False)
    min_loan_amount = Column(Numeric(14, 2), nullable=False)
    max_loan_amount = Column(Numeric(14, 2), nullable=False)
    min_term_months = Column(Integer, nullable=False)
    max_term_months = Column(Integer, nullable=False)
    annual_interest_rate = Column(Numeric(7, 4), nullable=False)
    min_credit_score = Column(Integer)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.current_timestamp())
