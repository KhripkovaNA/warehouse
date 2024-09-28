from fastapi import FastAPI
from src.database import create_tables, delete_tables
from contextlib import asynccontextmanager
from src.products.router import router as products_router
from src.orders.router import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    # await create_tables()
    yield
    print("Выключение")

app = FastAPI(
    title="Склад",
    lifespan=lifespan
)


app.include_router(products_router)
app.include_router(orders_router)
