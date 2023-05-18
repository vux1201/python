from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apis.deps import get_db, get_current_admin
import crud
import schemas

router = APIRouter(
    prefix="/discounts",
    tags=["discount"],
    dependencies=[Depends(get_current_admin)],
)


@router.get(
    "/",
    summary="Lấy danh sách mã giảm giá",
    response_model=list[schemas.Discount],
    dependencies=[Depends(get_current_admin)],
)
async def read_discounts(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    discounts = crud.discount.get_multi(db=db, skip=skip, limit=limit)
    return discounts


@router.post(
    "/",
    summary="Thêm mã giảm giá",
    response_model=schemas.Discount,
    dependencies=[Depends(get_current_admin)],
)
async def create_discount(
    *, db: Session = Depends(get_db), discount_in: schemas.DiscountCreate
):
    discount = crud.discount.create(db=db, obj_in=discount_in)
    return discount


@router.get(
    "/{id}",
    summary="Chi tiết mã giảm giá",
    response_model=schemas.Discount,
    dependencies=[Depends(get_current_admin)],
)
async def read_discount(*, db: Session = Depends(get_db), id: int):
    discount = crud.discount.get(db=db, id=id)
    return discount


@router.put(
    "/{id}",
    summary="Sửa mã giảm giá",
    response_model=schemas.Discount,
    dependencies=[Depends(get_current_admin)],
)
async def update_discount(
    *, db: Session = Depends(get_db), id: int, discount_in: schemas.DiscountUpdate
):
    discount = crud.discount.get(db=db, id=id)
    if not discount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="discount not found"
        )
    discount = crud.discount.update(db=db, db_obj=discount, obj_in=discount_in)
    return discount


@router.delete(
    "/{id}",
    summary="Xóa mã giảm giá",
    response_model=schemas.Discount,
    dependencies=[Depends(get_current_admin)],
)
async def delete_discount(*, db: Session = Depends(get_db), id: int):
    discount = crud.discount.get(db=db, id=id)
    if not discount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="discount not found"
        )
    discount = crud.discount.remove(db=db, db_obj=discount)
    return discount
