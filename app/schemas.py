from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
# from enum import Enum


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


    class Config:
        orm_mode = True
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: int
    published: bool

    class Config:
        orm_mode = True
        from_attributes = True

class PostOut(BaseModel):
    published: bool
    created_at: datetime
    content: str
    title: str
    id: int
    owner_id: int
    votes: int
    owner: Optional[UserOut] = None  

    class Config:
        orm_mode = True
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
 

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # type: ignore


# class DirEnum(int, Enum):
#     up = 1
#     down = 0

# class Vote(BaseModel):
#     post_id: int
#     dir: DirEnum