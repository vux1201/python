from crud.base import CRUDBase
from schemas import CartItemCreate, CartItemUpdate
from models.cart import CartItem


class CRUDCartItem(CRUDBase[CartItem, CartItemCreate, CartItemUpdate]):
    pass


cart_item = CRUDCartItem(CartItem)
