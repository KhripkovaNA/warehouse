from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(
    title="Warehouse App",
    lifespan=lifespan
)


products = [
    {'id': 1, 'name': 'table', 'description': '', 'price': 100.0, 'quantity': 5},
    {'id': 2, 'name': 'chair', 'description': '', 'price': 50.0, 'quantity': 10},
    {'id': 3, 'name': 'lamp', 'description': '', 'price': 40.0, 'quantity': 7},
]


@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    return [product for product in products if product.get('id') == product_id]
