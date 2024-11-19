from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from fastapi import HTTPException
from jamii.db.models.loan import Loan  # Assuming your LoanRequest model is here
from jamii.db.schemas.loan import LoanCreate

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    # Get all loans
    def get_all_loans(self):
        return self.db.query(Loan).all()

    # Get a loan by ID
    def get_loan_by_id(self, loan_id: int) -> Loan:
        return self.db.query(Loan).filter(Loan.id == loan_id).first()

    # Get loans by employee ID
    def get_loans_by_employee_id(self, employee_id: int):
        return self.db.query(Loan).filter(Loan.employee_id == employee_id).all()

    # Create a new loan request
    def create_loan(self, loan: LoanCreate):
        db_loan = Loan(
            user_id=loan.user_id,
            loan_amount=loan.loan_amount,
            loan_type=loan.loan_type,
            interest_rate=loan.interest_rate,
            repayment_term=loan.repayment_term,
            purpose=loan.purpose,
            application_date=datetime.now(),
            status="Pending"  # Default status is pending
        )
        
        self.db.add(db_loan)

        try:
            self.db.commit()
            self.db.refresh(db_loan)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Loan creation failed.")
        
        return db_loan

    # Update loan status
    def update_loan_status(self, loan_id: int, status: str):
        loan = self.get_loan_by_id(loan_id)
        
        if loan is None:
            raise HTTPException(status_code=404, detail="Loan not found.")

        loan.status = status
        loan.approval_date = datetime.now() if status == "Approved" else loan.approval_date

        try:
            self.db.commit()
            self.db.refresh(loan)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Failed to update loan status.")
        
        return loan

    # Delete a loan request
    def delete_loan(self, loan_id: int):
        loan = self.get_loan_by_id(loan_id)
        
        if loan is None:
            raise HTTPException(status_code=404, detail="Loan not found.")
        
        self.db.delete(loan)
        self.db.commit()

        return {"message": "Loan deleted successfully."}