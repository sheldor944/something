from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StockResponse(BaseModel):
    id: UUID
    name: Optional[str] = None
    symbol: Optional[str] = None
    created_at: Optional[datetime] = None
    last_updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StockPriceResponse(BaseModel):
    id: UUID
    stock_id: UUID
    startPrice: Optional[float] = None
    endPrice: Optional[float] = None
    highPrice: Optional[float] = None
    lowPrice: Optional[float] = None
    volume: Optional[float] = None
    date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    last_updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True