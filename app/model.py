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
    createdOn: Optional[datetime]
    items: List[OrderItem]
    userAddress: UserAddress
    totalAmount: Optional[float] = 0


class Product(BaseModel):
    name: str
    price: float
    quantity: int
