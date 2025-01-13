from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from schemas.responses.academic import DepartmentResponse, ProgramResponse, SessionResponse

class TokenBasic(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: UUID
    user_name: str
    email: str

    class Config:
        from_attributes = True

class UserSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    os: Optional[str] = None
    device: Optional[str] = None
    browser: Optional[str] = None

    class Config:
        from_attributes = True

class ProfileResponse(BaseModel):
    user: Optional[UserResponse] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    reg_no: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[DepartmentResponse] = None
    program: Optional[ProgramResponse] = None
    session: Optional[SessionResponse] = None
    codeforces_handle: Optional[str] = None
    atcoder_handle: Optional[str] = None
    vjudge_handle: Optional[str] = None
    discord_handle: Optional[str] = None
    github_handle: Optional[str] = None
    google_account: Optional[str] = None

    class Config:
        from_attributes = True