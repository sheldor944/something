from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class EventRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    start_date: datetime = Field(...)
    end_date: datetime = Field(...)
    venue: Optional[str] = None
    event_link: Optional[str] = None

    @field_validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title must not be empty")
        return v
    
    @field_validator("description")
    def description_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Description must not be empty")
        return v

    class Config:
        from_attributes = True


class EventUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    venue: Optional[str] = None
    event_link: Optional[str] = None

    class Config:
        from_attributes = True


    