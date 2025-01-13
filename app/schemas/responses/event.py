from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.responses.img import ImageResponse

class EventResponse(BaseModel):
    id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    venue: Optional[str] = None
    event_link: Optional[str] = None
    banner: Optional[ImageResponse] = None
    created_by: Optional[UUID] = None
    last_updated_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    last_updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True