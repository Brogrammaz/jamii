from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from jamii.db.session import Base

class Loan(Base):
    __tablename__ = 'tbl_loans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("tbl_users.user_id"), nullable=False)
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
    status = Column(String(20), default='Pending')  # Pending, Approved, Rejected, Disbursed, Repaid

    user = relationship("User", back_populates="loans")