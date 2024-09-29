from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.products.repository import ProductRepository
from src.products.schemas import SProductAdd, SProduct, Detail


router = APIRouter(
    prefix="/products",
    tags=["Товары"]
)


# Получение списка товаров (GET /products)
@router.get("",
            response_model=List[SProduct],
            summary="Получение списка товаров")
async def get_products(session: AsyncSession = Depends(get_async_session)):
    try:
        products = await ProductRepository.get_all(session)
        return products

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve products")


# Получение информации о товаре по id (GET /products/{id})
@router.get("/{product_id}",
            response_model=SProduct,
            summary="Получение информации о товаре по id")
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        product = await ProductRepository.find_by_id(product_id, session)
        return product

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve the product")


# Создание товара (POST /products)
@router.post("",
             response_model=SProduct,
             summary="Создание товара",
             response_description="Созданный товар")
async def add_product(product_data: SProductAdd, session: AsyncSession = Depends(get_async_session)):
    try:
        product = await ProductRepository.add_product(product_data, session)
        return product

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to add product")


# Обновление информации о товаре (PUT /products/{id})
@router.put("/{product_id}",
            response_model=SProduct,
            summary="Обновление информации о товаре",
            response_description="Обновленный товар")
async def update_product(
        product_id: int, product_data: SProductAdd, session: AsyncSession = Depends(get_async_session)
):
    try:
        product = await ProductRepository.update_product(product_id, product_data, session)
        return product

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update product")


# Удаление товара (DELETE /products/{id})
@router.delete("/{product_id}",
               response_model=Detail,
               summary="Удаление товара")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_async_session)) -> dict[str, str]:
    try:
        await ProductRepository.delete_product(product_id, session)
        return {"detail": f"Product with id={product_id} deleted successfully"}

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete product")
