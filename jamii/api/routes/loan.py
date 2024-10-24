from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from jamii.db.models.loan import LoanRequest  # Ensure LoanRequest is correctly imported
from jamii.db.schemas.loan import LoanRequestCreate, LoanRequestResponse  
from datetime import datetime 

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Create the loan request
@app.post("/loan_requests/", response_model=LoanRequestResponse)
def create_loan_request(loan_request: LoanRequestCreate, db: Session = Depends(get_db)):
    new_loan = LoanRequest(
        user_id=loan_request.user_id,  # Ensure correct field mapping
        loan_amount=loan_request.loan_amount,
        loan_type=loan_request.loan_type,
        interest_rate=loan_request.interest_rate,
        repayment_term=loan_request.repayment_term,
        purpose=loan_request.purpose,
        application_date=datetime.now(),  # Set to now if not provided
        approver_name=loan_request.approver_name,  # Check if this is necessary
        status="Pending"
    )
    
    db.add(new_loan)
    try:
        db.commit()
        db.refresh(new_loan)  # Refresh to get the new ID
    except Exception as e:
        db.rollback()  # Roll back on error
        raise HTTPException(status_code=400, detail="Error creating loan request: " + str(e))
    
    return new_loan

# Get a loan request by ID
@app.get("/loan_requests/{loan_id}", response_model=LoanRequestResponse)
def get_loan_request(loan_id: int, db: Session = Depends(get_db)):
    loan_request = db.query(LoanRequest).filter(LoanRequest.id == loan_id).first()
    
    if not loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found")
    
    return loan_request