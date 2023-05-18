from sqlalchemy import select, Select
from sqlalchemy.orm import Session, joinedload

from crud.base import CRUDBase
from models.product import Brand, Category, Discount, Product, ProductVariant
from schemas import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_multi_filter(
        self,
        category_id: list[int] | None = None,
        brand_id: list[int] | None = None,
        keyword: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
    ) -> Select[tuple[Product]]:
        stmt = select(Product)
        if category_id:
            stmt = stmt.where(Product.category_id.in_(category_id))
        if brand_id:
            stmt = stmt.where(Product.brand_id.in_(brand_id))
        if keyword:
            stmt = stmt.where(Product.name.icontains(keyword))
        if min_price:
            stmt = stmt.options(joinedload(Product.product_variants)).where(
                Product.product_variants.any(ProductVariant.price > min_price)
            )
        if max_price:
            stmt = stmt.options(joinedload(Product.product_variants)).where(
                Product.product_variants.any(ProductVariant.price < max_price)
            )
        return stmt


product = CRUDProduct(Product)
