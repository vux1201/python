from fastapi import APIRouter

from apis import (
    brands,
    carts,
    categories,
    discounts,
    login,
    orders,
    products,
    users,
    product_variants,
)

api_router = APIRouter()

api_router.include_router(brands.router)
api_router.include_router(carts.router)
api_router.include_router(categories.router)
api_router.include_router(discounts.router)
api_router.include_router(login.router)
api_router.include_router(orders.router)
api_router.include_router(products.router)
api_router.include_router(product_variants.router)
api_router.include_router(users.router)
