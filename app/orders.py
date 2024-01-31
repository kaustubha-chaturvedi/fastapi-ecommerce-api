from fastapi import APIRouter, Query, HTTPException
from bson import ObjectId, Timestamp
from typing import List
from datetime import datetime
from app.db import get_orders_collection
from app.model import Order
from app.products import get_products_collection

router = APIRouter()


@router.get("/all", response_model=List[dict])
async def list_orders(
    limit: int = Query(10, gt=0, le=100), offset: int = Query(0, ge=0)
):
    orders_collection = await get_orders_collection()
    orders = orders_collection.find().skip(offset).limit(limit)
    order_list = []
    async for order in orders:
        try:
            created_on = datetime.utcfromtimestamp(order.get("createdOn").time)
        except:
            created_on = None
        order_data = {
            "orderId": str(order["_id"]),
            "createdOn": created_on,
            "totalAmount": order.get("totalAmount", 0),
            "userAddress": order.get("userAddress", {}),
            "items": order.get("items", []),
        }
        order_list.append(order_data)
    return order_list


@router.post("/create", response_model=dict)
async def create_order(order: Order):
    total_amount = 0
    order_items_with_amount = []

    products_collection = await get_products_collection()
    orders_collection = await get_orders_collection()

    for item in order.items:
        product_id = ObjectId(item.productId)

        product = await products_collection.find_one({"_id": product_id})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        amount = product["price"] * item.boughtQuantity
        total_amount += amount

        order_items_with_amount.append(
            {
                "productId": str(product_id),
                "boughtQuantity": item.boughtQuantity,
                "amount": amount,
            }
        )
        await products_collection.update_one(
            {"_id": product_id}, {"$inc": {"quantity": -item.boughtQuantity}}
        )
    created_on_timestamp = Timestamp(int(product_id.generation_time.timestamp()), 0)

    order_data = {
        "createdOn": created_on_timestamp,
        "items": order_items_with_amount,
        "userAddress": order.userAddress.model_dump(),
        "totalAmount": total_amount,
    }

    result = await orders_collection.insert_one(order_data)
    order_id = str(result.inserted_id)
    return {
        "orderId": order_id,
        "totalAmount": total_amount,
        "orderItems": order_items_with_amount,
    }


@router.put("/{order_id}", response_model=dict)
async def update_order(order_id: str, updated_order: Order):
    orders_collection = await get_orders_collection()
    order_id_obj = ObjectId(order_id)
    existing_order = await orders_collection.find_one({"_id": order_id_obj})
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    original_items = existing_order.get("items", [])
    await orders_collection.update_one(
        {"_id": order_id_obj}, {"$set": updated_order.model_dump()}
    )
    products_collection = await get_products_collection()
    for updated_item in updated_order.items:
        product_id = ObjectId(updated_item.productId)
        original_item = next(
            (item for item in original_items if item["productId"] == str(product_id)),
            None,
        )
        if original_item:
            quantity_difference = (
                updated_item.boughtQuantity - original_item["boughtQuantity"]
            )
            await products_collection.update_one(
                {"_id": product_id}, {"$inc": {"quantity": -quantity_difference}}
            )
    return {"message": "Order updated successfully"}


@router.delete("/{order_id}", response_model=dict)
async def delete_order(order_id: str):
    orders_collection = await get_orders_collection()
    result = await orders_collection.delete_one({"_id": ObjectId(order_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}
