from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from fastapi import HTTPException
from jamii.db.models.transaction import Transaction  # Assuming your Transaction model is here
from jamii.db.schemas.transaction import TransactionCreate

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    # Get all transactions
    def get_all_transactions(self):
        return self.db.query(Transaction).all()

    # Get a transaction by ID
    def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    # Get transactions by user ID
    def get_transactions_by_user_id(self, user_id: int):
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).all()

    # Create a new transaction
    def create_transaction(self, transaction: TransactionCreate):
        db_transaction = Transaction(
            user_id=transaction.user_id,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type,
            description=transaction.description,
            transaction_date=datetime.now(),
            status="Pending",  # Default status is pending
            initiator_name=transaction.initiator_name
        )
        
        self.db.add(db_transaction)

        try:
            self.db.commit()
            self.db.refresh(db_transaction)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Transaction creation failed.")
        
        return db_transaction

    # Update transaction status
    def update_transaction_status(self, transaction_id: int, status: str):
        transaction = self.get_transaction_by_id(transaction_id)
        
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found.")

        transaction.status = status

        try:
            self.db.commit()
            self.db.refresh(transaction)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Failed to update transaction status.")
        
        return transaction

    # Delete a transaction
    def delete_transaction(self, transaction_id: int):
        transaction = self.get_transaction_by_id(transaction_id)
        
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found.")
        
        self.db.delete(transaction)
        self.db.commit()

        return {"message": "Transaction deleted successfully."}
