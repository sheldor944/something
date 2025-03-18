from uuid import UUID
from datetime import date as Date, datetime
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
    date: Optional[datetime] = None
    prediction_direction: Optional[bool] = None
    class Config:
        from_attributes = True

class PredictionFilter(BaseModel):
    prediction_id: Optional[UUID] = None
    stock_id: Optional[UUID] = None
    symbol: Optional[str] = None 
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    exactDate: Optional[datetime] = None
    created_at: Optional[datetime] = None
    last_updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
