from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None


class BookCreate(BookBase):
    owner_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None


class BookResponse(BookBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BookWithOwner(BookResponse):
    owner: UserResponse


class UserWithBooks(UserResponse):
    books: List[BookResponse] = []
