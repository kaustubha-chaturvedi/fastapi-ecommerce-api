import asyncio,os
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

fake = Faker()


async def generate_fake_product():
    return {
        "_id": ObjectId(),
        "name": fake.word(),
        "price": fake.pyfloat(min_value=10, max_value=1000, right_digits=2),
        "quantity": fake.random_int(min=1, max=100),
    }


async def add_fake_products(num):
    client = AsyncIOMotorClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
    db = client["ecommerce"]
    products_collection = db["products"]

    fake_products = [await generate_fake_product() for _ in range(num)]
    await products_collection.insert_many(fake_products)

    print(f"{num} fake products added to the database.")

    client.close()


asyncio.run(
    add_fake_products(int(input("How many fake products do you want to add? ")))
)
