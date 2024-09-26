from sqlalchemy import select
from src.database import AsyncSessionLocal
from models import Product
from schemas import ProductCreate


class ProductRepository:
    @classmethod
    async def find_all(cls) -> list[ProductCreate]:
        async with AsyncSessionLocal() as session:
            query = select(Product)
            result = await session.execute(query)
            product_models = result.scalars().all()
            product_schemas = [ProductCreate.model_validate(product_model) for product_model in product_models]
            return product_schemas
