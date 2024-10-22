from sqlalchemy import Column, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from jamii.db.session import Base
from datetime import datetime

class Deposit(Base):
    __tablename__ = "tbl_deposits"

    deposit_id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable = False)
    user_id = Column(Integer, ForeignKey("tbl_users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="deposits")