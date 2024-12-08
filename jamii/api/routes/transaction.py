from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from jamii.api.dependencies.db import get_db
from jamii.services.transaction_service import TransactionService
from jamii.db.schemas.transaction import TransactionCreate
from jamii.db.repositories.transaction_repository import get_all_transactions
from jamii.services import transactions_to_table, generate_pdf
from loguru import logger
import os

router = APIRouter()

@router.get("/download/transactions")
def download_pdf(db: Session = Depends(get_db)):
    """
    Endpoint to download the transactions PDF.
    """
    try:
        # Fetch transactions from the database
        transactions = get_all_transactions(db)
        
        if not transactions:
            raise HTTPException(status_code=404, detail="No transactions found to generate PDF.")

        # Convert transactions to table format
        data = transactions_to_table(transactions)
        
        # Generate the PDF
        pdf_path = "transactions.pdf"
        generate_pdf(data, output_path=pdf_path)
        
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="Failed to generate PDF file.")

        # Serve the PDF file as a response
        return FileResponse(pdf_path, media_type="application/pdf", filename="transactions.pdf")
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching transactions: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred while fetching transactions.")
    except Exception as e:
        logger.error(f"Unexpected error during PDF generation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF.")

@router.get("/user-transactions")
def get_user_transactions(user_id: int = None, email: str = None, db: Session = Depends(get_db)):
    """
    Retrieve the latest transactions of a user based on user ID or email.
    """
    try:
        transaction_service = TransactionService(db)
        transactions = transaction_service.get_user_transactions(user_id=user_id, email=email)

        if not transactions:
            raise HTTPException(status_code=404, detail="User not found or no transactions available.")
        
        return transactions
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving user transactions: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred while fetching user transactions.")
    except Exception as e:
        logger.error(f"Unexpected error during user transaction retrieval: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user transactions.")

@router.post("/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """
    Create a new transaction for a user.
    """
    try:
        transaction_service = TransactionService(db)
        created_transaction = transaction_service.create_transaction(transaction)
        return created_transaction
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating transaction: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred while creating transaction.")
    except Exception as e:
        logger.error(f"Unexpected error during transaction creation: {e}")
        raise HTTPException(status_code=500, detail="Transaction creation failed.")

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a transaction by its ID.
    """
    try:
        transaction_service = TransactionService(db)
        result = transaction_service.soft_delete_transaction(transaction_id)
        return result
    except HTTPException as e:
        logger.error(f"Error during transaction deletion: {e.detail}")
        raise e
    except SQLAlchemyError as e:
        logger.error(f"Database error while deleting transaction {transaction_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred while deleting transaction.")
    except Exception as e:
        logger.error(f"Unexpected error during transaction deletion: {e}")
        raise HTTPException(status_code=500, detail="Transaction deletion failed.")
