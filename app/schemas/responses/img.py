from uuid import UUID
from pydantic import BaseModel

class ImageResponse(BaseModel):
    id: UUID 
    url: str 
    class Config:
        from_attributes=True