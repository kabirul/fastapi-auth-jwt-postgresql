from typing import Union
from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    description: Union[str, None] = None
    owner_id: int

class BlogCreate(BlogBase):    
    pass

class BlogUpdate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
