
from xmlrpc.client import Boolean

from sqlalchemy import Column, String, Date, DateTime, func
from backend.database import Base
from sqlalchemy import (
    Column, String, Date, DateTime, func, Integer, Boolean
)



class Applicant(Base):
    __tablename__ = "applicants"

    applicant_id = Column(String(30), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    date_of_birth = Column(Date)
    email = Column(String(255))
    phone = Column(String(30))
    address = Column(String)
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    created_at = Column(DateTime, server_default=func.current_timestamp())
    credit_score = Column(Integer)
    credit_score_verified = Column(Boolean, default=False)
