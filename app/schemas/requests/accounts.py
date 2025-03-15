from uuid import UUID
from datetime import date as Date, datetime, date
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class AccountRequest(BaseModel):
    # user_id: Optional[UUID] = None
    balance: Optional[float] = None
    automated_balance: Optional[float] = None
    currency: Optional[str] = None
    class Config:
        from_attributes = True

class AccountUpdateRequest(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    # automated_balance: Optional[float] = None
    modificationType: Optional[bool] = None # True for addition and False for subtraction
    # modificationTypeAutomated: Optional[bool] = None # True for addition and False for subtraction
    class Config:
        from_attributes = True

class TransactionRequest(BaseModel):
    # account_id: UUID = None
    amount: float = None  # Changed from transaction_amount to amount
    symbol: Optional[str] = None
    transaction_type: Optional[str] = None
    transaction_date: Optional[datetime] = None
    transaction_status: Optional[str] = None
    transaction_done_by: Optional[str] = None
    
    class Config:
        from_attributes = True

class AutomatedAccountRequest(BaseModel):
    balance: float = None
    class Config:
        from_attributes = True

class AutomatedAccountUpdateRequest(BaseModel):
    amount: float = None
    modificationTypeAutomated: Optional[bool] = None # True for addition and False for subtraction
    class Config:
        from_attributes = True