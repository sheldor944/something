from uuid import UUID
from datetime import date as Date
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class PredictionRequest(BaseModel):
    stock_id: Optional[UUID] = None
    symbol: Optional[str] = None
    opening_price: Optional[float] = None
    closing_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    volume: Optional[float] = None
    date: Optional[Date] = None

class PredictionFilter(BaseModel):
    prediction_id: Optional[UUID] = None
    stock_id: Optional[UUID] = None
    symbol: Optional[str] = None 
    startDate: Optional[Date] = None
    endDate: Optional[Date] = None
    exactDate: Optional[Date] = None
    created_at: Optional[Date] = None
    last_updated_at: Optional[Date] = None
    class Config:
        from_attributes = True
