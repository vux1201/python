import typing

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.base_model import Base

if typing.TYPE_CHECKING:
    from models.cart import CartItem
    from models.order import OrderItem


class Category(Base):
    name: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(nullable=True)

    products: Mapped[list["Product"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"{self.name}"


class Brand(Base):
    name: Mapped[str] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship(
        back_populates="brand", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"{self.name}"


class Product(Base):
    name: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.id"))
    description: Mapped[str]

    category: Mapped["Category"] = relationship(back_populates="products")
    brand: Mapped["Brand"] = relationship(back_populates="products")
    product_variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return self.name


class ProductVariant(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    name: Mapped[str] = mapped_column(String(255))
    color: Mapped[str] = mapped_column(String(15), default="#000000")
    sku: Mapped[str] = mapped_column(String(255))
    price: Mapped[int]
    inventory: Mapped[int]

    product: Mapped["Product"] = relationship(back_populates="product_variants")
    discount: Mapped["Discount"] = relationship(back_populates="product_variant")
    images: Mapped[list["ProductVariantImage"]] = relationship(
        back_populates="product_variant", cascade="all, delete-orphan"
    )
    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="product_variant", cascade="all, delete-orphan"
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product_variant", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return self.name


class Discount(Base):
    product_variant_id: Mapped[int] = mapped_column(ForeignKey("product_variant.id"))
    name: Mapped[str] = mapped_column(String(255))
    discount_percent: Mapped[int]

    product_variant: Mapped["ProductVariant"] = relationship(back_populates="discount")


class ProductVariantImage(Base):
    product_variant_id: Mapped[int] = mapped_column(ForeignKey("product_variant.id"))
    image_path: Mapped[str]

    product_variant: Mapped["ProductVariant"] = relationship(back_populates="images")
