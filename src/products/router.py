from fastapi import APIRouter, HTTPException
from src.products.dependencies import ProductRepository
from src.products.schemas import SProductAdd


router = APIRouter(
    prefix="/products",
    tags=["Товары"]
)


@router.get("")
async def get_products():
    # try:
    #     products = await ProductRepository.get_all()
    #     return {
    #         "status": "success",
    #         "data": products,
    #         "details": None
    #     }
    # except Exception:
    #     raise HTTPException(status_code=500, detail={
    #         "status": "error",
    #         "data": None,
    #         "details": "Failed to retrieve products"
    #     })
    products = await ProductRepository.get_all()
    return {
        "status": "success",
        "data": products,
        "details": None
    }


@router.get("/{product_id}")
async def get_product(product_id: int):
    try:
        product = await ProductRepository.find_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": "Product not found"
            })
        return {
            "status": "success",
            "data": product,
            "details": None
        }
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Failed to retrieve the product"
        })


@router.post("")
async def add_product(product_data: SProductAdd):
    try:
        product_id = await ProductRepository.add_product(product_data)
        return {
            "status": "success",
            "data": {"id": product_id},
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Failed to add product"
        })


@router.put("/{product_id}")
async def update_product(product_id: int, product_data: SProductAdd):
    try:
        product = await ProductRepository.find_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": "Product not found"
            })
        await ProductRepository.update_product(product_id, product_data)
        return {
            "status": "success",
            "data": None,
            "details": "Product updated successfully"
        }
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Failed to update product"
        })


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    try:
        product = await ProductRepository.find_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": "Product not found"
            })
        await ProductRepository.delete_product(product_id)
        return {
            "status": "success",
            "data": None,
            "details": "Product deleted successfully"
        }
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Failed to delete product"
        })
