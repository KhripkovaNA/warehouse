from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.orders.repository import OrderRepository
from src.orders.schemas import SOrderAdd, SOrderStatus, SOrder

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"]
)


# Получение списка заказов (GET /orders)
@router.get("", response_model=List[SOrder])
async def get_orders(session: AsyncSession = Depends(get_async_session)):
    try:
        orders = await OrderRepository.get_all(session)
        return orders

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve orders: {e}")


# Получение информации о заказе по id (GET /orders/{id})
@router.get("/{order_id}", response_model=SOrder)
async def get_order(order_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        order = await OrderRepository.find_by_id(order_id, session)
        return order

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve the order")


# Создание заказа (POST /orders)
@router.post("")
async def add_order(order_data: SOrderAdd, session: AsyncSession = Depends(get_async_session)):
    try:
        order_id = await OrderRepository.add_order(order_data, session)
        return f"Order added successfully, order_id: {order_id}"

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to add order")


# Обновление статуса заказа (PATCH /orders/{id}/status)
@router.patch("/{order_id}/status")
async def update_order_status(
        order_id: int, new_status: SOrderStatus, session: AsyncSession = Depends(get_async_session)
):
    try:
        await OrderRepository.update_status(order_id, new_status, session)
        return "Order status updated successfully"

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update order status: {e}")
