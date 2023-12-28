from pydantic import BaseModel
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