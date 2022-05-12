from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class MealBase(BaseModel):
    name: str
    slug: str
    price: int
    protein: int
    fats: int
    carbs: int
    description: Optional[str] = None
    available_inventory: int
    category_id: int


class MealCreate(MealBase):
    pass


class Meal(MealBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str


class UserCreate(UserBase):
    password: str
    is_staff: Optional[bool] = False


class User(UserBase):
    id: int
    created_at: datetime
    is_staff: bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
