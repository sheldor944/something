from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel, Field, field_validator

class StockRequest(BaseModel):
    name : Optional[str] = None
    symbol : Optional[str] = None

class StockPriceRequest(BaseModel):
    startPrice : Optional[float]
    endPrice : Optional[float]
    highPrice : Optional[float]
    lowPrice : Optional[float]
    volume : Optional[float]
    date : Optional[date]

class StockPriceFilter(BaseModel):
    startDate : Optional[date] = None
    endDate : Optional[date] = None