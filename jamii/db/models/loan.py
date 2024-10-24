from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LoanRequest(Base):
    __tablename__ = 'loan_requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    loan_amount = Column(Float, nullable=False)
    loan_type = Column(String(100), nullable=False)  # e.g., personal, business, mortgage
    interest_rate = Column(Float, nullable=False)
    repayment_term = Column(Integer, nullable=False)  # In months or years
    
    # Dates for loan request
    application_date = Column(DateTime, nullable=False, default=func.now)  # Date of loan application
    approval_date = Column(DateTime, nullable=True)  # Date loan is approved
    disbursement_date = Column(DateTime, nullable=True)  # Date loan is disbursed
    
    # Approval and status tracking
    approver_name = Column(String(80), nullable=True)
    status = Column(String(20), default='Pending')  # Pending, Approved, Rejected, Disbursed
