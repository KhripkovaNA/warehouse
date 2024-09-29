import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope='session')
async def test_add_product(async_client: AsyncClient):
    response = await async_client.post("/products", json={
        "name": "table",
        "description": "wooden",
        "price": 100.0,
        "quantity": 10
    })

    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio(loop_scope='session')
async def test_get_products(async_client: AsyncClient):
    response = await async_client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio(loop_scope='session')
async def test_get_product(async_client: AsyncClient):
    response = await async_client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio(loop_scope='session')
async def test_get_product(async_client: AsyncClient):
    response = await async_client.get("/products/2")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 2 not found"


@pytest.mark.asyncio(loop_scope='session')
async def test_update_product(async_client: AsyncClient):
    response = await async_client.put("/products/1", json={
        "name": "table",
        "description": "wooden",
        "price": 100.0,
        "quantity": 20
    })

    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = await async_client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["quantity"] == 20


@pytest.mark.asyncio(loop_scope='session')
async def test_add_order_1(async_client: AsyncClient):
    await async_client.post("/products", json={
        "name": "wardrobe",
        "description": "wooden",
        "price": 150.0,
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
                "product_id": 2,
                "quantity": 5
            },
            {
                "product_id": 3,
                "quantity": 10
            }
        ]
    })

    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = await async_client.get("/products/2")

    assert response.status_code == 200
    assert response.json()["quantity"] == 5


@pytest.mark.asyncio(loop_scope='session')
async def test_get_orders(async_client: AsyncClient):
    response = await async_client.get("/orders")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio(loop_scope='session')
async def test_get_order(async_client: AsyncClient):
    response = await async_client.get("/orders/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio(loop_scope='session')
async def test_add_order_2(async_client: AsyncClient):
    response = await async_client.post("/orders", json={
        "order_items": [
            {
                "product_id": 2,
                "quantity": 10
            }
        ]
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough products with id 2"

    response = await async_client.get("/orders/2")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order with id 2 not found"


@pytest.mark.asyncio(loop_scope='session')
async def test_add_order_3(async_client: AsyncClient):
    response = await async_client.post("/orders", json={
        "order_items": [
            {
                "product_id": 4,
                "quantity": 1
            }
        ]
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 4 not found"

    response = await async_client.get("/orders")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio(loop_scope='session')
async def test_update_order_status(async_client: AsyncClient):
    response = await async_client.patch("/orders/1/status", params={
        "new_status": "отправлен"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Order status updated successfully"

    response = await async_client.get("/orders/1")

    assert response.status_code == 200
    assert response.json()["status"] == "отправлен"


@pytest.mark.asyncio(loop_scope='session')
async def test_delete_product(async_client: AsyncClient):
    response = await async_client.delete("/products/2")

    assert response.status_code == 200
    assert response.json()["detail"] == "Product with id=2 deleted successfully"

    response = await async_client.get("/products/2")

    assert response.status_code == 404


@pytest.mark.asyncio(loop_scope='session')
async def test_get_order_2(async_client: AsyncClient):
    response = await async_client.get("/orders/1")

    assert response.status_code == 200
    assert len(response.json()["order_items"]) == 1
