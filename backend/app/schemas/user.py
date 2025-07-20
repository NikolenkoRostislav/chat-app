from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    pfp_url: str | None = None

class UserReadPublic(UserBase):
    id: int
    last_online: datetime

    class Config:
        from_attributes = True

class UserReadPrivate(UserReadPublic):
    email: EmailStr

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    pfp_url: str | None = None
    password: str | None = None
