import typing

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_model import Base

if typing.TYPE_CHECKING:
    from models.cart import ShoppingSession
    from models.order import Order


class User(Base):
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str]
    firstname: Mapped[str] = mapped_column(String(30), nullable=True)
    lastname: Mapped[str] = mapped_column(String(30), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[int] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)

    shopping_session: Mapped["ShoppingSession"] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
