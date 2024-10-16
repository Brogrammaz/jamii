from ..db.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from jamii.db.schemas.user import UserCreate
from fastapi import HTTPException, status
from jamii.core.security import verify_password, create_access_token
from datetime import timedelta

from loguru import logger



class UserService:
    def __init__(self, db:Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def get_users(self):
        return self.user_repo.get_users()
    
    def get_user_by_name(self, user_name:str):
        return self.user_repo.get_user_by_username(user_name=user_name)
    
    def get_user_by_email(self, email:str):
        return self.user_repo.get_user_by_email(email=email)

    # service method to create a user
    def create_user(self, user_create: UserCreate):
        # check whether the user already exists
        existing_user = self.user_repo.get_user_by_email(user_create.email)

        if existing_user:
            logger.warning("Failed to create user") # Log failure message
            raise HTTPException(status_code=400, detail="User already exists")
        
        return self.user_repo.create_user(user_create)
    
    # define a function to authenticate the user
    def authenticate_user(self, user_name: str, password: str):
        
        user = self.user_repo.get_user_by_username(user_name)

        if not user or not verify_password(password, user.hashed_password):
            return False
        
        return user
    
    # define the login process
    def login_for_access_token(self, user_name: str, password: str):

        user = self.authenticate_user(user_name, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Kindly check Username or Password incorrect",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub":user.name},
            expires_delta=access_token_expires
            )
        
        return {"access_token":access_token, "token_type":"bearer"}
    

