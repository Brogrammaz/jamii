from ..db.repositories.deposit_repository import DepositRepository
from sqlalchemy.orm import Session
from jamii.db.schemas.deposit import DepositCreate
from fastapi import HTTPException, status
from datetime import timedelta

from loguru import logger


class DepositService:
    def __init__(self, db:Session):
        self.db = db
        self.deposit_repo = DepositRepository(db)

    def get_user_latest_deposit(self, user_id:int = None, email:str = None):
            return self.deposit_repo.get_latest_user_deposit(user_id=user_id, email=email)
        
    def create_deposit(self, deposit:DepositCreate):
            return self.deposit_repo.add_deposit(deposit)
        
