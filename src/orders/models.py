from typing import List
from sqlalchemy import Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
import enum
from src.database import Model


class OrderStatus(enum.Enum):
    IN_PROCESS = "в процессе"
    SHIPPED = "отправлен"
    DELIVERED = "доставлен"


# Order (Заказ): id, дата создания, статус
class Order(Model):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.IN_PROCESS)

    order_items: Mapped[List['OrderItem']] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


# OrderItem (Предмет Заказа): id, заказ, продукт, количество
class OrderItem(Model):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    order: Mapped['Order'] = relationship("Order", back_populates="order_items")

    product: Mapped['Product'] = relationship("Product", back_populates="orders")
