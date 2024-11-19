from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    transaction_type: str  # Either "credit" or "debit"
    description: Optional[str] = None
    initiator_name: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str  # Either "credit" or "debit"
    description: Optional[str] = None
    transaction_date: datetime
    initiator_name: Optional[str] = None
    status: str  # E.g., "completed", "pending", "failed"

    class Config:
        from_attributes = True
