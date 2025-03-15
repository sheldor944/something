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