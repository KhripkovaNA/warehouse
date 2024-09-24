from sqlalchemy import DateTime, Enum, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Model
from datetime import datetime
import enum


class OrderStatus(enum.Enum):
    IN_PROCESS = "в процессе"
    SHIPPED = "отправлен"
    DELIVERED = "доставлен"


class Order(Model):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.IN_PROCESS)


class OrderItem(Model):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    # # Optional: relationship definitions to access related Order and Product objects
    # order: Mapped['Order'] = relationship('Order', back_populates='items')
    # product: Mapped['Product'] = relationship('Product')


