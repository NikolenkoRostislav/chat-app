from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime
from typing import Annotated
from app.utils.exceptions import InvalidEntryError

def validate_password_complexity(password: str) -> str:
    if not any(c.islower() for c in password):
        raise InvalidEntryError("Password must contain at least one lowercase character")
    if not any(c.isupper() for c in password):
        raise InvalidEntryError("Password must contain at least one uppercase character")
    if not any(c.isdigit() for c in password):
        raise InvalidEntryError("Password must contain at least one digit")
    if all(c.isalnum() for c in password):
        raise InvalidEntryError("Password must contain at least one special character")
    return password

class UserBase(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=25)]
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
    password: Annotated[str, Field(min_length=8, max_length=100)]
    @validator("password")
    def check_password_complexity(cls, v):
        return validate_password_complexity(v)

class UserUpdateEmail(BaseModel):
    email: EmailStr

class UserUpdatePassword(BaseModel):
    password: Annotated[str, Field(min_length=8, max_length=100)]
    
    @validator("password")
    def check_password_complexity(cls, v):
        return validate_password_complexity(v)

class UserUpdateUsername(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=25)]

class UserUpdatePFP(BaseModel):
    pfp_url: str

class UserLogin(BaseModel):
    username: str
    password: str