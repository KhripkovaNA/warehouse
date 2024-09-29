from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Model


# Product (Товар): id, название, описание, цена, количество на складе
class Product(Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(default=None)
    price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    orders: Mapped[List['OrderItem']] = relationship(
        "OrderItem",
        back_populates="product",
        cascade="all, delete-orphan"
    )
