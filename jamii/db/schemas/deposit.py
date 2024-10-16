from pydantic import BaseModel
from datetime import datetime

class DepositBase(BaseModel):
    amount: float
    member_id: int


class DepositCreate(DepositBase):
    
    deposit_id:int
    created_at: datetime

    class Config:
        orm_mode = True