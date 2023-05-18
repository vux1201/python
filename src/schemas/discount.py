from pydantic import BaseModel


class DiscountBase(BaseModel):
    name: str


class DiscountCreate(DiscountBase):
    pass


class DiscountUpdate(DiscountBase):
    pass


class Discount(DiscountBase):
    id: int
    name: str
    discount_percent: int

    class Config:
        orm_mode = True
