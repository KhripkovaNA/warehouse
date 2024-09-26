from fastapi import APIRouter

from src.products.schemas import ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["Товары"]
)

@router.get("")
async def get_products() -> list[ProductCreate]:
    tasks = await TaskRepository.find_all()
    return tasks