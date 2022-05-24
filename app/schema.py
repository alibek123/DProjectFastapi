from datetime import datetime
from typing import Optional, List

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
    # image: Optional[str]
    # thumbnail: Optional[str]


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


class ShowCartItems(BaseModel):
    id: int
    meals: Meal
    created_at: datetime

    class Config:
        orm_mode = True


class ShowCart(BaseModel):
    id: int
    cart_items: List[ShowCartItems] = []

    class Config:
        orm_mode = True


class ShowOrderDetails(BaseModel):
    id: int
    order_id: int
    product_order_details: Meal

    class Config:
        orm_mode = True


class ShowOrder(BaseModel):
    id: Optional[int]
    order_date: datetime
    order_amount: float
    order_status: str
    order_details: List[ShowOrderDetails] = []

    class Config:
        orm_mode = True
