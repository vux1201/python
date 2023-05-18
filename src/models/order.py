import typing

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base_model import Base

if typing.TYPE_CHECKING:
    from models.user import User
    from models.product import ProductVariant


class Order(Base):
    code: Mapped[str] = mapped_column(String(255))
    status: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    total: Mapped[int]

    user: Mapped["User"] = relationship(back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_variant_id: Mapped[int] = mapped_column(ForeignKey("product_variant.id"))
    qty: Mapped[int]

    order: Mapped["Order"] = relationship(back_populates="order_items")
    product_variant: Mapped["ProductVariant"] = relationship(
        back_populates="order_items"
    )
