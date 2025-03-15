from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TradeResponse(BaseModel):
    id: Optional[UUID] = None
    stock_id: Optional[UUID] = None
    trade_start_price: Optional[float] = None
    trade_end_price: Optional[float] = None
    quantity: Optional[float] = None
    trade_start_date: Optional[datetime] = None
    trade_end_date: Optional[datetime] = None
    trade_type: Optional[str] = None
    trade_status: Optional[str] = None
    trade_profit: Optional[float] = None
    is_Automated: Optional[bool] = None
    trade_done_by: Optional[str] = None
    
    class Config:
        from_attributes = True
    