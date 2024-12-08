from sqlalchemy.orm import Session
from fastapi import HTTPException
from fpdf import FPDF
from datetime import datetime
from jamii.db.models.transaction import Transaction
from jamii.db.schemas.transaction import TransactionCreate, TransactionResponse
import numpy as np

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    # Create a new transaction
    def create_transaction(self, transaction_data: TransactionCreate) -> TransactionResponse:
        new_transaction = Transaction(
            user_id=transaction_data.user_id,
            transaction_type=transaction_data.transaction_type,
            amount=transaction_data.amount,
            description=transaction_data.description,
            status="Pending",  # Default status
            transaction_date=datetime.now(),
        )
        
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_transaction)
        return new_transaction

    # Get a transaction by ID
    def get_transaction(self, transaction_id: int) -> TransactionResponse:
        transaction = self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction

    # Get all transactions
    def get_all_transactions(self):
        return self.db.query(Transaction).all()

    # Get transactions by user ID
    def get_transactions_by_user(self, user_id: int):
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).all()

    # Update a transaction
    def update_transaction(self, transaction_id: int, transaction_data: TransactionCreate) -> TransactionResponse:
        transaction = self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Update attributes
        for var, value in vars(transaction_data).items():
            setattr(transaction, var, value) if value else None

        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    # Soft delete a transaction
    def soft_delete_transaction_service(db: Session, transaction_id: int) -> TransactionResponse:
        transaction = db.query(transaction).filter(transaction.id == transaction_id).first()
        if not transaction:
         raise HTTPException(status_code=404, detail="transaction not found")
        transaction.status = "Deleted"
        db.commit()
        db.refresh(transaction)
        return transaction
    
    def transactions_to_table(transactions):
     """
    Converts transaction data into a tabular format for PDF generation.
    """
    # Add headers
    data = [["Transaction ID", "User", "Amount", "Date"]]
    
    # Add rows
    data.extend(
        [
            [tx.id, tx.user.name, f"${tx.amount}", tx.date.strftime("%Y-%m-%d")]
            for tx in transactions_to_table
        ]
    )

def generate_pdf(data, output_path="transactions.pdf"):
    try:
        if not data or len(data) <= 1:  # Header row only
            raise ValueError("No data available for PDF generation.")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for row in data:
            pdf.cell(200, 10, txt=" | ".join(map(str, row)), ln=True)
        
        pdf.output(output_path)
    except Exception as e:
        raise RuntimeError(f"Failed to generate PDF: {e}")
    

def calculate_interest(principal: float, rate: float, time: float, compound: bool = False):
    """
    Calculate interest based on deposit or loan using simple or compound interest.

    Args:
        principal (float): The principal amount (e.g., deposit or loan).
        rate (float): Annual interest rate (e.g., 0.05 for 5%).
        time (float): Time in years.
        compound (bool): Whether to calculate compound interest. Default is False.

    Returns:
        dict: A dictionary with calculated interest and total amount.
    """
    if compound:
        # Compound interest
        future_value = principal * np.power(1 + rate, time)
        interest = future_value - principal
        return {
            "principal": principal,
            "rate": rate,
            "time": time,
            "interest": round(interest, 2),
            "total_amount": round(future_value, 2),
        }
    else:
        # Simple interest
        interest = principal * rate * time
        total_amount = principal + interest
        return {
            "principal": principal,
            "rate": rate,
            "time": time,
            "interest": round(interest, 2),
            "total_amount": round(total_amount, 2),
        }
    
def determine_interest_type(principal, time):
    """
    Determines whether to apply simple or compound interest.
    """
    if principal >1000 and time >1:
        return "simple"
    else:
        return "compound"

def get_loan_rate(amount: float) -> float:
    """
    Returns an interest rate based on the loan amount.
    """
    if amount <= 5000:
        return 0.05  # 5% for loans <= 5000
    elif amount <= 20000:
        return 0.07  # 7% for loans <= 20000
    else:
        return 0.1   # 10% for loans > 20000

def get_deposit_rate(amount: float) -> float:
    """
    Returns an interest rate based on the deposit amount.
    """
    if amount <= 1000:
        return 0.03  # 3% for deposits <= 1000
    elif amount <= 10000:
        return 0.04  # 4% for deposits <= 10000
    else:
        return 0.05  # 5% for deposits > 10000

# Example: Loan interest calculation
loan_amount = 15000
loan_rate = get_loan_rate(loan_amount)
loan_interest = calculate_interest(principal=loan_amount, rate=loan_rate, time=2, compound=True)
print("Loan Interest:", loan_interest)

# Example: Deposit interest calculation
deposit_amount = 5000
deposit_rate = get_deposit_rate(deposit_amount)
deposit_interest = calculate_interest(principal=deposit_amount, rate=deposit_rate, time=1, compound=False)
print("Deposit Interest:", deposit_interest)
