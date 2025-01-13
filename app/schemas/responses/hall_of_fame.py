from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from schemas.responses.user import UserResponse
from schemas.responses.img import ImageResponse

class HallOfFameResponse(BaseModel):
    id: Optional[UUID] = None
    title: Optional[str]
    description: Optional[str] 
    created_by: Optional[UUID] = None
    last_updated_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    last_updated_at: Optional[datetime] = None

    people: Optional[List[UserResponse]] = None
    images: Optional[List[ImageResponse]] = None 

    class Config:
        from_attributes = True