from sqlalchemy.orm import Mapped, mapped_column
from src.database import Model


# Product (Товар): id, название, описание, цена, количество на складе.
class Product(Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None] = None
    price: Mapped[float]
    quantity: Mapped[int]
