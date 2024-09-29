from fastapi import FastAPI
from src.products.router import router as products_router
from src.orders.router import router as orders_router


app = FastAPI(
    title="Склад"
)

app.include_router(products_router)
app.include_router(orders_router)
