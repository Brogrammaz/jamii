# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jamii.db.schemas.user import UserCreate, UserResponse
from jamii.db.models import user as user_model
from jamii.core.security import verify_password, create_access_token, verify_token
from jamii.api.dependencies.db import get_db
from jamii.db.enum import UserRole
router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Fetch the user from the database
    db_user = db.query(user_model.User).filter(user_model.User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Verify the password
    if not db_user.check_password(form_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Create an access token (assuming you have JWT setup)
    access_token = create_access_token(data={"sub": db_user.email, "role": db_user.role.value})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create a new user instance
    new_user = user_model.User(
        name=user.name,
        email=user.email,
        gender=user.gender,
        role=user.role
    )
    # Hash the password
    new_user.set_password(user.password)
    
    # Add to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def get_current_user_role(token: str):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication credentials")
    return payload["role"]

def role_required(required_role: UserRole):
    def role_dependency(token: str = Depends(get_current_user_role)):
        if token != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return role_dependency