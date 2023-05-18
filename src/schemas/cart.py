from pydantic import BaseModel

from schemas.product import ProductVariant


class CartItemBase(BaseModel):
    product_variant_id: int | None
    qty: int | None


class CartItemCreate(CartItemBase):
    product_variant_id: int
    qty: int


class CartItemUpdate(CartItemBase):
    pass


class CartItem(BaseModel):
    id: int
    product_variant: ProductVariant
    qty: int

    class Config:
        orm_mode = True
