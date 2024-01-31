import os
from motor.motor_asyncio import AsyncIOMotorClient


async def get_products_collection():
    client = AsyncIOMotorClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
    db = client["ecommerce"]
    return db["products"]


async def get_orders_collection():
    client = AsyncIOMotorClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
    db = client["ecommerce"]
    return db["orders"]
