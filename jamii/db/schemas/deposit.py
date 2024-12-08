from pydantic import BaseModel
from datetime import datetime

class DepositBase(BaseModel):
    amount: float
    user_id: int
    interest_rate:float
    interest_type:str


class DepositCreate(DepositBase):
    
    deposit_id:int
    created_at: datetime

    class Config:
        orm_mode = True