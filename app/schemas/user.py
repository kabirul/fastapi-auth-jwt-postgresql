from typing import List,Optional
from pydantic import BaseModel,EmailStr
from .import Blog

class UserBase(BaseModel):   
    username: str
    email: EmailStr
      
    
class UserCreate(UserBase):     
    password: str

class UserUpdate(UserBase):     
    password: str  

class User(UserBase):
    #id: int
    id: Optional[int] = None
    #is_active: bool
    is_active: Optional[bool] = None
    blogs: List[Blog] = []
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

