from fastapi import APIRouter, Depends
from jamii.api.dependencies.db import get_db
from sqlalchemy.orm import Session
from jamii.services.deposit_service import DepositService
from jamii.db.schemas.deposit import DepositCreate

from fastapi import HTTPException
from loguru import logger


router = APIRouter()

@router.get("/user-deposit")
def get_user_deposit(user_id:int = None, email:str = None, db:Session = Depends(get_db)):

    deposit_service = DepositService(db)

    deposits = deposit_service.get_user_latest_deposit(user_id=user_id, email=email)

    if deposits is None:
        raise HTTPException(status_code=404, details ="User not found or User has no deposits yet")
    
    return deposits