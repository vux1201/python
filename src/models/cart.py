import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_model import Base

if typing.TYPE_CHECKING:
    from models.user import User
    from models.product import ProductVariant


class ShoppingSession(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="shopping_session")
    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="shopping_session", cascade="all, delete-orphan"
    )


class CartItem(Base):
    shopping_session_id: Mapped[int] = mapped_column(ForeignKey("shopping_session.id"))
    product_variant_id: Mapped[int] = mapped_column(ForeignKey("product_variant.id"))
    qty: Mapped[int]

    shopping_session: Mapped["ShoppingSession"] = relationship(
        back_populates="cart_items"
    )
    product_variant: Mapped["ProductVariant"] = relationship(
        back_populates="cart_items"
    )
