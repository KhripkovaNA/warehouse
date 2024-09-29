from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.orders.models import Order, OrderItem
from src.orders.schemas import SOrderAdd, SOrder
from src.products.models import Product
from fastapi import HTTPException


class OrderService:
    @staticmethod
    async def check_and_create_order(order_data: SOrderAdd, session) -> int:
        try:
            # Создание заказа
            order = Order()

            # Получение всех продуктов, участвующих в заказе
            product_ids = [item.product_id for item in order_data.order_items]
            query = select(Product).where(Product.id.in_(product_ids))
            result = await session.execute(query)
            products = {product.id: product for product in result.scalars().all()}

            # Проверка наличия и достаточного количества товара на складе
            for item in order_data.order_items:
                product = products.get(item.product_id)
                if product is None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product with id {item.product_id} not found"
                        )

                if product.quantity < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough products with id {item.product_id}"
                        )

                order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
                session.add(order_item)
                order.order_items.append(order_item)

                # Обновление количества товаров
                product.quantity -= item.quantity

            session.add(order)
            await session.commit()
            await session.refresh(order)

            return order.id

        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def find_by_id(order_id: int, session) -> SOrder:
        query = select(Order).where(Order.id == order_id).options(selectinload(Order.order_items))
        result = await session.execute(query)
        order_model = result.scalar_one_or_none()
        if not order_model:
            raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
        return order_model
