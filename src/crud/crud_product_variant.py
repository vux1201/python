from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

import crud
from crud.base import CRUDBase
from models.product import ProductVariant, ProductVariantImage, Product
from schemas import ProductVariantCreate, ProductVariantUpdate, ProductVariantImageBase


class CRUDProduct(CRUDBase[ProductVariant, ProductVariantCreate, ProductVariantUpdate]):
    def get_multi_by_product(self, db: Session, product: Product):
        return product.product_variants

    def create(  # type: ignore[override]
        self, db: Session, variant_in: ProductVariantCreate, product_id: int
    ) -> ProductVariant:
        variant = ProductVariant(
            product_id=product_id,
            name=variant_in.name,
            color=variant_in.color,
            sku=variant_in.sku,
            price=variant_in.price,
            inventory=variant_in.inventory,
        )
        for image in variant_in.images:
            variant_image = ProductVariantImage(image_path=image.image_path)
            variant.images.append(variant_image)
        db.add(variant)
        db.commit()
        db.refresh(variant)
        return variant

    def update(
        self,
        db: Session,
        db_variant: ProductVariant,
        variant_in: ProductVariantUpdate | dict[str, Any],
    ):
        variant = super().update(db=db, db_obj=db_variant, obj_in=variant_in)
        if isinstance(variant_in, dict):
            images = variant_in.get("images", [])
            images = [ProductVariantImageBase(**image) for image in images]
        else:
            images = variant_in.images
        # since we allow to delete images and/or add new image to variant
        # we need to treat them by checking ids
        current_image_ids = [image.id for image in variant.images]
        coming_image_ids = [image.id for image in images if image.id]
        unsaved_images = [image for image in images if not image.id]
        deleted_image_ids = [
            id for id in current_image_ids if id not in coming_image_ids
        ]
        for image in unsaved_images:
            new_image = ProductVariantImage(image_path=image.image_path)
            variant.images.append(new_image)
        for image_id in deleted_image_ids:
            deleted_image = db.scalar(
                select(ProductVariantImage).filter(ProductVariantImage.id == image_id)
            )
            # ignore type here, since the image surely exist
            variant.images.remove(deleted_image)  # type: ignore
            db.delete(deleted_image)
        db.commit()
        db.refresh(variant)
        return variant


product_variant = CRUDProduct(ProductVariant)
