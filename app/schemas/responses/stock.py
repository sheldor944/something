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