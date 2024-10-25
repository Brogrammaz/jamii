from sqlalchemy import Column, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from jamii.db.session import Base
from datetime import datetime

class Deposit(Base):
    __table__ = "tbl_deposits"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable = False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="deposits")