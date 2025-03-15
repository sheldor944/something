from uuid import UUID
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class TradeCreateRequest(BaseModel):
    stock_id: Optional[UUID] = None
    trade_start_price: Optional[float] = None
    quantity: Optional[float] = None
    trade_start_date: Optional[datetime] = None
    trade_type: Optional[str] = None
    is_Automated: Optional[bool] = None
    trade_done_by: Optional[str] = None

class TradeCloseRequest(BaseModel):
    trade_id : Optional[UUID] = None    
    trade_end_price: Optional[float] = None
    trade_end_date: Optional[datetime] = None

class TradeFilter(BaseModel):
    trade_id : Optional[UUID] = None
    stock_id : Optional[UUID] = None
    symbol : Optional[str] = None
    trade_start_date : Optional[datetime] = None
    trade_end_date : Optional[date] = None
    trade_type : Optional[str] = None
    trade_status : Optional[str] = None
    trade_done_by : Optional[str] = None
    is_Automated : Optional[bool] = None

