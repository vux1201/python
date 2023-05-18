from pydantic import BaseModel

from schemas.user import User
from schemas.product_variant import ProductVariant


class OrderItemBase(BaseModel):
    product_variant_id: int | None
    qty: int | None


class OrderItemCreate(OrderItemBase):
    product_variant_id: int
    price: int
    qty: int


class OrderItemUpdate(OrderItemBase):
    pass


class OrderItem(BaseModel):
    id: int
    product_variant: ProductVariant
    qty: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    code: str | None
    status: int | None
    total: int | None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: int | None


class Order(OrderBase):
    id: int
    order_items: list["OrderItem"]

    class Config:
        orm_mode = True


class OrderAdmin(Order):
    user: User
