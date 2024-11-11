from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserLogin(BaseModel):
    user_name: str
    password: str


class UserCreate(UserLogin):
    email: EmailStr


class UserOut(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class ChatQuery(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str
