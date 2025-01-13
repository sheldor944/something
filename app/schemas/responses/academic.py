from pydantic import BaseModel

class DepartmentResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes=True

class ProgramResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes=True

class SessionResponse(BaseModel):
    id: int
    years: str

    class Config:
        from_attributes=True