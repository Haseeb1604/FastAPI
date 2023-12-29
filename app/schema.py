from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_At: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class _Base(BaseModel):
    title: str
    content: str 
    published: bool = True

class PostCreate(_Base):
    pass

class Post(_Base):
    id: int
    created_At: datetime
    owner: UserOut
    # class config:
    #     orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None