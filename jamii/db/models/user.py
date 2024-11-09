from sqlalchemy import Column, Integer, String
from jamii.db.session import Base
from sqlalchemy.orm import relationship
from jamii.db import enum
from jamii.db.enum import UserRole

class User(Base):
    __tablename__ = "tbl_users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    gender = Column(String, index=True)
    hashed_password = Column(String)
    role = Column(String, default=UserRole.USER, nullable=False) 

    deposits = relationship("Deposit", back_populates="user")
    loans = relationship("Loan", back_populates="user")
