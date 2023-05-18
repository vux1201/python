from pydantic import BaseModel, AnyHttpUrl


class ProductVariantImageBase(BaseModel):
    id: int | None
    image_path: AnyHttpUrl


class ProductVariantImage(ProductVariantImageBase):
    id: int

    class Config:
        orm_mode = True


class ProductVariantBase(BaseModel):
    name: str
    color: str
    sku: str
    price: int
    inventory: int
    images: list["ProductVariantImageBase"] = []


class ProductVariantCreate(ProductVariantBase):
    images: list["ProductVariantImageBase"]


class ProductVariantUpdate(ProductVariantBase):
    pass


class ProductVariant(BaseModel):
    id: int
    product_id: int
    name: str
    color: str
    sku: str
    price: int
    inventory: int
    images: list["ProductVariantImage"]

    class Config:
        orm_mode = True
