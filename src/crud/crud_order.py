from sqlalchemy import select, Select

from crud.base import CRUDBase
from schemas import OrderCreate, OrderUpdate
from models.order import Order


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_multi_filter(
        self,
    ) -> Select[tuple[Order]]:
        stmt = select(Order).order_by(Order.created_at.desc())
        return stmt


order = CRUDOrder(Order)
