from typing import Optional
from pydantic import BaseModel, Field, field_validator

class StockRequest(BaseModel):
    name : Optional[str] = None
    symbol : Optional[str] = None