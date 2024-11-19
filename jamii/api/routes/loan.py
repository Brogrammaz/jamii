from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jamii.api.dependencies.db import get_db
from jamii.services.loan_service import LoanService
from jamii.db.schemas.loan import LoanCreate
from loguru import logger

router = APIRouter()

@router.get("/user-loans")
def get_user_loans(user_id: int = None, email: str = None, db: Session = Depends(get_db)):
    """
    Retrieve the latest loans of a user based on user ID or email.
    """
    loan_service = LoanService(db)

    loans = loan_service.get_user_loans(user_id=user_id, email=email)

    if loans is None or not loans:
        raise HTTPException(status_code=404, detail="User not found or no loans available")
    
    return loans


@router.post("/")
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    """
    Create a new loan request for a user.
    """
    loan_service = LoanService(db)

    try:
        created_loan = loan_service.create_loan(loan)
        return created_loan
    except Exception as e:
        logger.error(f"Error creating loan: {e}")
        raise HTTPException(status_code=500, detail="Loan creation failed")


@router.delete("/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a loan request by its ID.
    """
    loan_service = LoanService(db)

    try:
        result = loan_service.soft_delete_loan(loan_id)
        return result
    except HTTPException as e:
        logger.error(f"Error deleting loan: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during loan deletion: {e}")
        raise HTTPException(status_code=500, detail="Loan deletion failed")
