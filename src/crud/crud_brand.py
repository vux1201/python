from crud.base import CRUDBase
from schemas import BrandCreate, BrandUpdate
from models.product import Brand


class CRUDBrand(CRUDBase[Brand, BrandCreate, BrandUpdate]):
    pass


brand = CRUDBrand(Brand)
