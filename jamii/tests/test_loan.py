# tests/test_loan.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jamii.main import app
from jamii.db.session import Base, get_db
from jamii.db.schemas.loan import LoanRequestCreate

# Configure a test database (in-memory SQLite for this example)
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test tables in the database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)  # Create tables
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)    # Drop tables after test run

def test_create_loan_request(test_db):
    loan_data = {
        "user_id": 1,
        "loan_amount": 1000.0,
        "loan_type": "personal",
        "interest_rate": 5.0,
        "repayment_term": 12,
        "purpose": "Medical expenses",
        "approver_name": "John Doe"
    }
    
    response = client.post("/api/loan_requests/", json=loan_data)
    assert response.status_code == 200
    assert response.json()["loan_amount"] == loan_data["loan_amount"]
    assert response.json()["status"] == "Pending"

def test_get_loan_request(test_db):
    # First create a loan request
    loan_data = {
        "user_id": 1,
        "loan_amount": 1000.0,
        "loan_type": "personal",
        "interest_rate": 5.0,
        "repayment_term": 12,
        "purpose": "Medical expenses",
        "approver_name": "John Doe"
    }
    response = client.post("/api/loan_requests/", json=loan_data)
    loan_id = response.json()["id"]
    
    # Now test fetching the loan request by ID
    response = client.get(f"/api/loan_requests/{loan_id}")
    assert response.status_code == 200
    assert response.json()["loan_amount"] == loan_data["loan_amount"]
    assert response.json()["status"] == "Pending"

