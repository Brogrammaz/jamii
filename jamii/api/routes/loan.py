# jamii/api/routes/loan.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jamii.db.models.loan import Loan
from jamii.db.schemas.loan import LoanCreate, LoanResponse
from jamii.api.dependencies.db import get_db
from datetime import datetime

router = APIRouter()

# Create the loan request
@router.post("/loan_requests/", response_model=LoanResponse)
def create_loan_request(loan_request: LoanCreate, db: Session = Depends(get_db)):
    new_loan = Loan(
        user_id=loan_request.user_id,
        loan_amount=loan_request.loan_amount,
        loan_type=loan_request.loan_type,
        interest_rate=loan_request.interest_rate,
        repayment_term=loan_request.repayment_term,
        purpose=loan_request.purpose,
        application_date=datetime.now(),
        approver_name=loan_request.approver_name,
        status="Pending"
    )
    
    db.add(new_loan)
    try:
        db.commit()
        db.refresh(new_loan)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating loan request: " + str(e))
    
    return new_loan

# Get a loan request by ID
@router.get("/loan_requests/{loan_id}", response_model=LoanResponse)
def get_loan_request(loan_id: int, db: Session = Depends(get_db)):
    loan_request = db.query(Loan).filter(Loan.id == loan_id).first()
    
    if not loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found")
    
    return loan_request

# Soft delete a loan request
@router.delete("/loan_requests/{loan_id}", response_model=LoanResponse)
def soft_delete_loan_request(loan_id: int, db: Session = Depends(get_db)):
    loan_request = db.query(Loan).filter(Loan.id == loan_id).first()

    if not loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found")

    # Soft delete by updating status
    loan_request.status = "Deleted"
    db.commit()
    db.refresh(loan_request)
    
    return loan_request