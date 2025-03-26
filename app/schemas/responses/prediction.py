from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PredictionResponse(BaseModel):
    id: Optional[UUID] = None
    stock_id: Optional[UUID] = None
    symbol: Optional[str] = None
    opening_price: Optional[float] = None
    closing_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    volume: Optional[float] = None
    date: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CurrentPredictionResponse(BaseModel):
    id: Optional[UUID] = None
    symbol: Optional[str] = None
    opening_price: Optional[float] = None
    closing_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    volume: Optional[float] = None
    prediction_direction: Optional[bool] = None
    date: Optional[datetime] = None
    
    class Config:
        from_attributes = True