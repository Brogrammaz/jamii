from sqlalchemy import Column, Integer, String
from jamii.db.session import Base

class User(Base):
    __tablename__ = "tbl_users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    gender = Column(String, index=True)
    hashed_password = Column(String)