from crud.base import CRUDBase
from schemas import CategoryCreate, CategoryUpdate
from models.product import Category


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


category = CRUDCategory(Category)
