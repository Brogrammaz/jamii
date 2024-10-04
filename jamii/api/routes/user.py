from fastapi import APIRouter, Depends
from ..dependencies.db import get_db
from sqlalchemy.orm import Session
from jamii.services.user_service import UserService
from jamii.db.schemas.user import UserCreate, UserResponse
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from loguru import logger



router = APIRouter()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return UserService(db).get_users()

@router.post("/token")
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db_session = Depends(get_db)):
    return UserService(db_session).login_for_access_token(
        form_data.username,
        form_data.password
    )

@router.post("/user", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.create_user(user)
    if db_user:
        logger.info(f"User {db_user.email} created successfully")
        return db_user
    else:
        logger.error(f"Failed to create user") # Log failure message
        raise HTTPException(status_code=400, detail="User Could not be created")
