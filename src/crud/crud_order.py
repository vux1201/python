from crud.base import CRUDBase
from schemas import OrderCreate, OrderUpdate
from models.order import Order


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    pass


order = CRUDOrder(Order)
