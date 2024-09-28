from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.database import AsyncSessionLocal
from src.products.models import Product
from src.products.schemas import SProductAdd, SProduct


class ProductRepository:
    @classmethod
    async def get_all(cls, session) -> list[SProduct]:
        query = select(Product)
        result = await session.execute(query)
        product_models = result.scalars().all()
        return product_models

    @classmethod
    async def find_by_id(cls, product_id: int, session) -> SProduct | None:
        query = select(Product).where(Product.id == product_id)
        result = await session.execute(query)
        product_model = result.scalar_one_or_none()
        if not product_model:
            raise HTTPException(
                status_code=404,
                detail=f"Product with id {product_id} not found"
            )
        return product_model

    @classmethod
    async def add_product(cls, product_data: SProductAdd, session) -> int:
        product_dict = product_data.model_dump()
        product = Product(**product_dict)
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product.id

    @classmethod
    async def update_product(cls, product_id: int, product_data: SProductAdd, session) -> SProduct | None:
        query = select(Product).where(Product.id == product_id)
        result = await session.execute(query)
        product_model = result.scalar_one_or_none()

        if not product_model:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

        for key, value in product_data.model_dump().items():
            setattr(product_model, key, value)

        await session.commit()
        return product_model

    @classmethod
    async def delete_product(cls, product_id: int, session):
        query = select(Product).where(Product.id == product_id)
        result = await session.execute(query)
        product_model = result.scalar_one_or_none()

        if not product_model:
            raise HTTPException(
                status_code=404,
                detail=f"Product with id {product_id} not found"
            )

        await session.delete(product_model)
        await session.commit()
