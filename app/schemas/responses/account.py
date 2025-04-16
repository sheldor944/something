from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccountResponse(BaseModel):
    id: UUID
    user_id: UUID
    balance: float
    automated_balance: float
    currency: str
    created_at: datetime
    last_updated_at: datetime
    class Config:
        from_attributes = True

class Transaction(BaseModel):
    id: UUID
    account_id: UUID
    amount: float
    transaction_type: str
    transaction_date: datetime
    transaction_status: str
    created_at: datetime
    last_updated_at: datetime
    transaction_done_by: str
    class Config:
        from_attributes = True

class AutomatedAccountHandlerResponse(BaseModel):
    id: UUID
    automated_account_id: UUID
    user_id: UUID
    symbol: str
    start_time: datetime
    end_time: datetime
    profit_lower_bound: float
    profit_upper_bound: float
    profit: Optional[float]
    status: Optional[str]
    balance: Optional[float]   
    class Config:
        from_attributes = True

# make a response for automated account
class AutomatedAccountResponse(BaseModel):
    id: UUID
    balance: float
    # automated_handler: Optional[AutomatedAccountHandlerResponse]
    class Config:
        from_attributes = True