from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError
from jamii.db.models.user import User
from jamii.db.schemas.user import UserCreate
from fastapi import HTTPException
from jamii.core.security import get_password_hash



class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    # get all users.
    def get_users(self):
        return self.db.query(User).all()
    
    # get user by email.
    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
    

    # get user by username
    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.name == username).first()

    # create use and commit to the db.
    def create_user(self, user:UserCreate):

        hashed_password = get_password_hash(user.password)

        db_user = User(
            name=user.name, 
            email=user.email, 
            gender = user.gender,
            hashed_password = hashed_password           
            )
        
        self.db.add(db_user)

        try:
            self.db.commit() # save to the DB
            self.db.refresh(db_user) # refresh the instance with new data from the db
        
        except IntegrityError: # handle unique constraint violation
            self.db.rollback() # Rollback the session
            return HTTPException(status_code=400, detail="User with this email already exists.") # return None if User already exists
        
        return db_user
    
   