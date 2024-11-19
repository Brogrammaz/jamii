from sqlalchemy.orm import Session
from fastapi import HTTPException
from jamii.db.schemas.loan import LoanCreate, LoanResponse
from jamii.db.models.loan import Loan


class LoanService:
    def __init__(self, db: Session):
        self.db = db

    def create_loan_request(self, loan_request: LoanCreate) -> LoanResponse:
        # Create a new loan
        new_loan = Loan(
            user_id=loan_request.user_id,
            loan_amount=loan_request.loan_amount,
            loan_type=loan_request.loan_type,
            interest_rate=loan_request.interest_rate,
            repayment_term=loan_request.repayment_term,
            purpose=loan_request.purpose,
            application_date=loan_request,
            approver_name=loan_request.approver_name,
            status="Pending"  # Default status
        )
        
        self.db.add(new_loan)
        self.db.commit()
        self.db.refresh(new_loan)  # Refresh to get the new ID
        
        return new_loan

    def get_loan_request(self, loan_id: int) -> LoanResponse:
        # Retrieve a loan request by ID
        loan_request = self.db.query(Loan).filter(Loan.id == loan_id).first()
        
        if not loan_request:
            raise HTTPException(status_code=404, detail="Loan request not found")
        
        return loan_request

    def update_loan_request(self, loan_id: int, loan_request: LoanCreate) -> LoanResponse:
        # Update an existing loan request
        existing_loan = self.db.query(Loan).filter(Loan.id == loan_id).first()
        
        if not existing_loan:
            raise HTTPException(status_code=404, detail="Loan request not found")

        # Update the loan request attributes
        for var, value in vars(loan_request).items():
            setattr(existing_loan, var, value) if value else None

        self.db.commit()
        self.db.refresh(existing_loan)
        
        return existing_loan

    def soft_delete_loan_service(db: Session, loan_id: int) -> LoanResponse:
        loan = db.query(loan).filter(loan.id == loan_id).first()
        if not loan:
         raise HTTPException(status_code=404, detail="Loan not found")
        loan.status = "Deleted"
        db.commit()
        db.refresh(loan)
        return loan
