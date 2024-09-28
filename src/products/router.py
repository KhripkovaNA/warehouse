from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.products.repository import ProductRepository
from src.products.schemas import SProductAdd, SProduct


router = APIRouter(
    prefix="/products",
    tags=["Товары"]
)


# Получение списка товаров (GET /products)
@router.get("", response_model=List[SProduct])
async def get_products(session: AsyncSession = Depends(get_async_session)):
    try:
        products = await ProductRepository.get_all(session)
        return products

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve products")


# Получение информации о товаре по id (GET /products/{id})
@router.get("/{product_id}")
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        product = await ProductRepository.find_by_id(product_id, session)
        return product

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve the product")


# Создание товара (POST /products)
@router.post("")
async def add_product(product_data: SProductAdd, session: AsyncSession = Depends(get_async_session)):
    try:
        product_id = await ProductRepository.add_product(product_data, session)
        return f"Product added successfully, product_id: {product_id}"

    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to add product")


# Обновление информации о товаре (PUT /products/{id})
@router.put("/{product_id}")
async def update_product(
        product_id: int, product_data: SProductAdd, session: AsyncSession = Depends(get_async_session)
):
    try:
        await ProductRepository.update_product(product_id, product_data, session)
        return "Product updated successfully"

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update product")


# Удаление товара (DELETE /products/{id})
@router.delete("/{product_id}")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        await ProductRepository.delete_product(product_id, session)
        return "Product deleted successfully"

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete product")
