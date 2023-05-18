from pydantic import BaseModel

from schemas.category import Category
from schemas.brand import Brand
from schemas.product_variant import ProductVariant


class ProductBase(BaseModel):
    name: str
    category_id: int
    brand_id: int
    description: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(BaseModel):
    id: int
    name: str
    category: Category
    brand: Brand
    description: str
    product_variants: list["ProductVariant"]

    class Config:
        orm_mode = True
