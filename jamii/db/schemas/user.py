from pydantic import BaseModel, EmailStr


# Pydantic schema for User Creation
class UserCreate(BaseModel):

    user_id: int
    name: str
    email: EmailStr 
    gender: str
    password: str
    
class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    gender: str

    class Config:
        orm_mode = True # Enables reading from SQLAlchemy models.