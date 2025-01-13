from typing import Optional
from pydantic import BaseModel, Field, field_validator

class HallOfFameRequest(BaseModel):   
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)

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

class HallOfFameUpdateRequest(BaseModel):   
    title: Optional[str] = None 
    description: Optional[str] = None

    class Config:
        from_attributes = True
