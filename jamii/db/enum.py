from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    
class InterestType(str, Enum):
    SIMPLE = "simple"
    COMPOUND = "compound"

class LoanStatus(str, Enum):
    WRITTEN_OFF = "written_off"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FUNDED = "funded"
    REPAID = "repaid"
