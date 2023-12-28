from pydantic import BaseModel, EmailStr
from datetime import datetime
class _Base(BaseModel):
    title: str
    content: str 
    published: bool = True

class PostCreate(_Base):
    pass

class Post(_Base):
    id: int
    created_At: datetime
    # class config:
    #     orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_At: datetime