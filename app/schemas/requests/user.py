from pydantic import BaseModel, Field, EmailStr, field_validator
from uuid import UUID
from typing import Optional

class UserSignUp(BaseModel):
    user_name: Optional[str] = Field(...)
    email: Optional[EmailStr] = Field(...)
    password: Optional[str] = Field(...)

    @field_validator('user_name')
    def user_name_must_not_be_empty(cls, v):
        if v is None or not v.strip():
            raise ValueError('User name must not be empty')
        return v

    @field_validator('email')
    def email_must_not_be_empty(cls, v):
        if v is None or not v.strip():
            raise ValueError('Email must not be empty')
        return v

    @field_validator('password')
    def password_must_not_be_empty(cls, v):
        if v is None or not v.strip():
            raise ValueError('Password must not be empty')
        return v

    class Config:
        from_attributes = True

    
class UserSignIn(BaseModel):
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=8)

    @field_validator('email')
    def email_must_not_be_empty(cls, v):
        if v is None or not v.strip():
            raise ValueError('Email must not be empty')
        return v

    @field_validator('password')
    def password_must_not_be_empty(cls, v):
        if v is None or not v.strip():
            raise ValueError('Password must not be empty')
        return v

    class Config:
        from_attributes = True

    

class ProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    reg_no: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[UUID] = None
    program_id: Optional[UUID] = None
    session_id: Optional[UUID] = None
    codeforces_handle: Optional[str] = None
    atcoder_handle: Optional[str] = None
    vjudge_handle: Optional[str] = None
    discord_handle: Optional[str] = None
    github_handle: Optional[str] = None
    google_account: Optional[str] = None

    class Config:
        from_attributes = True