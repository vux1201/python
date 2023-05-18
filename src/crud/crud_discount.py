from crud.base import CRUDBase
from schemas import DiscountCreate, DiscountUpdate
from models.product import Discount


class CRUDDiscount(CRUDBase[Discount, DiscountCreate, DiscountUpdate]):
    pass


discount = CRUDDiscount(Discount)
