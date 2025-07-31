from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Here are the schemas used throughout the app.

class EventBase(BaseModel):
    name: str
    description: Optional[str]
    date: datetime
    duration: int

class EventCreate(EventBase):
    pass

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Event(EventBase):
    id: int
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class EventOut(EventBase):
    id: int

    class Config:
        orm_mode = True

class EventOutAdmin(EventOut):
    owner_id: int