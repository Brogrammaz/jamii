from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from jamii.db.models.deposit import Deposit
from jamii.db.models.user import User
from jamii.db.schemas.deposit import DepositCreate

from fastapi import HTTPException

class DepositRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_latest_user_deposit(self, user_id:int = None, email:str = None):
        
        if email:
            user = self.db.query(User).filter(User.email == email).first()
        elif user_id:
            user = self.db.query(User).filter(User.user_id == user_id)
        else:
            
            return None
        
        if user:
            return user.deposits
        
        return None
    

    def get_all_deposits(self, user_id):
        pass

    def add_deposit(self, deposit:DepositCreate):

        user_deposit = DepositCreate(
            amount=deposit.amount,
            member_id=deposit.member_id,
            deposit_id=deposit.deposit_id,
            created_at=deposit.created_at
        )

        self.db.add(user_deposit)

        try:
            self.db.commit()
            self.db.refresh(user_deposit)

        except IntegrityError:
            self.db.rollback()
            return HTTPException(status_code=400, detail="Transaction id already exists.")
        
        return user_deposit
