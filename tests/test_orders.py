import pytest
from httpx import AsyncClient
from sqlalchemy import delete
from src.orders.models import Order, OrderItem
from src.products.models import Product
from tests.conftest import AsyncSessionLocal


@pytest.mark.asyncio
async def test_add_order_1(async_client: AsyncClient):
    await async_client.post("/products", json={
        "name": "table",
        "description": "wooden",
        "price": 100.0,
        "quantity": 10
    })
    await async_client.post("/products", json={
        "name": "chair",
        "description": "wooden",
        "price": 50.0,
        "quantity": 20
    })

    response = await async_client.post("/orders", json={
        "order_items": [
            {
                "product_id": 1,
                "quantity": 5
            },
            {
                "product_id": 2,
                "quantity": 10
            }
        ]
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Order added successfully, id: 1"

    response = await async_client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["quantity"] == 5


@pytest.mark.asyncio
async def test_get_orders(async_client: AsyncClient):
    response = await async_client.get("/orders")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_order(async_client: AsyncClient):
    response = await async_client.get("/orders/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio
async def test_add_order_2(async_client: AsyncClient):
    response = await async_client.post("/orders", json={
        "order_items": [
            {
                "product_id": 1,
                "quantity": 10
            }
        ]
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough products with id 1"

    response = await async_client.get("/orders/2")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order with id 2 not found"


async def test_add_order_3(async_client: AsyncClient):
    response = await async_client.post("/orders", json={
        "order_items": [
            {
                "product_id": 3,
                "quantity": 1
            }
        ]
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 3 not found"

    response = await async_client.get("/orders")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_update_order_status(async_client: AsyncClient):
    response = await async_client.patch("/orders/1/status", params={
        "new_status": "отправлен"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Order status updated successfully"

    response = await async_client.get("/orders/1")

    assert response.status_code == 200
    assert response.json()["status"] == "отправлен"

    async with AsyncSessionLocal() as session:
        await session.execute(delete(OrderItem))
        await session.execute(delete(Product))
        await session.execute(delete(Order))
        await session.commit()
