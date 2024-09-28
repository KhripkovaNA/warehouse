import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_product(async_client: AsyncClient):
    response = await async_client.post("/products", json={
        "name": "table",
        "description": "wooden",
        "price": 100.0,
        "quantity": 10
    })

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_products(async_client: AsyncClient):
    response = await async_client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_product(async_client: AsyncClient):
    response = await async_client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio
async def test_get_product(async_client: AsyncClient):
    response = await async_client.get("/products/2")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 2 not found"


@pytest.mark.asyncio
async def test_update_product(async_client: AsyncClient):
    response = await async_client.put("/products/1", json={
        "name": "table",
        "description": "wooden",
        "price": 100.0,
        "quantity": 20
    })

    assert response.status_code == 200
    assert response.json() == "Product updated successfully"

    response = await async_client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["quantity"] == 20


@pytest.mark.asyncio
async def test_delete_product(async_client: AsyncClient):
    response = await async_client.delete("/products/1")

    assert response.status_code == 200
    assert response.json() == "Product deleted successfully"

    response = await async_client.get("/products/1")

    assert response.status_code == 404
