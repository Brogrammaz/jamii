from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jamii.api.dependencies.db import get_db
from jamii.services.transaction_service import TransactionService
from jamii.db.schemas.transaction import TransactionCreate
from loguru import logger

router = APIRouter()

@router.get("/user-transactions")
def get_user_transactions(user_id: int = None, email: str = None, db: Session = Depends(get_db)):
    """
    Retrieve the latest transactions of a user based on user ID or email.
    """
    transaction_service = TransactionService(db)

    transactions = transaction_service.get_user_transactions(user_id=user_id, email=email)

    if transactions is None or not transactions:
        raise HTTPException(status_code=404, detail="User not found or no transactions available")
    
    return transactions


@router.post("/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """
    Create a new transaction for a user.
    """
    transaction_service = TransactionService(db)

    try:
        created_transaction = transaction_service.create_transaction(transaction)
        return created_transaction
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(status_code=500, detail="Transaction creation failed")


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a transaction by its ID.
    """
    transaction_service = TransactionService(db)

    try:
        result = transaction_service.soft_delete_transaction(transaction_id)
        return result
    except HTTPException as e:
        logger.error(f"Error deleting transaction: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during transaction deletion: {e}")
        raise HTTPException(status_code=500, detail="Transaction deletion failed")
