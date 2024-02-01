from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class OrderItem(BaseModel):
    productId: str
    boughtQuantity: int


class UserAddress(BaseModel):
    City: str
    Country: str
    ZipCode: str


class Order(BaseModel):
    items: List[OrderItem]
    userAddress: UserAddress
    class Config:
        underscore_attrs_are_private = True
    _createdOn: datetime
    _totalAmount: Optional[float]


class Product(BaseModel):
    name: str
    price: float
    quantity: int
