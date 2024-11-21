from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from fastapi import Form


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


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


@form_body
class ChatQuery(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str
