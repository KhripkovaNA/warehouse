from fastapi import FastAPI
from src.database import create_tables, delete_tables
from contextlib import asynccontextmanager
from src.products.router import router as router_products


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield
    print("Выключение")

app = FastAPI(
    title="WarehouseApp",
    lifespan=lifespan
)


app.include_router(router_products)
