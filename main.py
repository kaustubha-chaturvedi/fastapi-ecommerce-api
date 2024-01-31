from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.products import router as product_router
from app.orders import router as order_router

app = FastAPI()
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(order_router, prefix="/orders", tags=["orders"])