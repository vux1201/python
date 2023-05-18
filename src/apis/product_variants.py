import os
import secrets

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Request
from PIL import Image
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_current_admin, get_db
from utils.constants import IMAGE_TYPES_ALLOWED
from core.config import settings

router = APIRouter(
    prefix="/product-variants",
    tags=["product-variants"],
    dependencies=[Depends(get_current_admin)],
)


@router.post("/uploadfile/", summary="Upload ảnh sản phẩm")
async def upload_file(*, file: UploadFile = File(...), request: Request):
    if not file.content_type in IMAGE_TYPES_ALLOWED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ cho phép upload định dạng jpeg/png",
        )
    img = Image.open(file.file)
    img_out_size = (512, 512)
    img.thumbnail(img_out_size)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)  # type: ignore
    image_fn = random_hex + f_ext  # type: ignore
    to_save_path = os.path.join("media/product_images", image_fn)
    img.save(to_save_path)
    img.close()

    return settings.HOST_URL + "/files/" + image_fn


@router.get(
    "/products/{product_id}/variants",
    response_model=list[schemas.ProductVariant],
    summary="Lấy danh sách mẫu mã của sản phẩm",
)
async def read_variants(*, db: Session = Depends(get_db), product_id: int):
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sản phẩm với id này",
        )
    variants = product.product_variants
    return variants


@router.post(
    "/products/{product_id}/variants",
    response_model=schemas.ProductVariant,
    summary="Tạo mẫu mã sản phẩm",
)
async def create_variant(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    variant_in: schemas.ProductVariantCreate
):
    variant = crud.product_variant.create(
        db=db, variant_in=variant_in, product_id=product_id
    )
    return variant


@router.get(
    "/products/{product_id}/variants/{variant_id}",
    response_model=schemas.ProductVariant,
    summary="Xem chi tiết mẫu mã sản phẩm",
)
async def read_variant(
    *, db: Session = Depends(get_db), product_id: int, variant_id: int
):
    variant = crud.product_variant.get(db=db, id=variant_id)
    return variant


@router.put(
    "/products/{product_id}/variants/{variant_id}",
    response_model=schemas.ProductVariant,
    summary="Sửa mẫu mã sản phẩm",
)
async def update_variant(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    variant_id: int,
    variant_in: schemas.ProductVariantUpdate
):
    db_variant = crud.product_variant.get(db=db, id=variant_id)
    if not db_variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy mẫu mã với id này",
        )
    variant = crud.product_variant.update(
        db=db, db_variant=db_variant, variant_in=variant_in
    )
    return variant


@router.delete(
    "/products/{product_id}/variants/{variant_id}",
    response_model=schemas.ProductVariant,
    summary="Xóa mẫu mã sản phẩm",
)
async def delete_variant(
    *, db: Session = Depends(get_db), product_id: int, variant_id: int
):
    db_variant = crud.product_variant.get(db=db, id=variant_id)
    if not db_variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy mẫu mã với id này",
        )
    variant = crud.product_variant.remove(db=db, db_obj=db_variant)
    return variant
