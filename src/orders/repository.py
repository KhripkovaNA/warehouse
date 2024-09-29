from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.orders.models import Order, OrderStatus
from src.orders.schemas import SOrderAdd, SOrder, SOrderStatus
from src.orders.service import OrderService


class OrderRepository:
    @classmethod
    async def get_all(cls, session) -> list[SOrder]:
        query = select(Order).options(selectinload(Order.order_items))
        result = await session.execute(query)
        order_models = result.scalars().all()
        return order_models

    @classmethod
    async def find_by_id(cls, order_id: int, session) -> SOrder | None:
        order = await OrderService.find_by_id(order_id, session)
        return order

    @classmethod
    async def add_order(cls, order_data: SOrderAdd, session) -> SOrder | None:
        order_id = await OrderService.check_and_create_order(order_data, session)
        order = await OrderService.find_by_id(order_id, session)
        return order

    @classmethod
    async def update_status(cls, order_id: int, new_status: SOrderStatus, session) -> SOrder | None:
        query = select(Order).where(Order.id == order_id)
        result = await session.execute(query)
        order_model = result.scalar_one_or_none()
        if not order_model:
            raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")

        order_model.status = OrderStatus(new_status)

        await session.commit()
        return order_model
