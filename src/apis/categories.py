from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apis.deps import get_db, get_current_admin
import crud
import schemas

router = APIRouter(
    prefix="/categories",
    tags=["category"],
)


@router.get(
    "/",
    summary="Lấy danh sách danh mục sản phẩm",
    response_model=list[schemas.Category],
)
async def read_categories(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    categories = crud.category.get_multi(db=db, skip=skip, limit=limit)
    return categories


@router.post(
    "/",
    summary="Thêm danh mục sản phẩm",
    response_model=schemas.Category,
    dependencies=[Depends(get_current_admin)],
)
async def create_category(
    *, db: Session = Depends(get_db), category_in: schemas.CategoryCreate
):
    category = crud.category.create(db=db, obj_in=category_in)
    return category


@router.get(
    "/{id}",
    summary="Chi tiết danh mục sản phẩm",
    response_model=schemas.Category,
)
async def read_category(*, db: Session = Depends(get_db), id: int):
    category = crud.category.get(db=db, id=id)
    return category


@router.put(
    "/{id}",
    summary="Sửa danh mục sản phẩm",
    response_model=schemas.Category,
    dependencies=[Depends(get_current_admin)],
)
async def update_category(
    *, db: Session = Depends(get_db), id: int, category_in: schemas.CategoryUpdate
):
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    category = crud.category.update(db=db, db_obj=category, obj_in=category_in)
    return category


@router.delete(
    "/{id}",
    summary="Xóa danh mục sản phẩm",
    response_model=schemas.Category,
    dependencies=[Depends(get_current_admin)],
)
async def delete_category(*, db: Session = Depends(get_db), id: int):
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    category = crud.category.remove(db=db, db_obj=category)
    return category
