from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apis.deps import get_db, get_current_admin
import crud
import schemas

router = APIRouter(
    prefix="/brands",
    tags=["brand"],
)


@router.get(
    "/",
    summary="Lấy danh sách nhãn hiệu",
    response_model=list[schemas.Brand],
)
async def read_brands(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    brands = crud.brand.get_multi(db=db, skip=skip, limit=limit)
    return brands


@router.post(
    "/",
    summary="Thêm nhãn hiệu",
    response_model=schemas.Brand,
    dependencies=[Depends(get_current_admin)],
)
async def create_brand(*, db: Session = Depends(get_db), brand_in: schemas.BrandCreate):
    brand = crud.brand.create(db=db, obj_in=brand_in)
    return brand


@router.get(
    "/{id}",
    summary="Chi tiết nhãn hiệu",
    response_model=schemas.Brand,
)
async def read_brand(*, db: Session = Depends(get_db), id: int):
    brand = crud.brand.get(db=db, id=id)
    return brand


@router.put(
    "/{id}",
    summary="Sửa nhãn hiệu",
    response_model=schemas.Brand,
    dependencies=[Depends(get_current_admin)],
)
async def update_brand(
    *, db: Session = Depends(get_db), id: int, brand_in: schemas.BrandUpdate
):
    brand = crud.brand.get(db=db, id=id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="brand not found"
        )
    brand = crud.brand.update(db=db, db_obj=brand, obj_in=brand_in)
    return brand


@router.delete(
    "/{id}",
    summary="Xóa nhãn hiệu",
    response_model=schemas.Brand,
    dependencies=[Depends(get_current_admin)],
)
async def delete_brand(*, db: Session = Depends(get_db), id: int):
    brand = crud.brand.get(db=db, id=id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="brand not found"
        )
    brand = crud.brand.remove(db=db, db_obj=brand)
    return brand
