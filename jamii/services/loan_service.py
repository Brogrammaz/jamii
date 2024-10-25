from sqlalchemy.orm import Session
from fastapi import HTTPException
from jamii.db.schemas.loan import LoanRequestCreate, LoanRequestResponse
from jamii.db.models.loan import LoanRequest


class LoanService:
    def __init__(self, db: Session):
        self.db = db

    def create_loan_request(self, loan_request: LoanRequestCreate) -> LoanRequestResponse:
        # Create a new loan request
        new_loan = LoanRequest(
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

    def get_loan_request(self, loan_id: int) -> LoanRequestResponse:
        # Retrieve a loan request by ID
        loan_request = self.db.query(LoanRequest).filter(LoanRequest.id == loan_id).first()
        
        if not loan_request:
            raise HTTPException(status_code=404, detail="Loan request not found")
        
        return loan_request

    def update_loan_request(self, loan_id: int, loan_request: LoanRequestCreate) -> LoanRequestResponse:
        # Update an existing loan request
        existing_loan = self.db.query(LoanRequest).filter(LoanRequest.id == loan_id).first()
        
        if not existing_loan:
            raise HTTPException(status_code=404, detail="Loan request not found")

        # Update the loan request attributes
        for var, value in vars(loan_request).items():
            setattr(existing_loan, var, value) if value else None

        self.db.commit()
        self.db.refresh(existing_loan)
        
        return existing_loan

    def delete_loan_request(self, loan_id: int) -> None:
        # Delete a loan request by ID
        loan_request = self.db.query(LoanRequest).filter(LoanRequest.id == loan_id).first()
        
        if not loan_request:
            raise HTTPException(status_code=404, detail="Loan request not found")
        
        self.db.delete(loan_request)
        self.db.commit()
