from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoanCreate(BaseModel):
    user_id: int
    loan_amount: float
    loan_type: str
    interest_rate: float
    repayment_term: int
    purpose: Optional[str] = None

class LoanResponse(BaseModel):
    id: int
    user_id: int
    loan_amount: float
    loan_type: str
    interest_rate: float
    repayment_term: int
    purpose: Optional[str] = None
    application_date: datetime
    approval_date: Optional[datetime] = None
    disbursement_date: Optional[datetime] = None
    approver_name: Optional[str] = None
    status: str

    class Config:
        from_attributes = True