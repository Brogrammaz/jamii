from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from jamii.db.models.transaction import Transaction
from jamii.db.schemas.transaction import TransactionCreate, TransactionResponse


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
