# Import all the models, so that Alembic can read from memory
# and auto generate migration
# https://stackoverflow.com/questions/15660676/alembic-autogenerate-producing-empty-migration
from db.base_model import Base
from models.cart import CartItem, ShoppingSession
from models.order import Order, OrderItem
from models.product import (
    Brand,
    Category,
    Discount,
    Product,
    ProductVariant,
    ProductVariantImage,
)
from models.user import User
